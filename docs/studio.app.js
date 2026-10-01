
const ffmpeg = new FFmpegWASM.FFmpeg();
let loaded = false;
let result = { gif: null, wav: null, tema: "wajah", stem: "raspberry" };

function log(m) {
  const el = document.getElementById("log");
  el.textContent += m + "\n";
  el.scrollTop = el.scrollHeight;
}
function setStatus(t, ok) {
  const s = document.getElementById("status");
  s.textContent = t;
  if (ok === true) s.className = "ok";
  else if (ok === false) s.className = "warn";
  else s.className = "hint";
}
function host() {
  return document.getElementById("host").value.replace(/\/$/, "");
}
function fmtSize(n) {
  if (n < 1024) return n + " B";
  if (n < 1048576) return (n / 1024).toFixed(1) + " KB";
  return (n / 1048576).toFixed(2) + " MB";
}
async function toBlobURL(url, mime) {
  const res = await fetch(url);
  if (!res.ok) throw new Error("download fail " + url + " " + res.status);
  const buf = await res.arrayBuffer();
  return URL.createObjectURL(new Blob([buf], { type: mime }));
}
async function fetchFile(file) {
  return new Uint8Array(await file.arrayBuffer());
}
function withLocalWorker(fn) {
  const OrigWorker = window.Worker;
  const localWorker = new URL("./vendor/ffmpeg/814.ffmpeg.js", window.location.href).href;
  window.Worker = function (url, opts) {
    try {
      const u = String(url);
      if (u.indexOf("814.ffmpeg") >= 0 || u.indexOf("ffmpeg.js") >= 0) {
        return new OrigWorker(localWorker, opts);
      }
    } catch (e) {}
    return new OrigWorker(url, opts);
  };
  window.Worker.prototype = OrigWorker.prototype;
  return Promise.resolve().then(fn).finally(function () {
    window.Worker = OrigWorker;
  });
}

async function ping() {
  try {
    const j = await (await fetch(host() + "/api/status")).json();
    document.getElementById("pingst").textContent =
      "OK v" + (j.ver || "?") + " " + (j.storage || "") + " SD=" + (j.sd ? "yes" : "no");
    document.getElementById("pingst").className = "ok";
  } catch (e) {
    document.getElementById("pingst").textContent = "Fail - join Wi-Fi rzmong mochi first";
    document.getElementById("pingst").className = "warn";
  }
}

async function loadFFmpeg() {
  if (loaded) return;
  setStatus("Loading FFmpeg.wasm (~30 MB first time)...", false);
  log("Worker: local 814.ffmpeg.js");
  const coreBase = "https://cdn.jsdelivr.net/npm/@ffmpeg/core@0.12.6/dist/umd";
  const coreURL = await toBlobURL(coreBase + "/ffmpeg-core.js", "text/javascript");
  const wasmURL = await toBlobURL(coreBase + "/ffmpeg-core.wasm", "application/wasm");
  await withLocalWorker(function () {
    return ffmpeg.load({ coreURL: coreURL, wasmURL: wasmURL });
  });
  loaded = true;
  log("FFmpeg ready");
}

async function makeSmallGif(maxBytes) {
  const presets = [
    { t: "8", fps: "8", colors: "64", size: "240" },
    { t: "8", fps: "6", colors: "48", size: "240" },
    { t: "6", fps: "6", colors: "48", size: "240" },
    { t: "6", fps: "5", colors: "32", size: "200" },
    { t: "5", fps: "5", colors: "32", size: "200" },
    { t: "4", fps: "5", colors: "24", size: "200" },
    { t: "4", fps: "4", colors: "24", size: "160" },
    { t: "3", fps: "4", colors: "16", size: "160" }
  ];
  let lastBlob = null;
  for (let pi = 0; pi < presets.length; pi++) {
    const p = presets[pi];
    log("GIF try " + (pi + 1) + ": " + p.t + "s " + p.fps + "fps " + p.size + "px " + p.colors + " colors");
    setStatus("Compress GIF try " + (pi + 1) + "/" + presets.length + "...", false);
    const scale =
      "fps=" + p.fps +
      ",scale=" + p.size + ":" + p.size +
      ":force_original_aspect_ratio=decrease,pad=" + p.size + ":" + p.size +
      ":(ow-iw)/2:(oh-ih)/2:color=black";
    try {
      await ffmpeg.exec([
        "-i", "input",
        "-t", p.t,
        "-vf", scale + ",palettegen=max_colors=" + p.colors + ":stats_mode=single",
        "-y", "palette.png"
      ]);
      await ffmpeg.exec([
        "-i", "input",
        "-i", "palette.png",
        "-t", p.t,
        "-lavfi", scale + "[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5",
        "-loop", "0",
        "-y", "out.gif"
      ]);
    } catch (e) {
      log("Palette fail, simple fallback: " + (e.message || e));
      await ffmpeg.exec([
        "-i", "input",
        "-t", p.t,
        "-r", p.fps,
        "-vf", scale,
        "-loop", "0",
        "-y", "out.gif"
      ]);
    }
    const gifData = await ffmpeg.readFile("out.gif");
    lastBlob = new Blob([gifData.buffer], { type: "image/gif" });
    log("GIF try " + (pi + 1) + " size: " + fmtSize(lastBlob.size));
    if (lastBlob.size <= maxBytes) return lastBlob;
  }
  return lastBlob;
}

async function convertVideoToPair(file) {
  await ffmpeg.writeFile("input", await fetchFile(file));
  log("Source: " + file.name + " (" + fmtSize(file.size) + ")");
  const gifBlob = await makeSmallGif(599000);
  log("GIF final: " + fmtSize(gifBlob.size));
  let wavBlob = null;
  setStatus("Extract audio from video...", false);
  const audioTries = [
    ["-i", "input", "-t", "8", "-vn", "-map", "0:a:0", "-acodec", "pcm_s16le", "-ar", "22050", "-ac", "1", "-y", "out_from_vid.wav"],
    ["-i", "input", "-t", "8", "-vn", "-acodec", "pcm_s16le", "-ar", "22050", "-ac", "1", "-y", "out_from_vid.wav"]
  ];
  for (let ti = 0; ti < audioTries.length; ti++) {
    try {
      log("Audio try " + (ti + 1) + "...");
      await ffmpeg.exec(audioTries[ti]);
      const wavData = await ffmpeg.readFile("out_from_vid.wav");
      log("Audio raw size: " + wavData.length + " bytes");
      if (wavData.length > 2000) {
        wavBlob = new Blob([wavData.buffer], { type: "audio/wav" });
        log("WAV from video: " + fmtSize(wavBlob.size));
        break;
      }
    } catch (e) {
      log("Audio try " + (ti + 1) + " fail: " + (e.message || e));
    }
  }
  if (!wavBlob) log("No audio track found");
  return { gif: gifBlob, wav: wavBlob };
}

async function convertAudioOnly(file) {
  await ffmpeg.writeFile("ain", await fetchFile(file));
  await ffmpeg.exec([
    "-i", "ain",
    "-t", "8",
    "-acodec", "pcm_s16le",
    "-ar", "22050",
    "-ac", "1",
    "-y", "out.wav"
  ]);
  const data = await ffmpeg.readFile("out.wav");
  return new Blob([data.buffer], { type: "audio/wav" });
}

function showPreview() {
  const box = document.getElementById("previewBox");
  const img = document.getElementById("previewGif");
  const audioMeta = document.getElementById("audioMeta");
  const sizeMeta = document.getElementById("sizeMeta");
  box.classList.add("show");
  let parts = [];
  if (result.gif) {
    img.style.display = "inline-block";
    img.src = URL.createObjectURL(result.gif);
    parts.push('<span class="badge">GIF ' + fmtSize(result.gif.size) + "</span>");
  } else {
    img.style.display = "none";
  }
  if (result.wav) {
    audioMeta.style.display = "block";
    const src = URL.createObjectURL(result.wav);
    audioMeta.innerHTML = "WAV paired · <audio controls src='" + src + "' style='max-width:100%;margin-top:6px'></audio>";
    parts.push('<span class="badge">WAV ' + fmtSize(result.wav.size) + "</span>");
  } else {
    audioMeta.style.display = "none";
  }
  sizeMeta.innerHTML =
    "Theme <b>" + result.tema + "</b> · file <b>" + result.stem + "</b><br>" +
    parts.join(" ") +
    "<br><span class='hint'>Same tema + stem: ESP32 plays WAV then GIF</span>";
}

async function doConvert() {
  const btn = document.getElementById("btnConvert");
  btn.disabled = true;
  document.getElementById("log").textContent = "";
  document.getElementById("previewBox").classList.remove("show");
  result = { gif: null, wav: null, tema: "", stem: "" };
  const tema = document.getElementById("tema").value.trim() || "wajah";
  const stem = document.getElementById("stem").value.trim() || "clip";
  const vid = document.getElementById("vid").files[0];
  const sfx = document.getElementById("sfx").files[0];
  if (!(vid || sfx)) {
    setStatus("Pick at least one file", false);
    btn.disabled = false;
    return;
  }
  try {
    await loadFFmpeg();
    if (vid) {
      const pair = await convertVideoToPair(vid);
      result.gif = pair.gif;
      if (pair.wav) result.wav = pair.wav;
    }
    if (sfx) {
      setStatus("Convert separate SFX to WAV...", false);
      log("SFX override: " + sfx.name);
      result.wav = await convertAudioOnly(sfx);
      log("WAV: " + fmtSize(result.wav.size));
    }
    if (result.gif) {
      if (result.gif.size > 599000) {
        setStatus("GIF still over 599 KB after compress — use Save", false);
        log("TIP: try a shorter / simpler clip");
      }
    }
    if (result.wav) {
      if (result.wav.size > 599000) setStatus("WAV over 599 KB", false);
    }
    result.tema = tema;
    result.stem = stem;
    showPreview();
    if (result.gif) {
      if (result.wav) setStatus("Paired GIF + WAV ready — Save or Upload", true);
      else setStatus("GIF ready (no audio). Use video with sound, or add SFX file.", true);
    } else {
      setStatus("WAV ready", true);
    }
  } catch (e) {
    setStatus("Error: " + (e.message || e), false);
    log(String(e));
    console.error(e);
  }
  btn.disabled = false;
}

function downloadBlob(blob, filename) {
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
}

function saveLocal() {
  if (!(result.gif || result.wav)) {
    setStatus("Convert first", false);
    return;
  }
  if (result.gif) {
    downloadBlob(result.gif, result.stem + ".gif");
    log("Download " + result.stem + ".gif to /gif/" + result.tema + "/");
  }
  if (result.wav) {
    setTimeout(function () {
      downloadBlob(result.wav, result.stem + ".wav");
      log("Download " + result.stem + ".wav to /sfx/" + result.tema + "/");
    }, 400);
  }
  setStatus("Saved. Put both on SD with same tema + stem.", true);
}

async function uploadOne(blob, type, tema, stem) {
  const fd = new FormData();
  fd.append("file", blob, stem + "." + type);
  const amp = String.fromCharCode(38);
  const url =
    host() +
    "/api/upload?tema=" +
    encodeURIComponent(tema) +
    amp + "stem=" +
    encodeURIComponent(stem) +
    amp + "type=" +
    type;
  const r = await fetch(url, { method: "POST", body: fd });
  const j = await r.json().catch(function () {
    return { error: "bad_response" };
  });
  if (!r.ok) throw new Error(j.error || "HTTP " + r.status);
  return j;
}

async function doUpload() {
  if (!(result.gif || result.wav)) {
    setStatus("Convert first", false);
    return;
  }
  const btn = document.getElementById("btnUpload");
  btn.disabled = true;
  try {
    if (result.gif) {
      if (result.gif.size > 599000) throw new Error("GIF too large (max 599 KB)");
      setStatus("Upload GIF...", false);
      const res = await uploadOne(result.gif, "gif", result.tema, result.stem);
      log("GIF OK " + res.path + " " + res.size + " bytes");
    }
    if (result.wav) {
      if (result.wav.size > 599000) throw new Error("WAV too large (max 599 KB)");
      setStatus("Upload WAV...", false);
      const res = await uploadOne(result.wav, "wav", result.tema, result.stem);
      log("WAV OK " + res.path + " " + res.size + " bytes");
    }
    setStatus("Upload done — Mochi plays WAV then GIF", true);
  } catch (e) {
    setStatus("Error: " + (e.message || e), false);
    log(String(e));
  }
  btn.disabled = false;
}

document.getElementById("btnPing").onclick = ping;
document.getElementById("btnConvert").onclick = doConvert;
document.getElementById("btnSave").onclick = saveLocal;
document.getElementById("btnUpload").onclick = doUpload;
