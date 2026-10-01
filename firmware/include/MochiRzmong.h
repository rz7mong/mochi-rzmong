#pragma once
#define MOCHI_BRAND   "rzmong"
#define MOCHI_WATERMARK MOCHI_BRAND
#define MOCHI_AP_NAME "rzmong mochi"
#ifndef MOCHI_AP_PASS  /* override: build_flags = -DMOCHI_AP_PASS=\"sandibaru123\" */
#define MOCHI_AP_PASS "rzmong123"
#endif
#define MOCHI_VERSION "0.5.4"
/* v0.5.4: default rotation 2 (180 deg) for the GMT130 LCD mounted pins-down in case/tatakan_GMT130_fit.stl.
 * v0.5.3: GIF RGB565 + canvas, tap window, Chronos preempt, SFX from reused RAM buffer.
 * AP name/pass unchanged. Override pass via build_flags only.
 */
#ifndef MOCHI_DEFAULT_ROTATION  /* 2 = LCD pin di bawah (tatakan GMT130). Tatakan lama / pin di atas: build_flags = -DMOCHI_DEFAULT_ROTATION=0 */
#define MOCHI_DEFAULT_ROTATION 2
#endif
#define MOCHI_ROT_LAYOUT 1  /* versi arah pasang LCD di NVS ("rotv"); naikkan jika default rotasi berubah lagi */
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
