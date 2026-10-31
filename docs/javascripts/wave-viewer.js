// The waveform viewer (session 31, after Hallmark's measuring tool and Cobalt's timeline):
// under every WaveDrom diagram, two buttons that are off until pressed.
// - "מדידה" shows two cursors, A and B, on the clock edges (the diagram's dotted period
//   marks), a dimension line between them and the difference in cycles; in ns too when the
//   diagram declares its clock (a `dvq: { mhz: 100 }` key in its source, which WaveDrom
//   ignores). A click on the diagram moves the nearer cursor; the cursors are sliders
//   (arrows, Home, End) and can be dragged.
// - "הפעלה" sweeps a time line across the diagram once (what is still ahead is veiled) and
//   lights, line by line, a log of the changes written from the waves: "מחזור 3 : ack
//   עולה". Under reduced motion the log is shown at once.
// wavedrom-init.js hands each rendered diagram and its source to dvqWaveViewer.attach. The
// pure part (the changes of a source) runs under Node too (tests/tools/test_wave_viewer.py).
(() => {
  const NB = " ";

  // the source of a ```wavedrom block, which is a JavaScript object literal (unquoted keys)
  const parse = (text) => {
    try { return Function(`"use strict"; return (${text});`)(); } catch (e) { return null; }
  };

  // lanes left out of the log: clocks, and a lane that only numbers the cycles
  const isClock = (sig) => /clk|clock/i.test(String(sig.name || "")) || /^[pnPN][.pnPN|]*$/.test(String(sig.wave || ""));
  const isCounter = (sig) => /^(cycles?|cyc|מחזור)$/i.test(String(sig.name || "").trim());

  // one lane's values in time: [{ t, v }] at every change (t in cycles of the diagram)
  const lane = (sig) => {
    const wave = String(sig.wave || ""), period = Number(sig.period) || 1, phase = Number(sig.phase) || 0;
    const data = Array.isArray(sig.data) ? sig.data.map(String) : String(sig.data || "").split(/\s+/).filter(Boolean);
    const out = [];
    let v = null, d = 0;
    for (let k = 0; k < wave.length; k++) {
      const c = wave[k], t = k * period - phase;
      let nv = v;
      if (c === "." || c === "|") continue;
      if ("01xz".includes(c)) nv = c;
      else if (c === "h" || c === "H" || c === "u") nv = "1";
      else if (c === "l" || c === "L" || c === "d") nv = "0";
      else if (c === "=" || (c >= "2" && c <= "9")) nv = "=" + (d < data.length ? data[d++] : "");
      else continue;
      if (nv !== v) { out.push({ t: Math.round(t * 1000) / 1000, v: nv }); v = nv; }
    }
    return out;
  };

  const phrase = (name, from, to) => {
    if (to.startsWith("=")) return `${name} = ${to.slice(1) || "?"}`;
    if (to === "x") return `${name} לא מוגדר (x)`;
    if (to === "z") return `${name} מנותק (z)`;
    if (from === "1" && to === "0") return `${name} יורד`;
    if (to === "1") return `${name} עולה`;
    return `${name} יורד`;
  };

  // the changes of a diagram, grouped by time: [{ t, items: ["ack עולה", ...] }]; the values
  // at the start are not changes, and clock and counter lanes are left out. A diagram of
  // several cases (lanes split by empty {} rows) names each lane with its case: the case's
  // name from the head text ("late ack / req dropped / orphan ack") or its number.
  const changes = (src) => {
    const sigs = [];
    let group = 0;
    const walk = (list) => (list || []).forEach((s) => {
      if (Array.isArray(s)) walk(s.slice(1));                         // a group: ["name", sig, ...]
      else if (s && typeof s === "object" && s.wave) sigs.push({ s, group });
      else if (s && typeof s === "object" && sigs.length) group += 1;   // an empty row between cases
    });
    walk(src && src.signal);
    const used = new Set(sigs.map((x) => x.group));
    const heads = String((src && src.head && src.head.text) || "").split(" / ");
    const label = (g) => (used.size < 2 ? "" : ` (${heads.length === used.size ? heads[[...used].indexOf(g)].trim() : [...used].indexOf(g) + 1})`);
    const at = new Map();
    sigs.filter(({ s }) => !isClock(s) && !isCounter(s)).forEach(({ s, group: g }) => {
      let prev = null;
      lane(s).forEach(({ t, v }) => {
        if (prev !== null && t > 0) {
          if (!at.has(t)) at.set(t, []);
          at.get(t).push(phrase((String(s.name || "").trim() || "?") + label(g), prev, v));
        }
        prev = v;
      });
    });
    return [...at.keys()].sort((a, b) => a - b).map((t) => ({ t, items: at.get(t) }));
  };

  const fmtT = (t) => (Number.isInteger(t) ? String(t) : String(Math.round(t * 10) / 10));
  const cycles = (d) => (d === 1 ? "מחזור אחד" : `${d} מחזורים`);

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { parse, lane, changes, fmtT };
    return;
  }

  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const STEP_MS = 420;                                                  // the time line, per cycle
  const ICON = {
    measure: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3 7h18v10H3zm2 2v6h14V9h-2v3h-1V9h-2v2h-1V9h-2v3h-1V9H9v2H8V9H7v3H6V9z"/></svg>',
    play: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg>',
  };

  const attach = (display, text) => {
    const src = parse(text);
    const svg = display && display.querySelector("svg");
    if (!src || !svg || display.dataset.wv) return;
    const marks = [...svg.querySelectorAll('[id^="gmark_"]')];
    const lanesG = svg.querySelector('[id^="lanes_"]');
    const tr = lanesG && /translate\(\s*([-\d.]+)[ ,]+([-\d.]+)/.exec(lanesG.getAttribute("transform") || "");
    if (marks.length < 2 || !tr) return;
    display.dataset.wv = "1";
    const N = marks.length - 1;
    const mhz = Number(src.dvq && src.dvq.mhz) || 0;
    const log = changes(src);

    // the overlay, in the diagram's own box (it scrolls with it on a phone)
    display.classList.add("wv-host");
    const layer = document.createElement("div");
    layer.className = "wv-layer";
    layer.innerHTML =
      '<div class="wv-veil" hidden></div><div class="wv-now" hidden></div><div class="wv-guide" hidden><span></span></div>' +
      '<div class="wv-cur wv-a" hidden></div><div class="wv-cur wv-b" hidden></div><div class="wv-dim" hidden><span></span></div>' +
      '<button type="button" class="wv-knob wv-a" role="slider" aria-label="סמן A" aria-valuemin="0" hidden>A</button>' +
      '<button type="button" class="wv-knob wv-b" role="slider" aria-label="סמן B" aria-valuemin="0" hidden>B</button>';
    display.append(layer);
    const $ = (s) => layer.querySelector(s);
    const tools = document.createElement("div");
    tools.className = "wv-tools";
    tools.setAttribute("data-search-exclude", "");
    tools.innerHTML =
      `<button type="button" class="wv-btn wv-measure" aria-pressed="false">${ICON.measure}מדידה</button>` +
      `<button type="button" class="wv-btn wv-play">${ICON.play}הפעלה</button>` +
      '<p class="wv-read" aria-live="polite"></p>';
    const list = document.createElement("ol");
    list.className = "wv-log";
    list.hidden = true;
    list.setAttribute("data-search-exclude", "");
    list.innerHTML = log.length
      ? log.map((e) => `<li data-t="${e.t}">מחזור ${fmtT(e.t)}${NB}: ${e.items.join(", ")}</li>`).join("")
      : "<li>אין שינויים בגלים שאינם שעון.</li>";
    display.after(tools, list);

    // geometry: the period marks in the overlay's pixels
    let xs = [], y0 = 0, y1 = 0;
    const measure = () => {
      // an <svg> has no offsetLeft: its place in the diagram's box comes from the two rects
      const sr = svg.getBoundingClientRect(), dr = display.getBoundingClientRect();
      const vb = svg.viewBox && svg.viewBox.baseVal, w = sr.width;
      const k = vb && vb.width ? w / vb.width : 1;
      const ox = Number(tr[1]), oy = Number(tr[2]);
      layer.style.left = (sr.left - dr.left + display.scrollLeft) + "px";
      layer.style.top = (sr.top - dr.top + display.scrollTop) + "px";
      layer.style.width = w + "px";
      layer.style.height = sr.height + "px";
      xs = marks.map((m) => (ox + Number(m.getAttribute("x1"))) * k);
      y0 = oy * k;
      y1 = (oy + Number(marks[0].getAttribute("y2"))) * k;
      layer.style.setProperty("--wv-y0", y0 + "px");
      layer.style.setProperty("--wv-y1", y1 + "px");
      paint();
      if (!playing) veil(null);
    };
    const edgeAt = (clientX) => {
      const x = clientX - layer.getBoundingClientRect().left;
      let best = 0;
      xs.forEach((v, i) => { if (Math.abs(v - x) < Math.abs(xs[best] - x)) best = i; });
      return best;
    };

    // ---- measure ----
    const firstTwo = log.filter((e) => Number.isInteger(e.t) && e.t <= N).map((e) => e.t);
    const cur = { a: firstTwo[0] ?? 1, b: firstTwo[1] ?? Math.min(N, (firstTwo[0] ?? 1) + 2) };
    const btnM = tools.querySelector(".wv-measure"), read = tools.querySelector(".wv-read");
    let on = false;
    const paint = () => {
      if (!xs.length) return;
      ["a", "b"].forEach((k) => {
        const x = xs[cur[k]] + "px";
        $(`.wv-cur.wv-${k}`).style.left = x;
        const knob = $(`.wv-knob.wv-${k}`);
        knob.style.left = x;
        knob.setAttribute("aria-valuemax", String(N));
        knob.setAttribute("aria-valuenow", String(cur[k]));
        knob.setAttribute("aria-valuetext", `קצה ${cur[k]}`);
      });
      const lo = Math.min(cur.a, cur.b), hi = Math.max(cur.a, cur.b), d = hi - lo;
      const dim = $(".wv-dim");
      dim.style.left = xs[lo] + "px";
      dim.style.width = (xs[hi] - xs[lo]) + "px";
      dim.classList.toggle("is-zero", d === 0);
      const ns = mhz ? `${NB}·${NB}${+(d * 1000 / mhz).toFixed(2)}ns` : "";
      dim.querySelector("span").textContent = `${cycles(d)}${ns}`;
      if (on) read.textContent = `סמן A${NB}: קצה ${cur.a}. סמן B${NB}: קצה ${cur.b}. ההפרש${NB}: ${cycles(d)}` +
        (mhz ? `, ${+(d * 1000 / mhz).toFixed(2)}ns בשעון של ${mhz}MHz.` : ".");
    };
    const show = (v) => {
      on = v;
      btnM.setAttribute("aria-pressed", String(on));
      display.classList.toggle("wv-measuring", on);
      layer.querySelectorAll(".wv-cur, .wv-knob, .wv-dim").forEach((el) => { el.hidden = !on; });
      if (!on) { read.textContent = ""; $(".wv-guide").hidden = true; }
      measure();
    };
    btnM.addEventListener("click", () => show(!on));
    let drag = null;
    ["a", "b"].forEach((k) => {
      const knob = $(`.wv-knob.wv-${k}`);
      knob.addEventListener("pointerdown", (e) => { e.stopPropagation(); drag = k; knob.setPointerCapture(e.pointerId); });
      knob.addEventListener("pointermove", (e) => { if (drag === k) { cur[k] = edgeAt(e.clientX); paint(); } });
      knob.addEventListener("pointerup", () => { drag = null; });
      knob.addEventListener("keydown", (e) => {
        const d = { ArrowLeft: -1, ArrowDown: -1, ArrowRight: 1, ArrowUp: 1 }[e.key];
        let next = null;
        if (d) next = cur[k] + d;
        else if (e.key === "Home") next = 0;
        else if (e.key === "End") next = N;
        if (next === null) return;
        e.preventDefault();
        cur[k] = Math.max(0, Math.min(N, next));
        paint();
      });
    });
    display.addEventListener("pointermove", (e) => {
      if (!on || drag) return;
      const g = $(".wv-guide"), i = edgeAt(e.clientX);
      g.hidden = false;
      g.style.left = xs[i] + "px";
      g.querySelector("span").textContent = `קצה ${i}`;
    });
    display.addEventListener("pointerleave", () => { $(".wv-guide").hidden = true; });
    display.addEventListener("click", (e) => {
      if (!on || e.target.closest(".wv-knob")) return;
      const i = edgeAt(e.clientX);
      const k = Math.abs(i - cur.a) <= Math.abs(i - cur.b) ? "a" : "b";
      cur[k] = i;
      paint();
    });

    // ---- play ----
    const items = [...list.querySelectorAll("li[data-t]")];
    let playing = false, raf = 0;
    const veil = (t) => {
      const v = $(".wv-veil"), now = $(".wv-now");
      if (t === null) { v.hidden = true; now.hidden = true; return; }
      const x = xs[0] + (xs[N] - xs[0]) * (t / N);
      v.hidden = false; now.hidden = false;
      v.style.left = x + "px";
      v.style.width = Math.max(0, xs[N] - x) + "px";
      now.style.left = x + "px";
      items.forEach((li) => li.classList.toggle("is-on", Number(li.dataset.t) <= t + 1e-6));
    };
    const play = () => {
      list.hidden = false;
      if (reduce) { items.forEach((li) => li.classList.add("is-on")); return; }
      cancelAnimationFrame(raf);
      playing = true;
      list.classList.add("is-playing");
      const t0 = performance.now(), T = N * STEP_MS;
      const step = (now) => {
        const p = Math.min(1, (now - t0) / T);
        veil(p * N);
        if (p < 1) raf = requestAnimationFrame(step);
        else { playing = false; veil(null); list.classList.remove("is-playing"); items.forEach((li) => li.classList.add("is-on")); }
      };
      raf = requestAnimationFrame(step);
    };
    tools.querySelector(".wv-play").addEventListener("click", play);

    if ("ResizeObserver" in window) new ResizeObserver(measure).observe(display);
    measure();
  };

  window.dvqWaveViewer = { attach, changes };
})();
