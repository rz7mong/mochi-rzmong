// Mochi rzmong ST7789 240x240 — tema, sentuh, bisu, Chronos, watermark
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
#include "MochiRzmong.h"

static const int PIN_TOUCH = 1;
static const int PIN_SD_CS = 5;
static const int W = 240, H = 240;
TFT_eSPI tft; AnimatedGIF gif; WebServer server(80); ChronosESP32 watch; Preferences prefs;
String theme = "gundam", playMode = "kategori";
bool soundOn = true, musicOn = true, chronosOn = true, showWm = true;
static const char *THEMES[] = {"wajah","gundam","mobil","neon","anime","makanan","musik","intro"};
static const int NTHEME = 8;
String parts[32]; int nparts = 0, idx = 0; File gifFile; bool sdOk = false;
enum Ui { UI_PLAY, UI_MENU }; Ui ui = UI_PLAY; int menuRow = 0;
const char *MENU[] = {"Tema berikutnya","Mode acak","Musik /music","Bisu / bunyi","Chronos","Tentang rzmong","Tutup"};
const int NMENU = 7;

void loadPrefs(){prefs.begin("rzmong",false);theme=prefs.getString("theme","gundam");playMode=prefs.getString("mode","kategori");soundOn=prefs.getBool("sound",true);musicOn=prefs.getBool("music",true);chronosOn=prefs.getBool("chrono",true);showWm=prefs.getBool("wm",true);}
void savePrefs(){prefs.putString("theme",theme);prefs.putString("mode",playMode);prefs.putBool("sound",soundOn);prefs.putBool("music",musicOn);prefs.putBool("chrono",chronosOn);prefs.putBool("wm",showWm);}
void scanTheme(const String &t){nparts=0;String dir=String("/gif/")+t;File d=SD.open(dir);if(!d)return;while(true){File f=d.openNextFile();if(!f)break;String n=f.name();f.close();if(n.endsWith(".gif")&&n.indexOf("intro_full")<0&&nparts<32)parts[nparts++]=dir+"/"+n.substring(n.lastIndexOf('/')+1);}d.close();}
void GIFDraw(GIFDRAW *p){if(p->y>=H)return;uint16_t line[240];uint8_t *s=p->pPixels;int w=p->iWidth;if(w>W)w=W;for(int x=0;x<w;x++){uint8_t c=*s++;if(c==p->ucTransparent&&p->ucHasTransparency)continue;uint8_t *pal=(uint8_t*)p->pPalette+c*3;line[x]=tft.color565(pal[0],pal[1],pal[2]);}int y0=(H-p->iHeight)/2+p->iY+p->y;if(y0<0||y0>=H)return;tft.pushImage((W-p->iWidth)/2+p->iX,y0,w,1,line);}
void *gifOpen(const char *name,int32_t *sz){gifFile=SD.open(name);if(!gifFile)return NULL;*sz=gifFile.size();return (void*)1;}
void gifClose(void*){if(gifFile)gifFile.close();}
int32_t gifRead(GIFFILE *p,uint8_t *buf,int32_t len){int n=gifFile.read(buf,len);p->iPos=gifFile.position();return n;}
int32_t gifSeek(GIFFILE *p,int32_t pos){gifFile.seek(pos);p->iPos=gifFile.position();return p->iPos;}
void watermark(){if(!showWm)return;tft.setTextColor(tft.color565(90,90,100),TFT_BLACK);tft.drawString(MOCHI_WATERMARK,168,226,1);}
void bootMark(){tft.fillScreen(TFT_BLACK);tft.setTextColor(tft.color565(255,107,107),TFT_BLACK);tft.drawCentreString("Mochi rzmong",120,96,2);tft.setTextColor(tft.color565(140,150,160),TFT_BLACK);tft.drawCentreString(MOCHI_WATERMARK,120,128,1);delay(700);}
void drawMenu(){tft.fillScreen(TFT_BLACK);tft.setTextColor(tft.color565(255,107,107),TFT_BLACK);tft.drawString("menu rzmong",12,8,2);for(int i=0;i<NMENU;i++){tft.setTextColor(i==menuRow?tft.color565(29,209,161):tft.color565(200,205,214),TFT_BLACK);tft.drawString((i==menuRow?"> ":"  ")+String(MENU[i]),16,36+i*22,2);}watermark();}
bool playOne(const char *path){if(!sdOk)return false;if(gif.open(path,gifOpen,gifClose,gifRead,gifSeek,GIFDraw)){tft.fillScreen(TFT_BLACK);while(gif.playFrame(true,NULL)){if(digitalRead(PIN_TOUCH)==HIGH)break;yield();}gif.close();watermark();return true;}return false;}
void nextPart(){if(playMode=="acak"){theme=THEMES[random(NTHEME)];scanTheme(theme);}else if(playMode=="acak_tema"&&nparts>0){idx=random(nparts);return;}if(nparts==0)scanTheme(theme);if(nparts==0)return;idx=(idx+1)%nparts;}
void handleStatus(){JsonDocument d;d["brand"]=MOCHI_WATERMARK;d["theme"]=theme;d["mode"]=playMode;d["sound"]=soundOn;String s;serializeJson(d,s);server.send(200,"application/json",s);}
void handleSettings(){JsonDocument d;if(deserializeJson(d,server.arg("plain"))){server.send(400,"text/plain","bad");return;}if(d["theme"].is<const char*>())theme=(const char*)d["theme"];if(d["play_mode"].is<const char*>())playMode=(const char*)d["play_mode"];if(d["sound"].is<bool>())soundOn=d["sound"];if(d["music"].is<bool>())musicOn=d["music"];if(d["chronos"].is<bool>())chronosOn=d["chronos"];if(d["watermark"].is<bool>())showWm=d["watermark"];savePrefs();scanTheme(theme);server.send(200,"application/json","{\"ok\":true,\"brand\":\"rzmong\"}");}
void setup(){Serial.begin(115200);pinMode(PIN_TOUCH,INPUT_PULLDOWN);loadPrefs();tft.init();tft.setRotation(0);bootMark();sdOk=SD.begin(PIN_SD_CS);scanTheme(theme);WiFi.softAP("Mochi-rzmong","rzmong24");server.on("/api/status",handleStatus);server.on("/api/settings",HTTP_POST,handleSettings);server.begin();if(chronosOn)watch.begin();}
void loop(){server.handleClient();if(chronosOn)watch.loop();static uint32_t downAt=0,lastTap=0;static int taps=0;static bool prev=false;bool down=digitalRead(PIN_TOUCH)==HIGH;if(down&&!prev)downAt=millis();if(!down&&prev){uint32_t held=millis()-downAt;if(held>=900){soundOn=!soundOn;savePrefs();}else{taps++;lastTap=millis();}}prev=down;if(taps&&millis()-lastTap>320){if(ui==UI_MENU){if(taps==1)menuRow=(menuRow+1)%NMENU;else{if(menuRow==0){int i=0;for(;i<NTHEME;i++)if(theme==THEMES[i])break;theme=THEMES[(i+1)%NTHEME];scanTheme(theme);idx=0;ui=UI_PLAY;}else if(menuRow==1){playMode=(playMode=="acak")?"kategori":"acak";savePrefs();ui=UI_PLAY;}else if(menuRow==3){soundOn=!soundOn;savePrefs();}else if(menuRow==4){chronosOn=!chronosOn;savePrefs();}else if(menuRow==5){bootMark();delay(600);}else ui=UI_PLAY;}}else{if(taps>=2){ui=UI_MENU;menuRow=0;drawMenu();}else nextPart();}taps=0;}if(ui==UI_MENU){drawMenu();delay(80);return;}if(nparts>0)playOne(parts[idx].c_str());else{tft.fillScreen(TFT_BLACK);tft.drawCentreString("SD /gif ?",120,110,2);watermark();delay(400);}}
