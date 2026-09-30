# GIF reaksi untuk flash

Letakkan sepuluh berkas ini di folder ini agar tertanam ke memori ESP32 saat compile:

```text
yelling.gif
distracted_2.gif
dumb_love.gif
hadouken_hit.gif
awkward_laugh.gif
crying_smile.gif
keep_it_up.gif
big_sneeze.gif
blade.gif
pinky.gif
```

Perintah: `python firmware/tools/embed_assets.py`

Jika berkas tidak ada, skrip memakai cadangan yang digambar otomatis plus `firmware/tools/react_b64/yelling.gif.b64`.
