// Mochi rzmong 0.4.7 — captive DNS + portal probes; upload + GIF/SFX pairs; AP rzmong mochi
#include <Arduino.h>
#include <TFT_eSPI.h>
#include <AnimatedGIF.h>
#include <SD.h>
#include <SPI.h>
#include <WiFi.h>
#include <WebServer.h>
#include <DNSServer.h>
#include <Preferences.h>
#include <ArduinoJson.h>
#include <ChronosESP32.h>
#include "driver/i2s.h"
#include "MochiRzmong.h"
#include "defaults_gif.h"
#include "jingle.h"
#include "captive_ui.h"

static const int W=240,H=240;
static const uint16_t C_BG=0x1082,C_BAR=0xFD20,C_SEL=0xFE60,C_TEXT=0xEF7D,C_DIM=0x8410;
static const uint16_t C_RED=0xF985,C_TEAL=0x07F4,C_BLUE=0x3C7F,C_PINK=0xF81F,C_YEL=0xFFE0;

TFT_eSPI tft; AnimatedGIF gif; WebServer server(80); DNSServer dnsServer; ChronosESP32 watch; Preferences prefs;
String theme="wajah", playMode="kategori", reactMode="acak", apPass=MOCHI_AP_PASS;
bool soundOn=true, useSd=false, chronosOn=false, showWm=true;
int defIdx=0, reactIdx=0, volume=12, rot=0, menuRow=0, menuTop=0;
String parts[32]; int nparts=0, idx=0;
bool sdOk=false, sdBusy=false, prevDown=false;
uint32_t downAt=0, lastTap=0; int taps=0;
enum { UI_PLAY=0, UI_MENU=1 }; int ui=UI_PLAY;

// --- remaining body injected from fixed file via path --- PLACEHOLDER
