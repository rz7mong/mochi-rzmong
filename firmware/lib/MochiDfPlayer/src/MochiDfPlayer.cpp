#include "MochiDfPlayer.h"
#include <DFRobotDFPlayerMini.h>
#include <HardwareSerial.h>
#include "MochiRzmong.h"

/* Sama dengan firmware MAX98357, kecuali jalur suara.
 * GPIO20/21 di sana I2S. Di sini UART DFPlayer. Jangan pasang MAX98357.
 * RX modul <- GPIO20 lewat 1k. TX modul -> GPIO21. VCC modul = 5V.
 */
static const int DF_RX = 21;
static const int DF_TX = 20;
static const int DF_FOLDER_REACT = 1;
static const int DF_FOLDER_FACE = 2;

static HardwareSerial dfSerial(1);
static DFRobotDFPlayerMini dfPlayer;
static bool dfOk = false;
static uint32_t dfLastCmd = 0;

static void dfGap() {
  uint32_t now = millis();
  if (now - dfLastCmd < 80) delay(80 - (now - dfLastCmd));
  dfLastCmd = millis();
}

static int dfVol(int vol21) {
  if (vol21 < 0) vol21 = 0;
  if (vol21 > 21) vol21 = 21;
  return (vol21 * 30) / 21;
}

bool mochiDfInit() {
  dfSerial.begin(9600, SERIAL_8N1, DF_RX, DF_TX);
  delay(200);
  dfOk = dfPlayer.begin(dfSerial, false, false);
  if (!dfOk) {
    Serial.println("DFPlayer tidak jawab");
    return false;
  }
  dfPlayer.setTimeOut(500);
  dfPlayer.EQ(DFPLAYER_EQ_NORMAL);
  dfPlayer.outputDevice(DFPLAYER_DEVICE_SD);
  dfPlayer.volume(dfVol(12));
  Serial.println("DFPlayer siap");
  return true;
}

void mochiDfStop() {
  if (!dfOk) return;
  dfGap();
  dfPlayer.stop();
}

void mochiDfService() {}

void mochiDfSetVolume(int vol21, bool on) {
  if (!dfOk) return;
  dfGap();
  dfPlayer.volume(on ? dfVol(vol21) : 0);
  if (!on) dfPlayer.pause();
}

bool mochiDfPlayReact(int reactIndex) {
  if (!dfOk) return false;
  if (reactIndex < 0 || reactIndex >= MOCHI_REACT_COUNT) reactIndex = 0;
  dfGap();
  dfPlayer.playFolder(DF_FOLDER_REACT, reactIndex + 1);
  return true;
}

bool mochiDfPlayFace(int faceIndex) {
  if (!dfOk) return false;
  if (faceIndex < 0) faceIndex = 0;
  dfGap();
  dfPlayer.playFolder(DF_FOLDER_FACE, faceIndex + 1);
  return true;
}

bool mochiDfPlayGif(const char *gifPath) {
  if (!dfOk || !gifPath) return false;
  const char *slash = strrchr(gifPath, '/');
  const char *base = slash ? slash + 1 : gifPath;
  char stem[48];
  strncpy(stem, base, sizeof(stem) - 1);
  stem[sizeof(stem) - 1] = 0;
  char *dot = strrchr(stem, '.');
  if (dot) *dot = 0;
  for (int i = 0; i < MOCHI_REACT_COUNT; i++) {
    if (strcmp(stem, MOCHI_REACT[i].stem) == 0 || strcmp(stem, MOCHI_REACT[i].name) == 0)
      return mochiDfPlayReact(i);
  }
  return mochiDfPlayFace(0);
}
