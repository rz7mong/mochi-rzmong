#pragma once
// Mochi rzmong — pustaka tema
// https://github.com/rz7mong/mochi-rzmong

#define MOCHI_BRAND   "rzmong"
#define MOCHI_WATERMARK MOCHI_BRAND
#define MOCHI_AP_NAME "Mochi-rzmong"
#define MOCHI_VERSION "0.1.0"

// SD: /themes.json /gif/<tema>/ /sfx/<tema>/ /music/*.mp3
// Tema: wajah, gundam, mobil, neon, anime, makanan, musik, intro
// Sentuh 1x = bagian; 2x = menu; tahan = bisu

struct MochiPart {
  const char *theme;
  const char *stem;
};
