# Pustaka Mochi rzmong

Versi **0.2.1**. Sertakan `MochiRzmong.h` di firmware.

## Reaksi sentuh

Sepuluh GIF reaksi disimpan di flash ESP32 (`DEFAULT_GIFS[]` / PROGMEM).

Urutan putar saat kepala disentuh:

1. Array flash `DEFAULT_GIFS[]`
2. Jika flash gagal dan SD ada: `/gif/<tema>/<stem>.gif`

| Nama | Tema | Stem |
| --- | --- | --- |
| tickle | wajah | yelling |
| kedip | wajah | distracted_2 |
| cinta | wajah | dumb_love |
| marah | gundam | hadouken_hit |
| ketawa | wajah | awkward_laugh |
| nangis | wajah | crying_smile |
| ngantuk | intro | keep_it_up |
| kaget | wajah | big_sneeze |
| kedip-satu | gundam | blade |
| cemberut | anime | pinky |

## Gestur

- Ketuk 1× = reaksi (bukan ganti GIF tema)
- Ketuk 2× = menu pengaturan
- Tahan 1 detik = bisu

## Compile

```bash
python firmware/tools/embed_assets.py
cd firmware
pio run -e esp32-c3-super-mini
```

Sumber berkas: `firmware/assets/react/` dan `firmware/tools/react_b64/`.
