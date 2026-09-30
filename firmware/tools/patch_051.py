#!/usr/bin/env python3
from pathlib import Path
import re
p = Path("firmware/src/main.cpp")
m = p.read_text()
if "void serviceNet()" in m and "HTTP_OPTIONS" in m and "ap_pass" not in m:
    print("already"); raise SystemExit(0)
if len(m) < 10000:
    raise SystemExit("main too small")

if "void serviceNet()" not in m:
    m = m.replace(
        "void playReactGif(){",
        "void serviceNet(){\n  dnsServer.processNextRequest();\n  server.handleClient();\n  if(chronosOn) watch.loop();\n  yield();\n}\nvoid playReactGif(){",
    )

m = m.replace(
    "while(gif.playFrame(true,NULL)){ server.handleClient(); if(millis()-t0>1600) break; yield(); }",
    "while(gif.playFrame(true,NULL)){ serviceNet(); if(millis()-t0>1600) break; }",
)

old_ft = (
"void finishTaps(){\n"
"  if(!taps||millis()-lastTap<=320)return;\n"
"  if(ui==UI_MENU){ if(taps==1) menuRow=(menuRow+1)%NMENU; else applyMenu(); }\n"
"  else { if(taps>=2){ui=UI_MENU; menuRow=0; menuTop=0; drawMenu();} }\n"
"  taps=0;\n"
"}"
)
new_ft = (
"void finishTaps(){\n"
"  if(!taps||millis()-lastTap<=320)return;\n"
"  if(ui==UI_MENU){ if(taps==1) menuRow=(menuRow+1)%NMENU; else applyMenu(); }\n"
"  else {\n"
"    if(taps>=2){ ui=UI_MENU; menuRow=0; menuTop=0; taps=0; drawMenu(); return; }\n"
"    if(taps==1) playReactGif();\n"
"  }\n"
"  taps=0;\n"
"}"
)
if old_ft in m:
    m = m.replace(old_ft, new_ft)
    print("finishTaps ok")

if "playReactGif(); prevDown" in m:
    m2, n = re.subn(
        r"bool playCurrent\(\)\{.*?\n\}",
        "bool playCurrent(){\n"
        "  bool ok;\n"
        "  bool fromSd=useSd&&sdOk&&nparts>0;\n"
        "  if(fromSd && soundOn) playSfxForGifPath(parts[idx].c_str());\n"
        "  if(fromSd){ sdBusy=true; ok=playOpen(NULL,0,parts[idx].c_str()); }\n"
        "  else ok=playOpen(DEFAULT_GIFS[defIdx].data,DEFAULT_GIFS[defIdx].len,NULL);\n"
        "  if(!ok){\n"
        "    sdBusy=false;\n"
        "    ok=playOpen(DEFAULT_GIFS[defIdx].data,DEFAULT_GIFS[defIdx].len,NULL);\n"
        "    if(!ok){ delay(40); return false; }\n"
        "  }\n"
        "  tft.fillScreen(TFT_BLACK);\n"
        "  while(gif.playFrame(true,NULL)){\n"
        "    serviceNet();\n"
        "    bool down=digitalRead(MOCHI_PIN_TOUCH)==HIGH;\n"
        "    if(down&&!prevDown) downAt=millis();\n"
        "    if(!down&&prevDown){\n"
        "      uint32_t held=millis()-downAt;\n"
        "      if(held>=900){ soundOn=!soundOn; savePrefs(); }\n"
        "      else { taps++; lastTap=millis(); }\n"
        "      prevDown=down; break;\n"
        "    }\n"
        "    prevDown=down;\n"
        "  }\n"
        "  gif.close(); sdBusy=false; brandMark(); return true;\n"
        "}",
        m,
        count=1,
        flags=re.S,
    )
    print("playCurrent", n)
    m = m2

m = m.replace(
    'd["ap_ssid"]=MOCHI_AP_NAME; d["ap_pass"]=MOCHI_AP_PASS; d["sd_busy"]=sdBusy;',
    'd["ap_ssid"]=MOCHI_AP_NAME; d["sd_busy"]=sdBusy;',
)
m = m.replace(
    'out["storage"]=(useSd&&sdOk)?"sd":"flash"; out["gif_count"]=nparts; out["sd"]=sdOk; out["ap_pass"]=MOCHI_AP_PASS;',
    'out["storage"]=(useSd&&sdOk)?"sd":"flash"; out["gif_count"]=nparts; out["sd"]=sdOk;',
)

if "void sendCorsHeaders" not in m:
    m = m.replace(
        "void handleRoot(){",
        "void sendCorsHeaders(){\n"
        "  server.sendHeader(\"Access-Control-Allow-Origin\",\"*\");\n"
        "  server.sendHeader(\"Access-Control-Allow-Methods\",\"GET,POST,OPTIONS\");\n"
        "  server.sendHeader(\"Access-Control-Allow-Headers\",\"Content-Type\");\n"
        "}\n"
        "void handleOptions(){\n"
        "  sendCorsHeaders();\n"
        "  server.send(204);\n"
        "}\n"
        "void handleRoot(){",
    )

m = m.replace(
    'String s; serializeJson(d,s); server.send(200,"application/json",s);\n}\nvoid handleThemes(){',
    'String s; serializeJson(d,s); sendCorsHeaders(); server.send(200,"application/json",s);\n}\nvoid handleThemes(){',
)
m = m.replace(
    'String s; serializeJson(d,s); server.send(200,"application/json",s);\n}\nvoid handleSettings(){',
    'String s; serializeJson(d,s); sendCorsHeaders(); server.send(200,"application/json",s);\n}\nvoid handleSettings(){',
)
m = m.replace(
    'String s; serializeJson(out,s); server.send(200,"application/json",s);\n}\n\n// ===== Upload',
    'String s; serializeJson(out,s); sendCorsHeaders(); server.send(200,"application/json",s);\n}\n\n// ===== Upload',
)

if "HTTP_OPTIONS" not in m:
    m = m.replace(
        'server.on("/api/upload", HTTP_POST, [](){}, handleUpload);\n  server.onNotFound(handleNotFound);',
        'server.on("/api/upload", HTTP_POST, [](){}, handleUpload);\n'
        '  server.on("/api/status", HTTP_OPTIONS, handleOptions);\n'
        '  server.on("/api/themes", HTTP_OPTIONS, handleOptions);\n'
        '  server.on("/api/settings", HTTP_OPTIONS, handleOptions);\n'
        '  server.on("/api/upload", HTTP_OPTIONS, handleOptions);\n'
        '  server.onNotFound(handleNotFound);',
    )

old_loop = "void loop(){\n  dnsServer.processNextRequest();\n  server.handleClient();\n  if(chronosOn) watch.loop();"
if old_loop in m:
    m = m.replace(old_loop, "void loop(){\n  serviceNet();")

p.write_text(m)
print("done", len(m))
for k in ["void serviceNet()", "HTTP_OPTIONS", "if(taps==1) playReactGif()"]:
    print(k, k in m)
print("ap_pass", "ap_pass" in m)
