#pragma once
#define MOCHI_BRAND   "rzmong"
#define MOCHI_WATERMARK MOCHI_BRAND
#define MOCHI_AP_NAME "Mochi-rzmong"
#define MOCHI_VERSION "0.2.3"
/* Pin map v0.2.3 — boot-safe for ESP32-C3
 * Strapping pins: GPIO2, GPIO8, GPIO9
 * Free: GPIO2, GPIO9 (BOOT). Only GPIO8 used (I2S DIN, high-Z at reset).
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
static const char *MOCHI_THEMES[] = {"wajah","gundam","mobil","neon","anime","makanan","musik","intro"};
static const int MOCHI_THEME_COUNT = 8;
