# 🍡 Paket SD Mochi rzmong

## Download pack penuh

**Release:** https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1  
**File:** [mochi-themes.zip](https://github.com/user-attachments/files/32840215/mochi-themes.zip) (84 GIF + 85 WAV)

Salin **isi zip** ke **akar kartu microSD (FAT32)**:

```text
/
├── themes.json
├── gif/
│   ├── wajah/     (35 GIF ekspresi)
│   ├── gundam/
│   ├── mobil/
│   ├── neon/
│   ├── anime/
│   ├── makanan/
│   ├── musik/
│   ├── intro/
│   └── polisi/
└── sfx/
    └── <tema yang sama>/*.wav   (WAV 16-bit PCM)
```

## Tema (9 kategori)
| ID | Label | Keterangan |
|----|-------|------------|
| wajah | Wajah Mochi | Ekspresi dasar (default) |
| gundam | Gundam / Mecha | Robot & kokpit |
| mobil | Mobil | Racing & GTR |
| neon | Neon | Glitch & cyber |
| anime | Anime | Nezuko, Tanjiro, dll |
| makanan | Makanan | Banana, cookie, sushi |
| musik | Musik | Rainbow, stars, pong |
| intro | Intro | Title, dasai, keep_it_up |
| polisi | Polisi | Tema polisi |

## Reaksi sentuh (10) — juga di-embed flash
| Nama | GIF stem | SFX path |
|------|----------|----------|
| tickle | yelling | /sfx/wajah/yelling.wav |
| kedip | distracted_2 | /sfx/wajah/distracted_2.wav |
| cinta | dumb_love | /sfx/wajah/dumb_love.wav |
| marah | hadouken_hit | /sfx/gundam/hadouken_hit.wav |
| ketawa | awkward_laugh | /sfx/wajah/awkward_laugh.wav |
| nangis | crying_smile | /sfx/wajah/crying_smile.wav |
| ngantuk | keep_it_up | /sfx/intro/keep_it_up.wav |
| kaget | big_sneeze | /sfx/wajah/big_sneeze.wav |
| kedip-satu | blade | /sfx/gundam/blade.wav |
| cemberut | pinky | /sfx/anime/pinky.wav |

## Format
- **GIF** saja (240×240 disarankan). Bukan MP4.
- **SFX** = **WAV 16-bit PCM**. Bukan MP3.
- Speaker wajib lewat **MAX98357 I2S** (jangan GPIO langsung).
