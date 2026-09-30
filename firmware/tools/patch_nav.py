#!/usr/bin/env python3
from pathlib import Path
p = Path("firmware/src/main.cpp")
m = p.read_text()
if "drawChronosNav" in m and "chronos_nav" in m:
    print("already"); raise SystemExit(0)
if len(m) < 10000: raise SystemExit("main too small")
if "chronosNav" not in m:
    m = m.replace("bool chronoConn=false, ringerOn=false;", "bool chronoConn=false, ringerOn=false, chronosNav=true;")
if "chrono_nav" not in m:
    m = m.replace(
        'useSd=prefs.getBool("usesd",false); chronosOn=prefs.getBool("chrono",false); showWm=prefs.getBool("wm",true);',
        'useSd=prefs.getBool("usesd",false); chronosOn=prefs.getBool("chrono",false); chronosNav=prefs.getBool("chrono_nav",true); showWm=prefs.getBool("wm",true);')
    m = m.replace(
        'prefs.putBool("sound",soundOn); prefs.putBool("usesd",useSd); prefs.putBool("chrono",chronosOn); prefs.putBool("wm",showWm);',
        'prefs.putBool("sound",soundOn); prefs.putBool("usesd",useSd); prefs.putBool("chrono",chronosOn); prefs.putBool("chrono_nav",chronosNav); prefs.putBool("wm",showWm);')
old_st = """d[\"chronos\"]=chronosOn;
  d[\"chronos_conn\"]=chronosOn && watch.isConnected();
  d[\"chronos_run\"]=chronosOn && watch.isRunning();
  if(chronosOn && watch.isRunning()) d[\"chronos_mac\"]=watch.getAddress();
  if(chronosOn && chronoConn) d[\"chronos_time\"]=watch.getTimeDate();"""
new_st = """d[\"chronos\"]=chronosOn;
  d[\"chronos_conn\"]=chronosOn && watch.isConnected();
  d[\"chronos_run\"]=chronosOn && watch.isRunning();
  d[\"chronos_nav\"]=chronosNav;
  d[\"nav_active\"]=navActive && !navHide;
  if(chronosOn && watch.isRunning()) d[\"chronos_mac\"]=watch.getAddress();
  if(chronosOn && chronoConn) d[\"chronos_time\"]=watch.getTimeDate();
  if(navActive){ d[\"nav_title\"]=navTitle; d[\"nav_dist\"]=navDist; }"""
if old_st in m: m = m.replace(old_st, new_st)
else: raise SystemExit("status block not found")
if 'chronos_nav"].is' not in m:
    m = m.replace(
        'if(d["chronos"].is<bool>()){ chronosOn=d["chronos"]; chronosApply(); }',
        'if(d["chronos"].is<bool>()){ chronosOn=d["chronos"]; chronosApply(); }\n  if(d["chronos_nav"].is<bool>()){ chronosNav=d["chronos_nav"]; }')
new_loop = r"""void loop(){
  dnsServer.processNextRequest();
  server.handleClient();
  if(chronosOn) watch.loop();

  if(chronosOn && ringerOn){
    drawChronosRinger();
    bool down=digitalRead(MOCHI_PIN_TOUCH)==HIGH;
    if(down&&!prevDown) downAt=millis();
    if(!down&&prevDown){ if(millis()-downAt>=600) ringerOn=false; }
    prevDown=down; delay(40); return;
  }
  if(chronosOn && notifUntil && (int32_t)(millis()-notifUntil)<0){
    drawChronosNotif();
    bool down=digitalRead(MOCHI_PIN_TOUCH)==HIGH;
    if(down&&!prevDown){ notifUntil=0; }
    prevDown=down; delay(40); return;
  } else if(notifUntil && (int32_t)(millis()-notifUntil)>=0){
    notifUntil=0;
  }
  if(chronosOn && chronosNav && navActive && !navHide){
    drawChronosNav();
    bool down=digitalRead(MOCHI_PIN_TOUCH)==HIGH;
    if(down&&!prevDown){
      if(millis()-lastTap<400){ navHide=true; taps=0; }
      else { lastTap=millis(); taps=1; }
    }
    prevDown=down; delay(40); return;
  }

  bool down=digitalRead(MOCHI_PIN_TOUCH)==HIGH;
  if(ui==UI_MENU){
    if(down&&!prevDown) downAt=millis();
    if(!down&&prevDown){ uint32_t held=millis()-downAt; if(held>=900){soundOn=!soundOn;savePrefs();} else {taps++; lastTap=millis();} }
    prevDown=down; finishTaps(); drawMenu(); delay(35); return;
  }
  finishTaps(); playCurrent();
}
"""
idx = m.find("void loop(){")
if idx < 0: raise SystemExit("no loop")
m = m[:idx] + new_loop
m = m.replace("0.4.9 — Chronos full", "0.5.0 — Chronos nav + full")
p.write_text(m)
print("patched", len(m))
