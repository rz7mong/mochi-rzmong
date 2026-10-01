# 🍡 Paket SD Mochi rzmong

## 📦 Download pack penuh

**Hanya lewat GitHub Release (stabil):**  
https://github.com/rz7mong/mochi-rzmong/releases/tag/assets-v1

Unduh [`mochi-themes.zip`](https://github.com/rz7mong/mochi-rzmong/releases/download/assets-v1/mochi-themes.zip) dari halaman Release itu (86 GIF + 87 WAV).  
Hindari link `user-attachments` jangka panjang — bisa berubah.

Salin **isi zip** ke **akar kartu microSD (FAT32)**:

```text
/
├── themes.json
├── gif/<tema>/*.gif
└── sfx/<tema>/*.wav
```

## 🎨 Tema (9)
wajah · gundam · mobil · polisi · musik · neon · anime · makanan · intro

## 🆕 Update pack (2026-10-02, firmware 0.5.6)
Versi warna 8 fps: wajah/sleepy, smirk, raspberry, squint, angry_2 · musik/pong, rainbow · mobil/revs, headlights.
Baru: wajah/default (senyum + kedip), wajah/love_hearts_kiss, wajah/yawn_tired (+ WAV).

## 👆 Reaksi sentuh (11) — juga di flash
| Reaksi | GIF | SFX |
|--------|-----|-----|
| tickle | /gif/wajah/raspberry.gif | /sfx/wajah/raspberry.wav |
| kedip | /gif/wajah/squint.gif | /sfx/wajah/squint.wav |
| cinta | /gif/wajah/love_hearts_kiss.gif | /sfx/wajah/love_hearts_kiss.wav |
| marah | /gif/wajah/angry_2.gif | /sfx/wajah/angry_2.wav |
| ketawa | /gif/wajah/smirk.gif | /sfx/wajah/smirk.wav |
| ngantuk | /gif/wajah/sleepy.gif | /sfx/wajah/sleepy.wav |
| nguap | /gif/wajah/yawn_tired.gif | /sfx/wajah/yawn_tired.wav |
| pelangi | /gif/musik/rainbow.gif | /sfx/musik/rainbow.wav |
| pong | /gif/musik/pong.gif | /sfx/musik/pong.wav |
| ngebut | /gif/mobil/revs.gif | /sfx/mobil/revs.wav |
| hadouken | /gif/gundam/hadouken_hit.gif | /sfx/gundam/hadouken_hit.wav |

File di SD (tema+stem sama) didahulukan dari versi flash. Klip SD dipotong 1,6 dtk saat reaksi.

Format: **GIF** + **WAV 16-bit PCM**. Bukan MP3/MP4 di perangkat.
Speaker: **MAX98357 I2S** saja.
