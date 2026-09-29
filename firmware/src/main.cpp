// Mochi rzmong — reaksi sentuh + menu iPod
#include <Arduino.h>
#include <TFT_eSPI.h>
#include <AnimatedGIF.h>
#include <SD.h>
#include <SPI.h>
#include <WiFi.h>
#include <WebServer.h>
#include <Preferences.h>
#include <ArduinoJson.h>
#include <ChronosESP32.h>
#include "driver/i2s.h"
#include "MochiRzmong.h"
#include "defaults_gif.h"
#include "jingle.h"

static const int PIN_TOUCH = 1;
static const int PIN_SD_SCK = 4, PIN_SD_MISO = 2, PIN_SD_MOSI = 6, PIN_SD_CS = 5;
static const int PIN_I2S_BCLK = 21, PIN_I2S_LRC = 20, PIN_I2S_DIN = 9;
static const int W = 240, H = 240;
static const uint16_t C_BG=0x1082,C_BAR=0xFD20,C_SEL=0xFE60,C_TEXT=0xEF7D,C_DIM=0x8410,C_RED=0xF985,C_TEAL=0x07F4,C_BLUE=0x3C7F,C_PINK=0xF81F;

TFT_eSPI tft; AnimatedGIF gif; WebServer server(80); ChronosESP32 watch; Preferences prefs;
String theme="wajah", playMode="kategori";
bool soundOn=true, useSd=false, chronosOn=false, showWm=true;
int defIdx=2;
static const char *THEMES[]={"wajah","gundam","mobil","neon","anime","makanan","musik","intro"};
static const int NTHEME=8;
String parts[32]; int nparts=0, idx=0; File gifFile; bool sdOk=false, i2sOk=false;
enum Ui { UI_PLAY, UI_MENU }; Ui ui=UI_PLAY; int menuRow=0;
struct MenuItem { const char *icon; const char *label; uint16_t col; };
static const MenuItem MENU[]={
  {">","GIF berikutnya",C_TEAL},{"~","Mode acak",C_BAR},{"N","Musik tes",C_PINK},
  {"S","Sumber SD/Flash",C_BLUE},{"x","Bisu / bunyi",C_RED},{"+","Chronos",C_TEAL},
  {"i","Tentang rzmong",C_TEXT},{"<","Tutup",C_DIM}
};
static const int NMENU=8;
uint32_t downAt=0, lastTap=0; int taps=0; bool prevDown=false; bool pendingReact=false;

void loadPrefs(){prefs.begin("rzmong",false);theme=prefs.getString("theme","wajah");playMode=prefs.getString("mode","kategori");soundOn=prefs.getBool("sound",true);useSd=prefs.getBool("usesd",false);chronosOn=prefs.getBool("chrono",false);showWm=prefs.getBool("wm",true);defIdx=prefs.getInt("def",2);if(defIdx<0||defIdx>=DEFAULT_GIF_COUNT)defIdx=0;}
void savePrefs(){prefs.putString("theme",theme);prefs.putString("mode",playMode);prefs.putBool("sound",soundOn);prefs.putBool("usesd",useSd);prefs.putBool("chrono",chronosOn);prefs.putBool("wm",showWm);prefs.putInt("def",defIdx);}
void scanTheme(const String &t){nparts=0;if(!sdOk)return;String dir=String("/gif/")+t;File d=SD.open(dir);if(!d)return;while(true){File f=d.openNextFile();if(!f)break;String n=f.name();f.close();if(n.endsWith(".gif")&&nparts<32){int slash=n.lastIndexOf('/');parts[nparts++]=dir+"/"+n.substring(slash<0?0:slash+1);}}d.close();}
void GIFDraw(GIFDRAW *p){if(p->y>=H)return;uint16_t line[240];uint8_t *s=p->pPixels;int w=p->iWidth;if(w>W)w=W;for(int x=0;x<w;x++){uint8_t c=*s++;if(p->ucHasTransparency&&c==p->ucTransparent){line[x]=TFT_BLACK;continue;}uint8_t *pal=(uint8_t*)p->pPalette+c*3;line[x]=tft.color565(pal[0],pal[1],pal[2]);}int y0=(H-p->iHeight)/2+p->iY+p->y;if(y0<0||y0>=H)return;tft.pushImage((W-p->iWidth)/2+p->iX,y0,w,1,line);}
void *gifOpen(const char *name,int32_t *sz){gifFile=SD.open(name);if(!gifFile)return NULL;*sz=gifFile.size();return (void*)1;}
void gifClose(void*){if(gifFile)gifFile.close();}
int32_t gifRead(GIFFILE *p,uint8_t *buf,int32_t len){int n=gifFile.read(buf,len);p->iPos=gifFile.position();return n;}
int32_t gifSeek(GIFFILE *p,int32_t pos){gifFile.seek(pos);p->iPos=gifFile.position();return p->iPos;}
void audioInit(){i2s_config_t cfg={.mode=(i2s_mode_t)(I2S_MODE_MASTER|I2S_MODE_TX),.sample_rate=JINGLE_SR,.bits_per_sample=I2S_BITS_PER_SAMPLE_16BIT,.channel_format=I2S_CHANNEL_FMT_ONLY_LEFT,.communication_format=I2S_COMM_FORMAT_STAND_I2S,.intr_alloc_flags=0,.dma_buf_count=4,.dma_buf_len=256,.use_apll=false,.tx_desc_auto_clear=true,.fixed_mclk=0};if(i2s_driver_install(I2S_NUM_0,&cfg,0,NULL)!=ESP_OK)return;i2s_pin_config_t pins={.mck_io_num=I2S_PIN_NO_CHANGE,.bck_io_num=PIN_I2S_BCLK,.ws_io_num=PIN_I2S_LRC,.data_out_num=PIN_I2S_DIN,.data_in_num=I2S_PIN_NO_CHANGE};if(i2s_set_pin(I2S_NUM_0,&pins)!=ESP_OK)return;i2sOk=true;}
void playJingleMs(int ms){if(!soundOn||!i2sOk)return;int bytes=JINGLE_SR*2*ms/1000;if(bytes>JINGLE_PCM_LEN)bytes=JINGLE_PCM_LEN;if(bytes<2)bytes=2;size_t wr=0;i2s_write(I2S_NUM_0,JINGLE_PCM,bytes,&wr,pdMS_TO_TICKS(ms+50));}
void drawReact(){tft.fillRoundRect(28,78,184,84,18,C_BAR);tft.fillRoundRect(36,86,168,68,14,C_SEL);tft.setTextColor(TFT_BLACK,C_SEL);tft.drawCentreString("o_o",120,100,4);tft.drawCentreString("tickle",120,132,2);}
void brandMark(){if(!showWm)return;tft.setTextColor(C_DIM,TFT_BLACK);tft.drawString(MOCHI_BRAND,168,226,1);}
void bootMark(){tft.fillScreen(C_BG);tft.fillRoundRect(20,80,200,80,16,C_BAR);tft.setTextColor(TFT_BLACK,C_BAR);tft.drawCentreString("Mochi",120,96,4);tft.drawCentreString(MOCHI_BRAND,120,128,2);delay(450);}
void drawMenu(){tft.fillScreen(C_BG);tft.fillRect(0,0,240,34,C_BAR);tft.setTextColor(TFT_BLACK,C_BAR);tft.drawCentreString("MOCHI  rzmong",120,10,2);for(int i=0;i<NMENU;i++){int y=40+i*24;if(i==menuRow){tft.fillRoundRect(6,y-2,228,23,6,C_SEL);tft.fillCircle(20,y+9,7,MENU[i].col);tft.setTextColor(TFT_BLACK,C_SEL);}else{tft.fillCircle(20,y+9,6,MENU[i].col);tft.setTextColor(C_TEXT,C_BG);}tft.drawString(String(MENU[i].icon)+"  "+MENU[i].label,34,y+2,2);}}
void nextPart(){if(useSd&&sdOk){if(playMode=="acak"){theme=THEMES[random(NTHEME)];scanTheme(theme);}if(nparts==0)scanTheme(theme);if(nparts==0){useSd=false;return;}idx=(playMode=="acak_tema")?random(nparts):(idx+1)%nparts;}else{defIdx=(defIdx+1)%DEFAULT_GIF_COUNT;theme=DEFAULT_GIFS[defIdx].theme;savePrefs();}}
bool playOpen(const uint8_t *mem,int len,const char *path){if(mem)return gif.open((uint8_t*)mem,len,GIFDraw);if(!sdOk)return false;return gif.open(path,gifOpen,gifClose,gifRead,gifSeek,GIFDraw);}
bool playCurrent(){bool ok;if(useSd&&sdOk&&nparts>0)ok=playOpen(NULL,0,parts[idx].c_str());else ok=playOpen(DEFAULT_GIFS[defIdx].data,DEFAULT_GIFS[defIdx].len,NULL);if(!ok)return false;tft.fillScreen(TFT_BLACK);while(gif.playFrame(true,NULL)){server.handleClient();bool down=digitalRead(PIN_TOUCH)==HIGH;if(down&&!prevDown){downAt=millis();drawReact();playJingleMs(180);pendingReact=true;}if(!down&&prevDown){uint32_t held=millis()-downAt;if(held>=900){soundOn=!soundOn;savePrefs();}else{taps++;lastTap=millis();}prevDown=down;break;}prevDown=down;yield();}gif.close();brandMark();return true;}
void applyMenu(){if(menuRow==0){nextPart();ui=UI_PLAY;}else if(menuRow==1){playMode=(playMode=="acak")?"kategori":"acak";savePrefs();ui=UI_PLAY;}else if(menuRow==2){playJingleMs(800);}else if(menuRow==3){useSd=!useSd;if(useSd&&sdOk)scanTheme(theme);else useSd=false;savePrefs();}else if(menuRow==4){soundOn=!soundOn;savePrefs();}else if(menuRow==5){chronosOn=!chronosOn;savePrefs();}else if(menuRow==6){bootMark();}else ui=UI_PLAY;}
void finishTaps(){if(!taps||millis()-lastTap<=320)return;if(ui==UI_MENU){if(taps==1)menuRow=(menuRow+1)%NMENU;else applyMenu();}else{if(taps>=2){ui=UI_MENU;menuRow=0;drawMenu();}else pendingReact=false;}taps=0;}
void handleStatus(){JsonDocument d;d["brand"]=MOCHI_BRAND;d["theme"]=theme;d["mode"]=playMode;d["sound"]=soundOn;d["storage"]=(useSd&&sdOk)?"sd":"flash";d["sd"]=sdOk;d["def"]=defIdx;String s;serializeJson(d,s);server.send(200,"application/json",s);}
void handleSettings(){JsonDocument d;if(deserializeJson(d,server.arg("plain"))){server.send(400,"text/plain","bad");return;}if(d["theme"].is<const char*>())theme=(const char*)d["theme"];if(d["play_mode"].is<const char*>())playMode=(const char*)d["play_mode"];if(d["sound"].is<bool>())soundOn=d["sound"];if(d["chronos"].is<bool>())chronosOn=d["chronos"];if(d["watermark"].is<bool>())showWm=d["watermark"];if(d["storage"].is<const char*>())useSd=(String((const char*)d["storage"])=="sd");if(d["def"].is<int>())defIdx=d["def"];if(d["default_gif"].is<const char*>()){String want=(const char*)d["default_gif"];for(int i=0;i<DEFAULT_GIF_COUNT;i++)if(want==DEFAULT_GIFS[i].stem||want==DEFAULT_GIFS[i].theme)defIdx=i;}savePrefs();if(useSd)scanTheme(theme);server.send(200,"application/json","{\"ok\":true,\"brand\":\"rzmong\"}");}
void setup(){Serial.begin(115200);pinMode(PIN_TOUCH,INPUT_PULLDOWN);loadPrefs();tft.init();tft.setRotation(0);bootMark();SPI.begin(PIN_SD_SCK,PIN_SD_MISO,PIN_SD_MOSI,PIN_SD_CS);sdOk=SD.begin(PIN_SD_CS,SPI);if(sdOk)scanTheme(theme);if(useSd&&(!sdOk||nparts==0))useSd=false;audioInit();WiFi.softAP(MOCHI_AP_NAME,"rzmong24");server.on("/api/status",handleStatus);server.on("/api/settings",HTTP_POST,handleSettings);server.begin();if(chronosOn)watch.begin();}
void loop(){server.handleClient();if(chronosOn)watch.loop();bool down=digitalRead(PIN_TOUCH)==HIGH;if(ui==UI_MENU){if(down&&!prevDown)downAt=millis();if(!down&&prevDown){uint32_t held=millis()-downAt;if(held>=900){soundOn=!soundOn;savePrefs();}else{taps++;lastTap=millis();}}prevDown=down;finishTaps();drawMenu();delay(40);return;}finishTaps();playCurrent();}
