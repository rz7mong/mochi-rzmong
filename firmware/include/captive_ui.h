#pragma once
// Served at http://192.168.4.1/ — offline settings (no mixed content)
static const char CAPTIVE_HTML[] PROGMEM = R"MOCHI(
<!DOCTYPE html><html lang=id><head>
<meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Mochi rzmong</title>
<style>
body{font-family:system-ui,sans-serif;background:#0e1116;color:#eef2f7;margin:16px;max-width:420px}
h1{font-size:22px;margin:0 0 8px}h2{font-size:15px;margin:16px 0 8px;color:#8b95a7}
.card{background:#171b22;border:1px solid #2a3140;border-radius:12px;padding:14px;margin:10px 0}
label{display:block;font-size:12px;color:#8b95a7;margin:8px 0 4px}
input,select{width:100%;padding:10px;border-radius:8px;border:1px solid #2a3140;background:#10141b;color:#eef2f7;box-sizing:border-box}
button{background:#ff6b6b;color:#fff;border:0;border-radius:8px;padding:10px 14px;margin:6px 4px 0 0;cursor:pointer}
#st{font-size:13px;color:#50fa7b;margin-top:8px}.hint{font-size:12px;color:#8b95a7;line-height:1.4}
a{color:#54a0ff}
</style></head><body>
<h1>Mochi rzmong</h1>
<p class=hint>AP offline · v dari /api/status · Studio convert di GitHub Pages (butuh internet)</p>
<div class=card>
<label>Tema</label><select id=theme></select>
<label>Sumber</label><select id=storage><option value=flash>Flash</option><option value=sd>SD</option></select>
<label>Mode putar</label><select id=mode><option value=kategori>Kategori</option><option value=acak>Acak</option><option value=acak_tema>Acak tema</option></select>
<label>Reaksi</label><select id=rmode><option value=acak>Acak</option><option value=tetap>Tetap</option></select>
<label>Volume 0-21</label><input id=vol type=number min=0 max=21 value=12>
<label><input id=sound type=checkbox checked> SFX on</label>
<p id=st></p>
<button type=button onclick=load()>Muat</button>
<button type=button onclick=save()>Simpan</button>
</div>
<p class=hint>Upload GIF/WAV: sambung AP + buka Studio di HP yang masih punya internet, atau salin ke SD manual (/gif/tema/ /sfx/tema/).</p>
<script>
const T=['wajah','gundam','mobil','polisi','musik','neon','anime','makanan','intro'];
const ts=document.getElementById('theme');T.forEach(t=>{const o=document.createElement('option');o.value=t;o.textContent=t;ts.appendChild(o);});
async function load(){try{const j=await(await fetch('/api/status')).json();
if(j.theme)ts.value=j.theme;if(j.storage)document.getElementById('storage').value=j.storage;
if(j.mode)document.getElementById('mode').value=j.mode;if(j.react_mode)document.getElementById('rmode').value=j.react_mode;
if(typeof j.vol==='number')document.getElementById('vol').value=j.vol;
if(typeof j.sound==='boolean')document.getElementById('sound').checked=j.sound;
document.getElementById('st').textContent='v'+(j.ver||'?')+' · '+(j.ap_ssid||'')+' / '+(j.ap_pass||'');
}catch(e){document.getElementById('st').textContent='Gagal muat';}}
async function save(){const body={theme:ts.value,storage:document.getElementById('storage').value,play_mode:document.getElementById('mode').value,react_mode:document.getElementById('rmode').value,volume:+document.getElementById('vol').value,sound:document.getElementById('sound').checked};
try{const r=await fetch('/api/settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
document.getElementById('st').textContent=r.ok?'Tersimpan':'Gagal';}catch(e){document.getElementById('st').textContent='Offline';}}
load();
</script></body></html>
)MOCHI";
