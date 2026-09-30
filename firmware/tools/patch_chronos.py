#!/usr/bin/env python3
from pathlib import Path
p = Path("firmware/src/main.cpp")
m = p.read_text()
if "chronos_ui.inc" in m:
    print("already"); raise SystemExit(0)
if len(m) < 10000:
    raise SystemExit("main too small")
m = m.replace(
  'WebServer server(80); DNSServer dnsServer; ChronosESP32 watch; Preferences prefs;',
  'WebServer server(80); DNSServer dnsServer; ChronosESP32 watch("rzmong", CF_ESP32_240x240); Preferences prefs;')
if 'notifUntil' not in m:
  m = m.replace(
    'bool soundOn=true, useSd=false, chronosOn=false, showWm=true;',
    'bool soundOn=true, useSd=false, chronosOn=false, showWm=true;\nbool chronoConn=false, ringerOn=false;\nString notifApp, notifTitle, notifMsg, ringerName;\nuint32_t notifUntil=0;')
if 'chronos_ui.inc' not in m:
  m = m.replace(
    'static const int NMENU=16, VIS=7;',
    'static const int NMENU=16, VIS=7;\n#include "chronos_ui.inc"')
m = m.replace(
  'else if(menuRow==11){chronosOn=!chronosOn; savePrefs(); showInfo("chronos",chronosOn?"ON":"OFF");}',
  'else if(menuRow==11){chronosOn=!chronosOn; savePrefs(); chronosApply(); showInfo("Chronos",chronosOn?(chronoConn?"ON linked":"ON pair app"):"OFF");}')
m = m.replace(
  'char foot[56]; snprintf(foot,56,"%d/%d vol%d %s",menuRow+1,NMENU,volume,useSd&&sdOk?"SD":"flash");',
  'char foot[64]; snprintf(foot,64,"%d/%d vol%d %s%s",menuRow+1,NMENU,volume,useSd&&sdOk?"SD":"flash", chronosOn?(chronoConn?" BLE*":" BLE"):"");')
m = m.replace(
  'd["chronos"]=chronosOn;',
  'd["chronos"]=chronosOn;\n  d["chronos_conn"]=chronosOn && watch.isConnected();\n  d["chronos_run"]=chronosOn && watch.isRunning();\n  if(chronosOn && watch.isRunning()) d["chronos_mac"]=watch.getAddress();\n  if(chronosOn && chronoConn) d["chronos_time"]=watch.getTimeDate();')
m = m.replace(
  'if(d["chronos"].is<bool>()) chronosOn=d["chronos"];',
  'if(d["chronos"].is<bool>()){ chronosOn=d["chronos"]; chronosApply(); }')
m = m.replace(
  '  if(chronosOn) watch.begin();\n}',
  '  chronosSetupCallbacks();\n  if(chronosOn) chronosApply();\n}')
old = """void loop(){\n  dnsServer.processNextRequest();\n  server.handleClient(); if(chronosOn) watch.loop();\n  bool down=digitalRead(MOCHI_PIN_TOUCH)==HIGH;\n  if(ui==UI_MENU){\n    if(down&&!prevDown) downAt=millis();\n    if(!down&&prevDown){ uint32_t held=millis()-downAt; if(held>=900){soundOn=!soundOn;savePrefs();} else {taps++; lastTap=millis();} }\n    prevDown=down; finishTaps(); drawMenu(); delay(35); return;\n  }\n  finishTaps(); playCurrent();\n}"""
new = """void loop(){\n  dnsServer.processNextRequest();\n  server.handleClient();\n  if(chronosOn) watch.loop();\n  if(chronosOn && ringerOn){\n    drawChronosRinger();\n    bool down=digitalRead(MOCHI_PIN_TOUCH)==HIGH;\n    if(down&&!prevDown) ringerOn=false;\n    prevDown=down; delay(40); return;\n  }\n  if(chronosOn && notifUntil && (int32_t)(millis()-notifUntil)<0){\n    drawChronosNotif();\n    bool down=digitalRead(MOCHI_PIN_TOUCH)==HIGH;\n    if(down&&!prevDown) notifUntil=0;\n    prevDown=down; delay(40); return;\n  } else if(notifUntil && (int32_t)(millis()-notifUntil)>=0){\n    notifUntil=0;\n  }\n  bool down=digitalRead(MOCHI_PIN_TOUCH)==HIGH;\n  if(ui==UI_MENU){\n    if(down&&!prevDown) downAt=millis();\n    if(!down&&prevDown){ uint32_t held=millis()-downAt; if(held>=900){soundOn=!soundOn;savePrefs();} else {taps++; lastTap=millis();} }\n    prevDown=down; finishTaps(); drawMenu(); delay(35); return;\n  }\n  finishTaps(); playCurrent();\n}"""
if "drawChronosRinger();" not in m:
  if old not in m: raise SystemExit("loop not found")
  m = m.replace(old, new)
m = m.replace("0.4.8 — captive DNS", "0.4.9 — Chronos full + captive DNS")
p.write_text(m)
print("patched", len(m))
