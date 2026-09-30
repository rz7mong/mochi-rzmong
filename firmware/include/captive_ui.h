#pragma once
// Served at http://192.168.4.1/ — offline settings + Chronos
static const char CAPTIVE_HTML[] PROGMEM = R"MOCHI(
<!DOCTYPE html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Mochi rzmong</title>
<style>
body{font-family:system-ui,sans-serif;background:#111;color:#eee;margin:12px;max-width:420px}
h1{font-size:1.2rem;color:#fd0}h2{font-size:1rem;color:#7ef;margin:16px 0 8px}
label{display:block;margin:8px 0 4px;color:#aaa;font-size:.85rem}
select,input[type=range],input[type=number]{width:100%;padding:8px;border-radius:8px;border:1px solid #333;background:#222;color:#fff;box-sizing:border-box}
.tog{display:flex;justify-content:space-between;align-items:center;padding:10px;background:#1a1a1a;border-radius:10px;margin:6px 0}
button{width:100%;padding:12px;margin:6px 0;border:0;border-radius:10px;font-weight:600}
.p{background:#fd0;color:#000}.s{background:#234;color:#9ef}
#st{font-size:.8rem;color:#888;margin-top:8px;white-space:pre-wrap}
.box{background:#1a1a22;border:1px solid #333;border-radius:12px;padding:12px;margin:10px 0}
.hint{font-size:.75rem;color:#666;margin:4px 0 8px}a{color:#7ef}
</style></head><body>
<h1>Mochi · rzmong</h1>
<p class=hint>v0.5.0 · offline · AP 192.168.4.1</p>
<div class=box>
<label>Tema</label><select id=theme></select>
<label>Sumber</label><select id=storage><option value=sd>SD</option><option value=flash>Flash</option></select>
<label>Mode putar</label><select id=mode><option value=kategori>Kategori</option><option value=acak>Acak</option><option value=acak_tema>Acak tema</option></select>
<label>Reaksi</label><select id=rmode><option value=acak>Acak</option><option value=tetap>Tetap</option></select>
<label>Volume <span id=vv></span></label><input type=range id=vol min=0 max=21 value=12>
<div class=tog><span>SFX</span><input type=checkbox id=sound checked></div>
</div>
<div class=box>
<h2>Chronos (BLE)</h2>
<p class=hint>Pair di app Chronos (bukan Bluetooth Settings). Nama BLE: <b>rzmong</b></p>
<div class=tog><span>Chronos BLE</span><input type=checkbox id=chronos></div>
<div class=tog><span>Tampil navigasi / peta</span><input type=checkbox id=chronos_nav checked></div>
<p class=hint>Ketuk: notif=1x · panggilan=tahan · nav=2x sembunyi</p>
<div id=chinfo class=hint>—</div>
</div>
<button class=p onclick=save()>Simpan ke Mochi</button>
<button class=s onclick=load()>Muat status</button>
<p class=hint><a href=https://rz7mong.github.io/mochi-rzmong/studio.html>Studio convert GIF</a></p>
<div id=st></div>
<script>
const T=['wajah','gundam','mobil','polisi','musik','neon','anime','makanan','intro'];
const ts=document.getElementById('theme');T.forEach(t=>{const o=document.createElement('option');o.value=t;o.textContent=t;ts.appendChild(o);});
document.getElementById('vol').oninput=e=>document.getElementById('vv').textContent=e.target.value;
async function load(){try{const j=await(await fetch('/api/status')).json();
if(j.theme)ts.value=j.theme;if(j.storage)document.getElementById('storage').value=j.storage;
if(j.mode)document.getElementById('mode').value=j.mode;if(j.react_mode)document.getElementById('rmode').value=j.react_mode;
if(typeof j.vol==='number'){document.getElementById('vol').value=j.vol;document.getElementById('vv').textContent=j.vol;}
if(typeof j.sound==='boolean')document.getElementById('sound').checked=j.sound;
if(typeof j.chronos==='boolean')document.getElementById('chronos').checked=j.chronos;
if(typeof j.chronos_nav==='boolean')document.getElementById('chronos_nav').checked=j.chronos_nav;
let ci='BLE: '+(j.chronos_run?'ON':'off');
if(j.chronos_conn)ci+=' · linked';
if(j.chronos_mac)ci+='\n'+j.chronos_mac;
if(j.chronos_time)ci+='\n'+j.chronos_time;
if(j.nav_active)ci+='\nNav: '+(j.nav_title||'aktif')+' '+(j.nav_dist||'');
document.getElementById('chinfo').textContent=ci;
document.getElementById('st').textContent='v'+(j.ver||'?')+' · '+(j.ap_ssid||'')+' / '+(j.ap_pass||'');
}catch(e){document.getElementById('st').textContent='Gagal muat';}}
async function save(){const body={theme:ts.value,storage:document.getElementById('storage').value,play_mode:document.getElementById('mode').value,react_mode:document.getElementById('rmode').value,volume:+document.getElementById('vol').value,sound:document.getElementById('sound').checked,chronos:document.getElementById('chronos').checked,chronos_nav:document.getElementById('chronos_nav').checked};
try{const r=await fetch('/api/settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
document.getElementById('st').textContent=r.ok?'Tersimpan':'Gagal';if(r.ok)setTimeout(load,400);}catch(e){document.getElementById('st').textContent='Offline';}}
load();
</script></body></html>
)MOCHI";
