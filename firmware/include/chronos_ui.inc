
// chronos_ui.inc — included from main.cpp after globals (ESP32-C3 Super Mini)
void drawChronosNotif(){
  tft.fillScreen(C_BG);
  tft.fillRect(0,0,240,36,C_TEAL);
  tft.setTextColor(TFT_BLACK,C_TEAL);
  tft.drawCentreString(notifApp.length()?notifApp.c_str():"Notifikasi",120,8,2);
  tft.setTextColor(C_TEXT,C_BG);
  tft.drawString(notifTitle,12,50,2);
  tft.setTextColor(C_DIM,C_BG);
  String m=notifMsg;
  if(m.length()>36){ tft.drawString(m.substring(0,36),12,80,1); tft.drawString(m.substring(36,72),12,96,1); }
  else tft.drawString(m,12,80,1);
  if(chronoConn){
    char tbuf[24]="--:--";
    String td=watch.getTimeDate();
    if(td.length()>=5) td.substring(0,5).toCharArray(tbuf,24);
    tft.drawCentreString(tbuf,120,210,2);
  }
}
void drawChronosRinger(){
  tft.fillScreen(C_BG);
  tft.fillRoundRect(20,60,200,100,16,C_RED);
  tft.setTextColor(TFT_WHITE,C_RED);
  tft.drawCentreString("Panggilan",120,80,2);
  tft.drawCentreString(ringerName.length()?ringerName.c_str():"...",120,110,2);
}
void onChronosConn(bool state){
  chronoConn=state;
  Serial.printf("[chronos] %s\n", state?"connected":"disconnected");
  if(state) watch.setBattery(100, false);
}
void onChronosNotif(Notification n){
  notifApp=n.app; if(notifApp.length()>22) notifApp=notifApp.substring(0,22);
  notifTitle=n.title; if(notifTitle.length()>28) notifTitle=notifTitle.substring(0,28);
  notifMsg=n.message; if(notifMsg.length()>72) notifMsg=notifMsg.substring(0,72);
  notifUntil=millis()+6000;
  playJingleMs(180);
}
void onChronosRinger(String caller, bool state){
  ringerOn=state;
  ringerName=caller; if(ringerName.length()>24) ringerName=ringerName.substring(0,24);
  if(state) playJingleMs(500);
}
void onChronosConfig(Config config, uint32_t a, uint32_t b){
  if(config==CF_FIND){
    playJingleMs(700);
    for(int i=0;i<3;i++){ tft.fillScreen(C_YEL); delay(120); tft.fillScreen(C_BG); delay(80); }
  } else if(config==CF_TIME){
    Serial.printf("[chronos] time %s\n", watch.getTimeDate().c_str());
  }
}
void chronosSetupCallbacks(){
  watch.setConnectionCallback(onChronosConn);
  watch.setNotificationCallback(onChronosNotif);
  watch.setRingerCallback(onChronosRinger);
  watch.setConfigurationCallback(onChronosConfig);
}
void chronosApply(){
  if(chronosOn){
    if(!watch.isRunning()){
      chronosSetupCallbacks();
      watch.begin();
      Serial.printf("[chronos] BLE on mac=%s\n", watch.getAddress().c_str());
    }
  } else {
    chronoConn=false; ringerOn=false; notifUntil=0;
    if(watch.isRunning()) watch.stop();
    Serial.println("[chronos] BLE off");
  }
}
