#pragma once
// Pustaka Mochi rzmong 0.2.0
// https://github.com/rz7mong/mochi-rzmong

#define MOCHI_BRAND   "rzmong"
#define MOCHI_WATERMARK MOCHI_BRAND
#define MOCHI_AP_NAME "Mochi-rzmong"
#define MOCHI_VERSION "0.2.0"

#define MOCHI_PIN_TOUCH 1
#define MOCHI_PIN_SD_SCK 4
#define MOCHI_PIN_SD_MISO 2
#define MOCHI_PIN_SD_MOSI 6
#define MOCHI_PIN_SD_CS 5
#define MOCHI_PIN_I2S_BCLK 21
#define MOCHI_PIN_I2S_LRC 20
#define MOCHI_PIN_I2S_DIN 9

struct MochiPart { const char *theme; const char *stem; };

// Model reaksi sentuh (seperti banyak emote Dasai)
static const char *MOCHI_REACTS[] = {
  "tickle", "kedip", "cinta", "marah", "ketawa",
  "nangis", "ngantuk", "kaget", "kedip-satu", "cemberut"
};
static const int MOCHI_REACT_COUNT = 10;
static const char *MOCHI_REACT_FACE[] = {
  "o_o", "-_-", "<3", ">_<", "^_^",
  "T_T", "u_u", "O_O", "^_o", ":*"
};

static const char *MOCHI_THEMES[] = {
  "wajah","gundam","mobil","neon","anime","makanan","musik","intro"
};
static const int MOCHI_THEME_COUNT = 8;
