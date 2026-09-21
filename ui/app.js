/* =========================================================
   CrackProof - Browser Client Logic (app.js)
   Server se data communicate karta hai aur screen manage karta hai.
   ========================================================= */

/* Kaun logged in hai, kaunsa interview chal raha hai */
var user = null;
var isGuest = false;
var interviewId = null;
var audioPath = null;
var questionNumber = 0;
var batchDone = false;

/* =========================================================
   UTILITIES
   ========================================================= */

function $(id) {
  return document.getElementById(id);
}

/* Text ko safe banao taaki XSS na ho */
function safe(text) {
  var box = document.createElement("div");
  box.textContent = text;
  return box.innerHTML;
}

/* Screen switch karo */
function go(name) {
  var screens = document.querySelectorAll(".screen");
  for (var i = 0; i < screens.length; i++) {
    screens[i].classList.remove("on");
  }
  var target = $("s-" + name);
  if (target) {
    target.classList.add("on");
  }
  window.scrollTo(0, 0);
}

/* Evaluation screen tab switch */
function tab(button, paneId) {
  var box = button.parentElement.parentElement;
  var buttons = box.querySelectorAll(".tabs button");
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].classList.remove("on");
  }
  var panes = box.querySelectorAll(".tabpane");
  for (var j = 0; j < panes.length; j++) {
    panes[j].classList.remove("on");
  }
  button.classList.add("on");
  var targetPane = $(paneId);
  if (targetPane) {
    targetPane.classList.add("on");
  }
}

/* Server API fetch helper */
async function ask(path, data) {
  var options = { method: "GET" };
  if (data) {
    options.method = "POST";
    options.headers = { "Content-Type": "application/json" };
    options.body = JSON.stringify(data);
  }

  try {
    var reply = await fetch(path, options);
    return await reply.json();
  } catch (problem) {
    return {
      ok: false,
      message: "Could not reach the server. Start it with: python3 server.py"
    };
  }
}

function readyWord(value) {
  if (value === "STRONG") return "Ready";
  if (value === "DEVELOPING") return "Almost Ready";
  if (value === "NEEDS_IMPROVEMENT") return "Needs Practice";
  return "In progress";
}

function readyColour(value) {
  if (value === "STRONG") return "pill-g";
  if (value === "DEVELOPING") return "pill-a";
  if (value === "NEEDS_IMPROVEMENT") return "pill-n";
  return "pill-b";
}

function showError(boxId, message) {
  var box = $(boxId);
  if (!box) return;
  if (message) {
    box.textContent = message;
    box.hidden = false;
  } else {
    box.textContent = "";
    box.hidden = true;
  }
}

/* =========================================================
   AUTHENTICATION
   ========================================================= */

async function signIn() {
  showError("loginError", "");
  var em = $("em").value.trim();
  var pw = $("pw").value;

  if (!em || !pw) {
    showError("loginError", "Please enter both your email and password.");
    return;
  }

  var btn = $("signInBtn");
  var oldText = btn.textContent;
  btn.disabled = true;
  btn.textContent = "Signing In...";

  try {
    var reply = await ask("/api/login", { email: em, password: pw });
    if (reply.ok) {
      user = reply.user;
      isGuest = false;
      openApp();
    } else {
      showError("loginError", reply.message || "Invalid credentials.");
    }
  } catch (err) {
    showError("loginError", "Could not sign in. Please try again.");
  } finally {
    btn.disabled = false;
    btn.textContent = oldText;
  }
}

async function signUp() {
  showError("signupError", "");
  var name = $("suName") ? $("suName").value.trim() : "";
  var em = $("suEm").value.trim();
  var pw = $("suPw").value;

  if (!name) {
    showError("signupError", "Please enter your full name.");
    if ($("suName")) $("suName").focus();
    return;
  }
  if (!em || !pw) {
    showError("signupError", "Please fill in all fields.");
    return;
  }
  if (pw.length < 6) {
    showError("signupError", "Password must be at least 6 characters.");
    return;
  }

  var btn = $("signUpBtn");
  var oldText = btn.textContent;
  btn.disabled = true;
  btn.textContent = "Creating Account...";

  try {
    var reply = await ask("/api/signup", { name: name, email: em, password: pw });
    if (reply.ok && reply.user) {
      user = reply.user;
      isGuest = false;
      openApp();
    } else {
      showError("signupError", reply.message || "Could not create account.");
    }
  } catch (err) {
    showError("signupError", "Could not connect to server. Please try again.");
  } finally {
    btn.disabled = false;
    btn.textContent = oldText;
  }
}

async function signOut() {
  await ask("/api/logout", {});
  user = null;
  isGuest = false;
  $("em").value = "";
  $("pw").value = "";
  if ($("suName")) $("suName").value = "";
  if ($("suEm")) $("suEm").value = "";
  if ($("suPw")) $("suPw").value = "";
  go("login");
}

function openApp() {
  if (isGuest) {
    $("userEmail").textContent = "Guest";
    $("avatar").textContent = "G";
    $("greeting").textContent = "Welcome to CrackProof!";
    $("guestNote").hidden = false;
  } else {
    var displayName = (user && user.name) ? user.name : (user && user.email ? user.email.split("@")[0].charAt(0).toUpperCase() + user.email.split("@")[0].slice(1) : "Candidate");
    $("userEmail").textContent = displayName;
    if (user && user.email) $("userEmail").title = user.email;
    $("avatar").textContent = (displayName[0] || "U").toUpperCase();
    $("greeting").textContent = "Good to see you, " + displayName + "!";
    $("guestNote").hidden = true;
  }
  go("dash");
  loadHistory();
}

/* =========================================================
   DASHBOARD & HISTORY
   ========================================================= */

async function loadHistory() {
  if (isGuest) {
    $("historyRows").innerHTML =
      '<tr><td colspan="4" class="muted small" style="padding:24px; text-align:center;">Guest sessions are not stored. Sign up to track your progress over time.</td></tr>';
    countTopics([]);
    return;
  }

  var reply = await ask("/api/history");
  if (!reply.ok || !reply.interviews || reply.interviews.length === 0) {
    $("historyRows").innerHTML =
      '<tr><td colspan="4" class="muted small" style="padding:24px; text-align:center;">No past interviews yet. Pick a topic to begin!</td></tr>';
    countTopics([]);
    return;
  }

  countTopics(reply.interviews);

  var html = "";
  for (var i = 0; i < reply.interviews.length; i++) {
    var row = reply.interviews[i];
    var readiness = row.readiness || "IN_PROGRESS";
    var dateStr = row.created_at ? row.created_at.slice(0, 10) : "Recent";

    html +=
      '<tr class="histRow" onclick="makeHistoryClick(\'' + row.id + '\')()">' +
      "<td>" + safe(dateStr) + "</td>" +
      "<td><b>" + safe(row.topic) + "</b></td>" +
      "<td>" + (row.questions_answered || 0) + " answered</td>" +
      "</tr>";
  }
  $("historyRows").innerHTML = html;
}

function countTopics(list) {
  var counts = {};
  for (var i = 0; i < list.length; i++) {
    var t = list[i].topic;
    counts[t] = (counts[t] || 0) + (list[i].questions_answered || 0);
  }

  var tags = document.querySelectorAll(".qcount");
  for (var j = 0; j < tags.length; j++) {
    var top = tags[j].getAttribute("data-topic");
    if (counts[top]) {
      tags[j].textContent = counts[top] + " questions practiced";
    } else {
      tags[j].textContent = "5 questions · Core concepts";
    }
  }
}

/* =========================================================
   INTERVIEW SESSION FLOW
   ========================================================= */

async function startInterview(topic) {
  go("iv1");
  $("questionText").textContent = "Setting up your " + topic + " interview...";
  batchDone = false;
  questionNumber = 0;

  var reply = await ask("/api/start", { topic: topic });
  if (reply.ok) {
    interviewId = reply.interview_id;
    showQuestion(reply);
  } else {
    $("questionText").textContent = reply.message || "Failed to start interview.";
  }
}

function showQuestion(reply) {
  questionNumber = reply.question_number || questionNumber + 1;
  $("questionText").textContent = reply.question;
  markStep(1);

  var crumb = document.querySelector("#s-iv1 .crumb");
  if (crumb && reply.topic) {
    crumb.innerHTML = "<b>" + safe(reply.topic) + '</b><span class="sep">›</span><span>Question ' + questionNumber + " of 5</span>";
  }
  var crumb2 = document.querySelector("#s-iv2 .crumb");
  if (crumb2 && reply.topic) {
    crumb2.innerHTML = "<b>" + safe(reply.topic) + '</b><span class="sep">›</span><span>Question ' + questionNumber + " of 5</span>";
  }
  var crumb3 = document.querySelector("#s-iv3 .crumb");
  if (crumb3 && reply.topic) {
    crumb3.innerHTML = "<b>" + safe(reply.topic) + '</b><span class="sep">›</span><span>Question ' + questionNumber + " of 5</span>";
  }
}

function markStep(num) {
  var stepContainers = [
    document.querySelectorAll("#s-iv1 .step"),
    document.querySelectorAll("#s-iv2 .step"),
    document.querySelectorAll("#s-iv3 .step")
  ];

  stepContainers.forEach(function (steps) {
    if (!steps.length) return;
    for (var i = 0; i < steps.length; i++) {
      steps[i].classList.remove("on", "done");
      if (i + 1 < num) {
        steps[i].classList.add("done");
      } else if (i + 1 === num) {
        steps[i].classList.add("on");
      }
    }
  });
}

/* =========================================================
   AUDIO & INDEXEDDB STORAGE
   ========================================================= */

var db = null;

function openStore() {
  return new Promise(function (done, fail) {
    if (db) {
      done(db);
      return;
    }
    var request = indexedDB.open("crackproof_audio", 1);
    request.onupgradeneeded = function (event) {
      var d = event.target.result;
      if (!d.objectStoreNames.contains("recordings")) {
        d.createObjectStore("recordings");
      }
    };
    request.onsuccess = function (event) {
      db = event.target.result;
      done(db);
    };
    request.onerror = function () {
      fail("IndexedDB unavailable");
    };
  });
}

function recordingKey(interview, number) {
  return interview + "_q" + number;
}

async function saveAudio(interview, number, question, blob) {
  try {
    var d = await openStore();
    var tx = d.transaction("recordings", "readwrite");
    var store = tx.objectStore("recordings");
    store.put(
      {
        interview_id: interview,
        question_number: number,
        question: question,
        audio: blob,
        saved_at: new Date().toISOString()
      },
      recordingKey(interview, number)
    );
  } catch (e) {
    console.warn("Audio cache not saved", e);
  }
}

async function loadAudio(interview, number) {
  try {
    var d = await openStore();
    return await new Promise(function (done) {
      var tx = d.transaction("recordings", "readonly");
      var store = tx.objectStore("recordings");
      var askReq = store.get(recordingKey(interview, number));
      askReq.onsuccess = function () {
        done(askReq.result ? askReq.result.audio : null);
      };
      askReq.onerror = function () {
        done(null);
      };
    });
  } catch (e) {
    return null;
  }
}

/* =========================================================
   AUDIO RECORDER & WAVEFORM
   ========================================================= */

var recorder = null;
var audioChunks = [];
var recTimer = null;
var recSeconds = 0;

function makeBars() {
  var wave = $("wave");
  if (!wave) return;
  wave.innerHTML = "";
  for (var i = 0; i < 32; i++) {
    var bar = document.createElement("i");
    bar.style.height = "6px";
    if (i >= 12 && i <= 20) bar.classList.add("mid");
    wave.appendChild(bar);
  }
}

function drawBars() {
  var bars = document.querySelectorAll("#wave i");
  if (!bars.length) return;
  for (var i = 0; i < bars.length; i++) {
    var h = 6 + Math.floor(Math.random() * 38);
    bars[i].style.height = h + "px";
  }
}

function showTime() {
  var m = Math.floor(recSeconds / 60);
  var s = recSeconds % 60;
  var str = (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
  $("recLabel").textContent = "Recording · " + str;
}

async function startRecording() {
  audioChunks = [];
  try {
    var stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = function (event) {
      if (event.data.size > 0) audioChunks.push(event.data);
    };
    recorder.start();

    recSeconds = 0;
    showTime();
    $("recBtn").classList.add("recording");
    $("recHint").textContent = "Click again when done speaking";

    recTimer = setInterval(function () {
      recSeconds++;
      showTime();
      drawBars();
    }, 100);
  } catch (e) {
    alert("Microphone access is required to record your answer.");
  }
}

function stopRecording() {
  if (!recorder) return;
  clearInterval(recTimer);
  recorder.stop();
  recorder.stream.getTracks().forEach(function (t) { t.stop(); });

  $("recBtn").classList.remove("recording");
  $("recLabel").textContent = "Processing audio...";
  $("recHint").textContent = "Transcribing with local Whisper...";

  setTimeout(sendRecording, 500);
}

async function sendRecording() {
  var blob = new Blob(audioChunks, { type: "audio/webm" });
  await saveAudio(interviewId, questionNumber, $("questionText").textContent, blob);

  var form = new FormData();
  form.append("interview_id", interviewId);
  form.append("question_number", questionNumber);
  form.append("audio", blob, "recording.webm");

  try {
    var res = await fetch("/api/transcribe", { method: "POST", body: form });
    var reply = await res.json();
    if (reply.ok) {
      audioPath = reply.audio_path;
      $("transcriptText").textContent = reply.transcript || "";
      go("iv2");
      markStep(2);
    } else {
      $("questionText").textContent = reply.message || "Transcription failed.";
      go("iv1");
    }
  } catch (err) {
    alert("Could not connect to transcription service.");
    go("iv1");
  }
}

/* =========================================================
   EVALUATION & REPORTS
   ========================================================= */

function makeList(items, kind) {
  if (!items || !items.length) return '<p class="muted small">None recorded.</p>';
  var html = '<ul style="margin:8px 0 0 18px; padding:0;">';
  for (var i = 0; i < items.length; i++) {
    html += '<li style="margin-bottom:6px;">' + safe(items[i]) + "</li>";
  }
  html += "</ul>";
  return html;
}

function statusPill(status) {
  if (status === "READY") return '<span class="pill pill-g">Ready</span>';
  if (status === "ALMOST_READY") return '<span class="pill pill-a">Almost Ready</span>';
  return '<span class="pill pill-n">Needs Practice</span>';
}

function niceName(dimension) {
  var map = {
    FUNDAMENTAL: "Core Concepts",
    REASONING: "Technical Reasoning",
    APPLICATION: "Real-World Application",
    EDGE_CASE: "Edge Cases & Depth"
  };
  return map[dimension] || dimension;
}

function showEvaluation(ev) {
  go("iv3");
  markStep(3);

  $("evtabs").querySelectorAll("button")[0].click();

  $("t1").innerHTML =
    "<h4>What you explained accurately</h4>" +
    makeList(ev.correct_points, "good");

  $("t2").innerHTML =
    "<h4>Key areas to cover next time</h4>" +
    makeList(ev.missing_core_concepts, "miss");

  $("t3").innerHTML =
    "<h4>Points to refine or clarify</h4>" +
    makeList(ev.misconceptions, "warn");

  var dims = ev.dimension_scores || {};
  var dHtml = '<h4>Depth Evaluation</h4><div style="margin-top:12px;">';
  for (var k in dims) {
    var val = dims[k] || 0;
    var pct = Math.min(100, Math.round((val / 10) * 100));
    dHtml +=
      '<div class="dim">' +
      "<span>" + niceName(k) + "</span><b>" + val + " / 10</b>" +
      '<div class="bar"><i style="width:' + pct + '%;"></i></div>' +
      "</div>";
  }
  dHtml += "</div>";
  $("t4").innerHTML = dHtml;

  $("t5").innerHTML =
    "<h4>Detailed Evaluator Rationale</h4>" +
    '<p class="tbox" style="margin-top:10px;">' + safe(ev.reasoning || "Evaluation grounded against reference knowledge.") + "</p>";
}

async function showReport(afterBatch) {
  go("report");
  var reply = await ask("/api/report", { interview_id: interviewId });
  if (reply.ok) {
    drawReport(reply);
  }
  if (afterBatch) {
    $("batchChoice").hidden = false;
  } else {
    $("batchChoice").hidden = true;
  }
}

function drawReport(reply) {
  $("reportMeta").textContent = (reply.topic || "") + " · " + (reply.questions_answered || 0) + " questions evaluated";

  var body = $("reportBody");
  var html =
    '<div class="card readiness">' +
    '<h3>Overall Candidate Readiness</h3>' +
    '<div style="margin:14px 0;">' + statusPill(reply.readiness) + '</div>' +
    '<p class="muted small">' + safe(reply.summary || "Complete summary generated from grounded LLM evaluation.") + '</p>' +
    '</div>';

  var profile = reply.dimension_profile || {};
  html += '<div class="card readiness"><h3>Profile Breakdown</h3><div class="scores">';
  for (var key in profile) {
    var score = profile[key] || 0;
    var pct = Math.min(100, Math.round((score / 10) * 100));
    html +=
      '<div>' +
      '<div class="score-top"><span>' + niceName(key) + '</span><b>' + score + '/10</b></div>' +
      '<div class="rbar"><i style="width:' + pct + '%;"></i></div>' +
      '</div>';
  }
  html += '</div></div>';

  body.innerHTML = html;
}

function openPastInterview(id) {
  interviewId = id;
  showReport(false);
}

/* =========================================================
   SETUP & EVENT BINDINGS
   ========================================================= */

function makeHistoryClick(id) {
  return function () {
    openPastInterview(id);
  };
}

function makeTopicClick(name) {
  return function () {
    startInterview(name);
  };
}

async function setup() {
  makeBars();

  /* Login & Signup buttons */
  $("signInBtn").onclick = signIn;
  $("signUpBtn").onclick = signUp;
  $("signOutBtn").onclick = signOut;

  $("guestBtn").onclick = function () {
    user = null;
    isGuest = true;
    openApp();
  };

  $("toSignup").onclick = function (e) {
    e.preventDefault();
    if ($("em") && $("em").value) $("suEm").value = $("em").value;
    if ($("pw") && $("pw").value) $("suPw").value = $("pw").value;
    showError("signupError", "");
    go("signup");
    if ($("suName")) $("suName").focus();
  };

  $("toLogin").onclick = function (e) {
    e.preventDefault();
    if ($("suEm") && $("suEm").value) $("em").value = $("suEm").value;
    if ($("suPw") && $("suPw").value) $("pw").value = $("suPw").value;
    showError("loginError", "");
    go("login");
    if ($("em")) $("em").focus();
  };

  /* Enter key triggers form submit */
  $("em").onkeydown = function (e) { if (e.key === "Enter") $("pw").focus(); };
  $("pw").onkeydown = function (e) { if (e.key === "Enter") signIn(); };
  if ($("suName")) {
    $("suName").onkeydown = function (e) { if (e.key === "Enter") $("suEm").focus(); };
  }
  $("suEm").onkeydown = function (e) { if (e.key === "Enter") $("suPw").focus(); };
  $("suPw").onkeydown = function (e) { if (e.key === "Enter") signUp(); };

  /* Topic cards */
  var cards = document.querySelectorAll(".topic");
  for (var i = 0; i < cards.length; i++) {
    var label = cards[i].querySelector("b").textContent;
    cards[i].onclick = makeTopicClick(label);
  }

  /* Audio recording button */
  $("recBtn").onclick = function () {
    if (recorder && recorder.state === "recording") {
      stopRecording();
    } else {
      startRecording();
    }
  };

  /* Continue to evaluation after reviewing transcript */
  $("continueBtn").onclick = async function () {
    var text = $("transcriptText").textContent.trim();
    if (!text) return;

    this.disabled = true;
    this.textContent = "Evaluating your answer...";

    var reply = await ask("/api/evaluate", {
      interview_id: interviewId,
      transcript: text,
      audio_path: audioPath
    });

    this.disabled = false;
    this.textContent = "Continue";

    if (reply.ok) {
      batchDone = reply.batch_complete;
      showEvaluation(reply.evaluation);
    } else {
      $("okbarText").textContent = reply.message || "Evaluation error.";
    }
  };

  $("playBtn").onclick = async function () {
    var blob = await loadAudio(interviewId, questionNumber);
    if (blob) {
      var audio = new Audio(URL.createObjectURL(blob));
      audio.play();
    } else {
      $("okbarText").textContent = "Audio not found on this device.";
    }
  };

  $("rerecBtn").onclick = async function () {
    await ask("/api/retry", { interview_id: interviewId });
    go("iv1");
  };

  $("nextBtn").onclick = async function () {
    if (batchDone) {
      showReport(true);
      return;
    }

    this.disabled = true;
    this.textContent = "Writing next question...";

    var reply = await ask("/api/next", { interview_id: interviewId });
    this.disabled = false;
    this.textContent = "Continue";

    showQuestion(reply);
    go("iv1");
  };

  var stops = document.querySelectorAll(".btn-danger");
  for (var j = 0; j < stops.length; j++) {
    stops[j].onclick = function () { showReport(false); };
  }

  $("sameTopicBtn").onclick = async function () {
    $("batchChoice").hidden = true;
    go("iv1");
    $("questionText").textContent = "Formulating your next question...";
    batchDone = false;
    var reply = await ask("/api/continue", { interview_id: interviewId });
    showQuestion(reply);
  };

  $("newTopicBtn").onclick = function () {
    $("batchChoice").hidden = true;
    go("topics");
  };

  $("finishBtn").onclick = function () {
    $("batchChoice").hidden = true;
    go("dash");
    loadHistory();
  };

  $("backHomeBtn").onclick = function () {
    go("dash");
    loadHistory();
  };

  /* Auto login session check */
  var me = await ask("/api/me");
  if (me.ok && me.user) {
    user = me.user;
    isGuest = false;
    openApp();
  }
}

document.addEventListener("DOMContentLoaded", setup);
