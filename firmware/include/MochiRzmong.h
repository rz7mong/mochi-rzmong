#pragma once
#define MOCHI_BRAND   "rzmong"
#define MOCHI_WATERMARK MOCHI_BRAND
#define MOCHI_AP_NAME "rzmong mochi"
#define MOCHI_AP_PASS "rzmong123"
#define MOCHI_VERSION "0.5.0"
/* Chronos: BLE name rzmong · pair via Chronos app (not system BT).
 * ESP32-C3 shares 2.4GHz radio with Wi-Fi AP — expect lag if both busy.
 */
#define MOCHI_PIN_TOUCH 1
#define MOCHI_PIN_SD_SCK 4
#define MOCHI_PIN_SD_MISO 3
#define MOCHI_PIN_SD_MOSI 6
#define MOCHI_PIN_SD_CS 5
#define MOCHI_PIN_I2S_BCLK 21
#define MOCHI_PIN_I2S_LRC 20
#define MOCHI_PIN_I2S_DIN 8
struct MochiPart { const char *theme; const char *stem; };
struct MochiReact { const char *name; const char *theme; const char *stem; };
static const MochiReact MOCHI_REACT[] = {
  {"tickle","wajah","yelling"},
  {"kedip","wajah","distracted_2"},
  {"cinta","wajah","dumb_love"},
  {"marah","gundam","hadouken_hit"},
  {"ketawa","wajah","awkward_laugh"},
  {"nangis","wajah","crying_smile"},
  {"ngantuk","intro","keep_it_up"},
  {"kaget","wajah","big_sneeze"},
  {"kedip-satu","gundam","blade"},
  {"cemberut","anime","pinky"}
};
static const int MOCHI_REACT_COUNT = 10;
static const char *MOCHI_THEMES[] = {
  "wajah","gundam","mobil","polisi","musik","neon","anime","makanan","intro"
};
static const int MOCHI_THEME_COUNT = 9;
