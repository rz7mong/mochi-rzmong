// Mochi rzmong 0.2.9 — sdBusy SPI guard; AP rzmong mochi / rzmong123
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

static const int W=240,H=240;
static const uint16_t C_BG=0x1082,C_BAR=0xFD20,C_SEL=0xFE60,C_TEXT=0xEF7D,C_DIM=0x8410;
static const uint16_t C_RED=0xF985,C_TEAL=0x07F4,C_BLUE=0x3C7F,C_PINK=0xF81F,C_YEL=0xFFE0;

TFT_eSPI tft; AnimatedGIF gif; WebServer server(80); ChronosESP32 watch; Preferences prefs;
String theme="wajah", playMode="kategori", reactMode="acak", apPass=MOCHI_AP_PASS;
bool soundOn=true, useSd=false, chronosOn=false, showWm=true;
int defIdx=0, reactIdx=0, volume=12, rot=0, menuRow=0, menuTop=0;
String parts[32]; int nparts=0, idx=0; File gifFile; bool sdOk=false, i2sOk=false, sdBusy=false;
enum Ui { UI_PLAY, UI_MENU }; Ui ui=UI_PLAY;
uint32_t downAt=0,lastTap=0; int taps=0; bool prevDown=false;

struct MenuItem { const char *icon; const char *label; uint16_t col; };
static const MenuItem MENU[] = {
  {">","GIF berikutnya",C_TEAL},{"T","Pilih tema",C_BAR},{"E","Ekspresi flash",C_PINK},
  {"M","Mode putar",C_YEL},{"R","Reaksi acak/tetap",C_BLUE},{"F","Model reaksi",C_PINK},
  {"S","Sumber SD/Flash",C_BLUE},{"+","Volume +",C_TEAL},{"-","Volume -",C_TEAL},
  {"x","Bisu / bunyi",C_RED},{"O","Rotasi layar",C_YEL},{"C","Chronos",C_TEAL},
  {"W","Merek LCD",C_DIM},{"A","Info Wi-Fi AP",C_BLUE},{"i","Tentang rzmong",C_TEXT},{"<","Tutup",C_DIM}
};
static const int NMENU=16, VIS=7;

void loadPrefs(){
  prefs.begin("rzmong",false);
  theme=prefs.getString("theme","wajah"); playMode=prefs.getString("mode","kategori");
  reactMode=prefs.getString("rmode","acak"); soundOn=prefs.getBool("sound",true);
  useSd=prefs.getBool("usesd",false); chronosOn=prefs.getBool("chrono",false); showWm=prefs.getBool("wm",true);
  defIdx=prefs.getInt("def",0); reactIdx=prefs.getInt("react",0); volume=prefs.getInt("vol",12); rot=prefs.getInt("rot",0);
  if(defIdx<0||defIdx>=DEFAULT_GIF_COUNT)defIdx=0;
  if(reactIdx<0||reactIdx>=MOCHI_REACT_COUNT)reactIdx=0;
  if(volume<0)volume=0; if(volume>21)volume=21;
}
void savePrefs(){
  prefs.putString("theme",theme); prefs.putString("mode",playMode); prefs.putString("rmode",reactMode);
  prefs.putBool("sound",soundOn); prefs.putBool("usesd",useSd); prefs.putBool("chrono",chronosOn); prefs.putBool("wm",showWm);
  prefs.putInt("def",defIdx); prefs.putInt("react",reactIdx); prefs.putInt("vol",volume); prefs.putInt("rot",rot);
}
void scanTheme(const String &t){
  nparts=0; if(!sdOk||sdBusy)return;
  String dir=String("/gif/")+t; File d=SD.open(dir); if(!d)return;
  while(true){File f=d.openNextFile(); if(!f)break; String n=f.name(); f.close();
    if(n.endsWith(".gif")&&nparts<32){int sl=n.lastIndexOf('/'); parts[nparts++]=dir+"/"+n.substring(sl<0?0:sl+1);}}
  d.close();
}
void GIFDraw(GIFDRAW *p){
  if(p->y>=H)return; uint16_t line[240]; uint8_t *s=p->pPixels; int w=p->iWidth; if(w>W)w=W;
  for(int x=0;x<w;x++){uint8_t c=*s++; if(p->ucHasTransparency&&c==p->ucTransparent){line[x]=TFT_BLACK;continue;}
    uint8_t *pal=(uint8_t*)p->pPalette+c*3; line[x]=tft.color565(pal[0],pal[1],pal[2]);}
  int y0=(H-p->iHeight)/2+p->iY+p->y; if(y0<0||y0>=H)return;
  tft.pushImage((W-p->iWidth)/2+p->iX,y0,w,1,line);
}
void *gifOpen(const char *name,int32_t *sz){gifFile=SD.open(name); if(!gifFile)return NULL; *sz=gifFile.size(); return (void*)1;}
void gifClose(void*){if(gifFile)gifFile.close();}
int32_t gifRead(GIFFILE *p,uint8_t *buf,int32_t len){int n=gifFile.read(buf,len); p->iPos=gifFile.position(); return n;}
int32_t gifSeek(GIFFILE *p,int32_t pos){gifFile.seek(pos); p->iPos=gifFile.position(); return p->iPos;}

void audioInit(){
  i2s_config_t cfg={.mode=(i2s_mode_t)(I2S_MODE_MASTER|I2S_MODE_TX),.sample_rate=JINGLE_SR,.bits_per_sample=I2S_BITS_PER_SAMPLE_16BIT,.channel_format=I2S_CHANNEL_FMT_ONLY_LEFT,.communication_format=I2S_COMM_FORMAT_STAND_I2S,.intr_alloc_flags=0,.dma_buf_count=8,.dma_buf_len=256,.use_apll=false,.tx_desc_auto_clear=true,.fixed_mclk=0};
  if(i2s_driver_install(I2S_NUM_0,&cfg,0,NULL)!=ESP_OK)return;
  i2s_pin_config_t pins={.mck_io_num=I2S_PIN_NO_CHANGE,.bck_io_num=MOCHI_PIN_I2S_BCLK,.ws_io_num=MOCHI_PIN_I2S_LRC,.data_out_num=MOCHI_PIN_I2S_DIN,.data_in_num=I2S_PIN_NO_CHANGE};
  if(i2s_set_pin(I2S_NUM_0,&pins)!=ESP_OK)return; i2sOk=true;
}

void playJingleMs(int ms){
  if(!soundOn||!i2sOk)return;
  i2s_set_sample_rates(I2S_NUM_0, JINGLE_SR);
  int bytes=JINGLE_SR*2*ms/1000; if(bytes>JINGLE_PCM_LEN)bytes=JINGLE_PCM_LEN; if(bytes<2)bytes=2;
  int16_t buf[256]; int off=0;
  while(off<bytes){
    int n=bytes-off; if(n>512)n=512; int samples=n/2;
    const int16_t *src=(const int16_t*)(JINGLE_PCM+off);
    for(int i=0;i<samples;i++){ int v=(int)src[i]*(volume+1)/22; if(v>32767)v=32767; if(v<-32768)v=-32768; buf[i]=(int16_t)v; }
    size_t wr=0; i2s_write(I2S_NUM_0,buf,(size_t)samples*2,&wr,pdMS_TO_TICKS(200)); off+=n;
  }
}

bool playWavFromSd(const char *path){
  if(!soundOn||!i2sOk||!sdOk||sdBusy) return false;
  sdBusy=true;
  File f=SD.open(path); if(!f){sdBusy=false; return false;}
  uint8_t hdr[44];
  if(f.read(hdr,12)<12){f.close(); sdBusy=false; return false;}
  if(memcmp(hdr,"RIFF",4)!=0||memcmp(hdr+8,"WAVE",4)!=0){f.close(); sdBusy=false; return false;}
  uint16_t audioFormat=1, channels=1, bits=16;
  uint32_t sampleRate=22050, dataSize=0;
  bool gotFmt=false, gotData=false;
  while(f.available()){
    uint8_t ch[8]; if(f.read(ch,8)<8) break;
    uint32_t sz=ch[4]|(ch[5]<<8)|(ch[6]<<16)|(ch[7]<<24);
    if(memcmp(ch,"fmt ",4)==0){
      uint8_t fmt[16]; int need=sz>16?16:(int)sz;
      if(f.read(fmt,need)<need){f.close(); sdBusy=false; return false;}
      if(sz>(uint32_t)need) f.seek(f.position()+(sz-need));
      audioFormat=fmt[0]|(fmt[1]<<8); channels=fmt[2]|(fmt[3]<<8);
      sampleRate=fmt[4]|(fmt[5]<<8)|(fmt[6]<<16)|(fmt[7]<<24); bits=fmt[14]|(fmt[15]<<8); gotFmt=true;
    } else if(memcmp(ch,"data",4)==0){ dataSize=sz; gotData=true; break; }
    else f.seek(f.position()+sz);
  }
  if(!gotFmt||!gotData||audioFormat!=1||bits!=16||channels<1||channels>2){f.close(); sdBusy=false; return false;}
  if(sampleRate<8000) sampleRate=8000; if(sampleRate>48000) sampleRate=48000;
  i2s_set_sample_rates(I2S_NUM_0, sampleRate);
  const size_t CHUNK=512; uint8_t raw[CHUNK]; int16_t out[CHUNK];
  uint32_t left=dataSize; uint32_t t0=millis();
  while(left>0 && f.available()){
    size_t n=left>CHUNK?CHUNK:left; int rd=f.read(raw,n); if(rd<=0) break;
    int samples=rd/2; int16_t *src=(int16_t*)raw; int outN=0;
    if(channels==2){ for(int i=0;i+1<samples;i+=2){ int v=((int)src[i]+(int)src[i+1])/2; v=v*(volume+1)/22; if(v>32767)v=32767; if(v<-32768)v=-32768; out[outN++]=(int16_t)v; } }
    else { for(int i=0;i<samples;i++){ int v=(int)src[i]*(volume+1)/22; if(v>32767)v=32767; if(v<-32768)v=-32768; out[outN++]=(int16_t)v; } }
    size_t wr=0; if(outN>0) i2s_write(I2S_NUM_0,out,(size_t)outN*2,&wr,pdMS_TO_TICKS(300));
    left-=(uint32_t)rd; if(millis()-t0>4000) break; yield();
  }
  f.close(); sdBusy=false; i2s_set_sample_rates(I2S_NUM_0, JINGLE_SR); return true;
}

bool playSfxForReact(int r){
  if(!soundOn||!i2sOk) return false;
  if(r<0||r>=MOCHI_REACT_COUNT) r=0;
  const char *themeR=MOCHI_REACT[r].theme; const char *stem=MOCHI_REACT[r].stem; const char *name=MOCHI_REACT[r].name;
  if(sdOk){
    char path[96];
    snprintf(path,sizeof(path),"/sfx/%s/%s.wav",themeR,stem);
    if(SD.exists(path) && playWavFromSd(path)) return true;
    snprintf(path,sizeof(path),"/sfx/%s.wav",stem);
    if(SD.exists(path) && playWavFromSd(path)) return true;
    snprintf(path,sizeof(path),"/sfx/%s.wav",name);
    if(SD.exists(path) && playWavFromSd(path)) return true;
  }
  playJingleMs(220); return true;
}

int pickReact(){ return (reactMode=="acak") ? random(MOCHI_REACT_COUNT) : reactIdx; }
bool playOpen(const uint8_t *mem,int len,const char *path){
  if(mem) return gif.open((uint8_t*)mem,len,GIFDraw);
  if(!sdOk) return false;
  return gif.open(path,gifOpen,gifClose,gifRead,gifSeek,GIFDraw);
}
void playReactGif(){
  int r=pickReact(); playSfxForReact(r);
  String path=String("/gif/")+MOCHI_REACT[r].theme+"/"+MOCHI_REACT[r].stem+".gif";
  bool ok=false;
  if(sdOk && !sdBusy && SD.exists(path.c_str())){ sdBusy=true; ok=playOpen(NULL,0,path.c_str()); if(!ok) sdBusy=false; }
  if(!ok){ for(int i=0;i<DEFAULT_GIF_COUNT;i++){ if(strcmp(DEFAULT_GIFS[i].stem,MOCHI_REACT[r].stem)==0){ ok=playOpen(DEFAULT_GIFS[i].data,DEFAULT_GIFS[i].len,NULL); break; } } }
  if(!ok){ sdBusy=false; return; }
  tft.fillScreen(TFT_BLACK); uint32_t t0=millis();
  while(gif.playFrame(true,NULL)){ server.handleClient(); if(millis()-t0>1600) break; yield(); }
  gif.close(); sdBusy=false;
}
void brandMark(){if(!showWm)return; tft.setTextColor(C_DIM,TFT_BLACK); tft.drawString(MOCHI_BRAND,168,226,1);}
void bootMark(){
  tft.fillScreen(C_BG); tft.fillRoundRect(20,80,200,80,16,C_BAR);
  tft.setTextColor(TFT_BLACK,C_BAR); tft.drawCentreString("Mochi",120,96,4); tft.drawCentreString(MOCHI_BRAND,120,128,2); delay(400);
}
void drawMenu(){
  if(menuRow<menuTop) menuTop=menuRow; if(menuRow>=menuTop+VIS) menuTop=menuRow-VIS+1;
  tft.fillScreen(C_BG); tft.fillRect(0,0,240,34,C_BAR);
  tft.setTextColor(TFT_BLACK,C_BAR); tft.drawCentreString("PENGATURAN",120,4,2); tft.drawCentreString("rzmong",120,20,1);
  for(int i=0;i<VIS;i++){
    int id=menuTop+i; if(id>=NMENU)break; int y=40+i*26;
    if(id==menuRow){tft.fillRoundRect(6,y-2,228,25,6,C_SEL); tft.fillCircle(20,y+10,7,MENU[id].col); tft.setTextColor(TFT_BLACK,C_SEL);}
    else {tft.fillCircle(20,y+10,6,MENU[id].col); tft.setTextColor(C_TEXT,C_BG);}
    tft.drawString(String(MENU[id].icon)+" "+MENU[id].label,34,y+4,2);
  }
  tft.setTextColor(C_DIM,C_BG);
  char foot[56]; snprintf(foot,56,"%d/%d vol%d %s",menuRow+1,NMENU,volume,useSd&&sdOk?"SD":"flash");
  tft.drawString(foot,10,224,1);
}
void nextPart(){
  if(useSd&&sdOk){
    if(playMode=="acak"){theme=MOCHI_THEMES[random(MOCHI_THEME_COUNT)]; scanTheme(theme);}
    if(nparts==0)scanTheme(theme); if(nparts==0){useSd=false;return;}
    idx=(playMode=="acak_tema")?random(nparts):(idx+1)%nparts;
  } else { defIdx=(defIdx+1)%DEFAULT_GIF_COUNT; theme=DEFAULT_GIFS[defIdx].theme; savePrefs(); }
}
void showInfo(const char *a,const char *b){
  tft.fillScreen(C_BG); tft.fillRoundRect(16,70,208,100,14,C_SEL);
  tft.setTextColor(TFT_BLACK,C_SEL); tft.drawCentreString(a,120,90,2); tft.drawCentreString(b,120,118,2); delay(800);
}
void applyMenu(){
  if(menuRow==0){nextPart(); ui=UI_PLAY;}
  else if(menuRow==1){
    int i=0; for(;i<MOCHI_THEME_COUNT;i++) if(theme==MOCHI_THEMES[i]) break;
    theme=MOCHI_THEMES[(i+1)%MOCHI_THEME_COUNT];
    if(sdOk){ useSd=true; scanTheme(theme); idx=0; } savePrefs();
    if(sdOk && nparts>0) showInfo(theme.c_str(), (String(nparts)+" GIF").c_str());
    else if(sdOk) showInfo(theme.c_str(),"kosong di SD"); else showInfo(theme.c_str(),"default (no SD)");
  }
  else if(menuRow==2){defIdx=(defIdx+1)%DEFAULT_GIF_COUNT; savePrefs(); showInfo("ekspresi",DEFAULT_GIFS[defIdx].stem);}
  else if(menuRow==3){playMode=(playMode=="kategori")?"acak":(playMode=="acak"?"acak_tema":"kategori"); savePrefs(); showInfo("mode",playMode.c_str());}
  else if(menuRow==4){reactMode=(reactMode=="acak")?"tetap":"acak"; savePrefs(); showInfo("reaksi",reactMode.c_str());}
  else if(menuRow==5){reactIdx=(reactIdx+1)%MOCHI_REACT_COUNT; reactMode="tetap"; savePrefs(); showInfo(MOCHI_REACT[reactIdx].name,MOCHI_REACT[reactIdx].stem);}
  else if(menuRow==6){useSd=!useSd; if(useSd&&sdOk)scanTheme(theme); else useSd=false; savePrefs(); showInfo("sumber",useSd?"SD":"flash");}
  else if(menuRow==7){if(volume<21)volume++; savePrefs(); showInfo("volume",String(volume).c_str()); playJingleMs(120);}
  else if(menuRow==8){if(volume>0)volume--; savePrefs(); showInfo("volume",String(volume).c_str()); playJingleMs(120);}
  else if(menuRow==9){soundOn=!soundOn; savePrefs(); showInfo("suara",soundOn?"ON":"BISU");}
  else if(menuRow==10){rot=(rot+1)&3; tft.setRotation(rot); savePrefs();}
  else if(menuRow==11){chronosOn=!chronosOn; savePrefs(); showInfo("chronos",chronosOn?"ON":"OFF");}
  else if(menuRow==12){showWm=!showWm; savePrefs();}
  else if(menuRow==13){showInfo(MOCHI_AP_NAME, MOCHI_AP_PASS);}
  else if(menuRow==14){bootMark();}
  else ui=UI_PLAY;
}
void finishTaps(){
  if(!taps||millis()-lastTap<=320)return;
  if(ui==UI_MENU){ if(taps==1) menuRow=(menuRow+1)%NMENU; else applyMenu(); }
  else { if(taps>=2){ui=UI_MENU; menuRow=0; menuTop=0; drawMenu();} }
  taps=0;
}
bool playCurrent(){
  bool ok;
  bool fromSd=useSd&&sdOk&&nparts>0;
  if(fromSd){ sdBusy=true; ok=playOpen(NULL,0,parts[idx].c_str()); }
  else ok=playOpen(DEFAULT_GIFS[defIdx].data,DEFAULT_GIFS[defIdx].len,NULL);
  if(!ok){ sdBusy=false; return false; }
  tft.fillScreen(TFT_BLACK);
  while(gif.playFrame(true,NULL)){
    server.handleClient();
    bool down=digitalRead(MOCHI_PIN_TOUCH)==HIGH;
    if(down&&!prevDown){
      downAt=millis(); gif.close(); sdBusy=false;
      playReactGif(); prevDown=true; return true;
    }
    if(!down&&prevDown){
      uint32_t held=millis()-downAt;
      if(held>=900){soundOn=!soundOn; savePrefs();} else {taps++; lastTap=millis();}
      prevDown=down; break;
    }
    prevDown=down; yield();
  }
  gif.close(); sdBusy=false; brandMark(); return true;
}
void handleStatus(){
  JsonDocument d; d["brand"]=MOCHI_BRAND; d["ver"]=MOCHI_VERSION; d["theme"]=theme;
  d["mode"]=playMode; d["react_mode"]=reactMode; d["react"]=MOCHI_REACT[reactIdx].name;
  d["react_idx"]=reactIdx;
  d["react_gif"]=String("/gif/")+MOCHI_REACT[reactIdx].theme+"/"+MOCHI_REACT[reactIdx].stem+".gif";
  d["sound"]=soundOn; d["vol"]=volume; d["storage"]=(useSd&&sdOk)?"sd":"flash"; d["sd"]=sdOk;
  d["sfx"]="wav_sd_or_jingle"; d["def"]=defIdx; d["gif_count"]=nparts;
  d["ap_ssid"]=MOCHI_AP_NAME; d["ap_pass"]=MOCHI_AP_PASS; d["sd_busy"]=sdBusy;
  JsonArray themes=d["themes"].to<JsonArray>();
  for(int i=0;i<MOCHI_THEME_COUNT;i++) themes.add(MOCHI_THEMES[i]);
  String s; serializeJson(d,s); server.send(200,"application/json",s);
}
void handleThemes(){
  if(sdBusy){server.send(503,"application/json","{\"error\":\"sd_busy\"}");return;}
  JsonDocument d; d["sd"]=sdOk; d["current"]=theme; d["storage"]=(useSd&&sdOk)?"sd":"flash";
  JsonArray arr=d["themes"].to<JsonArray>();
  for(int i=0;i<MOCHI_THEME_COUNT;i++){
    JsonObject o=arr.add<JsonObject>(); o["id"]=MOCHI_THEMES[i]; int cnt=0;
    if(sdOk){ String dir=String("/gif/")+MOCHI_THEMES[i]; File dd=SD.open(dir);
      if(dd){ while(true){File f=dd.openNextFile(); if(!f)break; String n=f.name(); f.close(); if(n.endsWith(".gif")) cnt++; } dd.close(); }
    }
    o["gif_count"]=cnt; o["available"]=(cnt>0)||(!sdOk && i==0);
  }
  String s; serializeJson(d,s); server.send(200,"application/json",s);
}
void handleSettings(){
  JsonDocument d; if(deserializeJson(d,server.arg("plain"))){server.send(400,"text/plain","bad");return;}
  if(d["theme"].is<const char*>()) theme=(const char*)d["theme"];
  if(d["play_mode"].is<const char*>()) playMode=(const char*)d["play_mode"];
  if(d["react_mode"].is<const char*>()) reactMode=(const char*)d["react_mode"];
  if(d["sound"].is<bool>()) soundOn=d["sound"];
  if(d["chronos"].is<bool>()) chronosOn=d["chronos"];
  if(d["watermark"].is<bool>()) showWm=d["watermark"];
  if(d["storage"].is<const char*>()) useSd=(String((const char*)d["storage"])=="sd");
  if(d["def"].is<int>()){ defIdx=d["def"]; if(defIdx<0||defIdx>=DEFAULT_GIF_COUNT) defIdx=0; }
  if(d["react"].is<int>()){ reactIdx=d["react"]; if(reactIdx<0||reactIdx>=MOCHI_REACT_COUNT) reactIdx=0; }
  if(d["volume"].is<int>()){ volume=d["volume"]; if(volume<0)volume=0; if(volume>21)volume=21; }
  if(sdOk && d["theme"].is<const char*>() && !d["storage"].is<const char*>()) useSd=true;
  if(useSd && !sdOk) useSd=false;
  savePrefs(); if(useSd && sdOk && !sdBusy){ scanTheme(theme); idx=0; }
  JsonDocument out; out["ok"]=true; out["brand"]=MOCHI_BRAND; out["theme"]=theme;
  out["storage"]=(useSd&&sdOk)?"sd":"flash"; out["gif_count"]=nparts; out["sd"]=sdOk; out["ap_pass"]=MOCHI_AP_PASS;
  String s; serializeJson(out,s); server.send(200,"application/json",s);
}
void setup(){
  Serial.begin(115200); pinMode(MOCHI_PIN_TOUCH,INPUT_PULLDOWN); loadPrefs();
  tft.init(); tft.setRotation(rot); bootMark();
  SPI.begin(MOCHI_PIN_SD_SCK,MOCHI_PIN_SD_MISO,MOCHI_PIN_SD_MOSI,MOCHI_PIN_SD_CS);
  sdOk=SD.begin(MOCHI_PIN_SD_CS,SPI); if(sdOk) scanTheme(theme);
  if(useSd&&(!sdOk||nparts==0)) useSd=false;
  audioInit();
  apPass = MOCHI_AP_PASS;
  WiFi.softAP(MOCHI_AP_NAME, MOCHI_AP_PASS);
  server.on("/api/status",handleStatus); server.on("/api/themes",handleThemes); server.on("/api/settings",HTTP_POST,handleSettings); server.begin();
  if(chronosOn) watch.begin();
}
void loop(){
  server.handleClient(); if(chronosOn) watch.loop();
  bool down=digitalRead(MOCHI_PIN_TOUCH)==HIGH;
  if(ui==UI_MENU){
    if(down&&!prevDown) downAt=millis();
    if(!down&&prevDown){ uint32_t held=millis()-downAt; if(held>=900){soundOn=!soundOn;savePrefs();} else {taps++; lastTap=millis();} }
    prevDown=down; finishTaps(); drawMenu(); delay(35); return;
  }
  finishTaps(); playCurrent();
}
