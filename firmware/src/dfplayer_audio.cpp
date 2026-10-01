#include "MochiDfPlayer.h"

#if defined(MOCHI_AUDIO_DFPLAYER)
#include <DFRobotDFPlayerMini.h>
#include <HardwareSerial.h>

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
  return (vol21 * MOCHI_DF_VOLUME_MAX) / 21;
}

void dfAudioInit() {
  dfSerial.begin(9600, SERIAL_8N1, MOCHI_PIN_DF_RX, MOCHI_PIN_DF_TX);
  delay(200);
  dfOk = dfPlayer.begin(dfSerial, false, false);
  if (!dfOk) {
    Serial.println("DFPlayer tidak jawab. Cek 5V, GND, TX/RX, SD mp3.");
    return;
  }
  dfPlayer.setTimeOut(500);
  dfPlayer.EQ(DFPLAYER_EQ_NORMAL);
  dfPlayer.outputDevice(DFPLAYER_DEVICE_SD);
  dfPlayer.volume(dfVol(12));
  Serial.println("DFPlayer siap");
}

void dfStop() {
  if (!dfOk) return;
  dfGap();
  dfPlayer.stop();
}

void dfSetVolume(int vol21, bool on) {
  if (!dfOk) return;
  dfGap();
  dfPlayer.volume(on ? dfVol(vol21) : 0);
  if (!on) dfPlayer.pause();
}

bool dfPlayReact(int reactIndex) {
  if (!dfOk) return false;
  if (reactIndex < 0 || reactIndex >= MOCHI_REACT_COUNT) reactIndex = 0;
  dfGap();
  dfPlayer.playFolder(MOCHI_DF_FOLDER_REACT, reactIndex + 1);
  return true;
}

bool dfPlayFace(int faceIndex) {
  if (!dfOk) return false;
  if (faceIndex < 0) faceIndex = 0;
  dfGap();
  dfPlayer.playFolder(MOCHI_DF_FOLDER_FACE, faceIndex + 1);
  return true;
}

bool dfPlayGif(const char *gifPath) {
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
      return dfPlayReact(i);
  }
  return dfPlayFace(0);
}
#else
void dfAudioInit() {}
void dfStop() {}
void dfSetVolume(int, bool) {}
bool dfPlayReact(int) { return false; }
bool dfPlayFace(int) { return false; }
bool dfPlayGif(const char *) { return false; }
#endif
