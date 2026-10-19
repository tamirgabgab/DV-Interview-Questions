// Interactive cake split of questions 0027 and 0028: sliders for a and d (arithmetic
// fractions) or a and q (geometric fractions), the bars of the shares S(k) with the largest
// one highlighted, and the fractions p(k) against the threshold T. The math functions are
// exported under Node, where tests/0027 checks them against the Python reference.
(() => {
  const EPS = 1e-9;

  // Rows {k, p, R, S}: person k takes p of what is left (R); a fraction of 1 or more takes
  // the rest and ends the split.
  const split = (kind, a, step) => {
    const rows = [];
    let R = 1;
    for (let k = 1; k <= 2000; k++) {
      const raw = kind === "arith" ? a + (k - 1) * step : a * Math.pow(step, k - 1);
      const p = Math.min(raw, 1);
      rows.push({ k, p, R, S: p * R });
      if (p >= 1) break;
      R *= 1 - p;
    }
    return rows;
  };

  const threshold = (kind, step) =>
    kind === "arith" ? (Math.sqrt(step * step + 4 * step) - step) / 2 : 1 - 1 / step;

  // The page's closed form: the first person whose fraction reaches T; a tie with the next
  // person when the fraction equals T.
  const formula = (kind, a, step) => {
    const T = threshold(kind, step);
    const x = kind === "arith" ? (T - a) / step + 1 : Math.log((step - 1) / a) / Math.log(step);
    const k = Math.max(1, Math.ceil(x - EPS));
    const pk = kind === "arith" ? a + (k - 1) * step : a * Math.pow(step, k - 1);
    return { k, tie: Math.abs(pk - T) < EPS };
  };

  // The largest share in the rows themselves (both people on a tie).
  const best = (rows) => {
    const top = Math.max(...rows.map((r) => r.S));
    return rows.filter((r) => Math.abs(r.S - top) <= EPS * top).map((r) => r.k);
  };

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { split, threshold, formula, best };
    return;
  }

  const fmt = (v, n = 3) => Number(v).toFixed(n);

  const bars = (rows, peak) => {
    const w = 640, h = 230, x0 = 46, right = 12, top = 14, base = 198;
    const smax = Math.max(...rows.map((r) => r.S));
    const ymax = Math.ceil(smax * 20 + 0.6) / 20;
    const slot = (w - x0 - right) / rows.length;
    const Y = (v) => base - (v / ymax) * (base - top);
    const tickEvery = Math.ceil(rows.length / 16);
    let s = `<svg class="perf-chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="החלק של כל אדם">`;
    for (let v = 0; v <= ymax + 1e-9; v += 0.05) {
      s += `<line class="grid" x1="${x0}" x2="${w - right}" y1="${Y(v).toFixed(1)}" y2="${Y(v).toFixed(1)}"/>` +
           `<text class="tick" x="${x0 - 8}" y="${(Y(v) + 4).toFixed(1)}" text-anchor="end">${v.toFixed(2)}</text>`;
    }
    rows.forEach((r) => {
      const cx = x0 + (r.k - 0.5) * slot, bw = Math.max(slot * 0.68, 1);
      const cls = peak.includes(r.k) ? "by-enum" : "by-multiples";
      s += `<rect class="bar ${cls}" x="${(cx - bw / 2).toFixed(1)}" y="${Y(r.S).toFixed(1)}" width="${bw.toFixed(1)}" ` +
           `height="${(base - Y(r.S)).toFixed(1)}"><title>S(${r.k}) = ${fmt(r.S, 4)}</title></rect>`;
      if (r.k % tickEvery === 0 || r.k === 1 || peak.includes(r.k)) {
        s += `<text class="tick" x="${cx.toFixed(1)}" y="${base + 18}" text-anchor="middle">${r.k}</text>`;
      }
    });
    return s + `<line class="axis" x1="${x0}" x2="${w - right}" y1="${base}" y2="${base}"/></svg>`;
  };

  const fractions = (rows, T, peak) => {
    const w = 640, h = 230, x0 = 46, right = 12, top = 14, base = 198;
    const slot = (w - x0 - right) / rows.length;
    const Y = (v) => base - v * (base - top);
    const tickEvery = Math.ceil(rows.length / 16);
    let s = `<svg class="perf-chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="השבר של כל אדם מול הסף">`;
    [0, 0.25, 0.5, 0.75, 1].forEach((v) => {
      s += `<line class="grid" x1="${x0}" x2="${w - right}" y1="${Y(v).toFixed(1)}" y2="${Y(v).toFixed(1)}"/>` +
           `<text class="tick" x="${x0 - 8}" y="${(Y(v) + 4).toFixed(1)}" text-anchor="end">${v}</text>`;
    });
    s += `<line class="ink-line" x1="${x0}" x2="${w - right}" y1="${Y(T).toFixed(1)}" y2="${Y(T).toFixed(1)}" ` +
         `stroke-width="1.5" stroke-dasharray="6 4"/>` +
         `<text class="legend" x="${x0 + 6}" y="${(Y(T) - 6).toFixed(1)}">T ≈ ${fmt(T)}</text>`;
    rows.forEach((r) => {
      const cx = x0 + (r.k - 0.5) * slot;
      const cls = r.k === peak[0] ? "s2" : r.p < T - EPS ? "s1" : "ink";
      s += `<line class="${cls}-line" x1="${cx.toFixed(1)}" x2="${cx.toFixed(1)}" y1="${base}" y2="${Y(r.p).toFixed(1)}" ` +
           `stroke-width="${Math.min(2, slot * 0.4).toFixed(1)}"/>` +
           `<circle class="${cls}-dot" cx="${cx.toFixed(1)}" cy="${Y(r.p).toFixed(1)}" ` +
           `r="${r.k === peak[0] ? 6 : Math.min(4.5, Math.max(1.5, slot * 0.35)).toFixed(1)}"><title>p(${r.k}) = ${fmt(r.p, 4)}</title></circle>`;
      if (r.k % tickEvery === 0 || r.k === 1 || r.k === peak[0]) {
        s += `<text class="tick" x="${cx.toFixed(1)}" y="${base + 18}" text-anchor="middle">${r.k}</text>`;
      }
    });
    return s + `<line class="axis" x1="${x0}" x2="${w - right}" y1="${base}" y2="${base}"/></svg>`;
  };

  const SLIDERS = {
    arith: [
      { key: "a", label: "השבר הראשון a", min: 0.005, max: 0.6, step: 0.005 },
      { key: "step", label: "ההפרש d", min: 0.01, max: 0.5, step: 0.01 },
    ],
    geo: [
      { key: "a", label: "השבר הראשון a", min: 0.001, max: 0.5, step: 0.001 },
      { key: "step", label: "המנה q", min: 1.05, max: 2, step: 0.05 },
    ],
  };

  const setup = (box) => {
    const kind = box.dataset.kind === "geo" ? "geo" : "arith";
    const state = { a: Number(box.dataset.a), step: Number(box.dataset.step) };
    const controls = document.createElement("div");
    controls.className = "ce-controls";
    const outputs = {};
    SLIDERS[kind].forEach((sl) => {
      const label = document.createElement("label");
      const id = `ce-${kind}-${sl.key}-${Math.random().toString(36).slice(2, 7)}`;
      label.htmlFor = id;
      label.innerHTML = `<span>${sl.label}</span>`;
      const input = document.createElement("input");
      Object.assign(input, { type: "range", id, min: sl.min, max: sl.max, step: sl.step, value: state[sl.key] });
      input.dir = "ltr";
      const out = document.createElement("output");
      out.htmlFor = id;
      outputs[sl.key] = out;
      input.addEventListener("input", () => { state[sl.key] = Number(input.value); draw(); });
      label.append(input, out);
      controls.append(label);
    });
    const reset = document.createElement("button");
    reset.type = "button";
    reset.className = "md-button ce-reset";
    reset.textContent = "חזרה לערכים של השאלה";
    reset.addEventListener("click", () => {
      state.a = Number(box.dataset.a);
      state.step = Number(box.dataset.step);
      controls.querySelectorAll("input").forEach((inp, i) => { inp.value = state[SLIDERS[kind][i].key]; });
      draw();
    });
    controls.append(reset);
    const summary = document.createElement("p");
    summary.className = "ce-summary";
    summary.setAttribute("aria-live", "polite");
    const charts = document.createElement("div");
    charts.className = "ce-charts";
    box.append(controls, summary, charts);

    const draw = () => {
      outputs.a.textContent = String(state.a);
      outputs.step.textContent = String(state.step);
      const rows = split(kind, state.a, state.step);
      const peak = best(rows);
      const T = threshold(kind, state.step);
      const f = formula(kind, state.a, state.step);
      const who = peak.length > 1 ? `תיקו בין האדם ה-${peak[0]} לאדם ה-${peak[1]}` : `האדם ה-${peak[0]}`;
      const agree = f.k === peak[0] && f.tie === (peak.length > 1);
      summary.textContent = `המקבל הגדול: ${who}, עם ${fmt(rows[peak[0] - 1].S)} מהעוגה, מתוך ${rows.length} אנשים. ` +
        `הסף הוא T ≈ ${fmt(T)}, והנוסחה נותנת את האדם ה-${f.k}${f.tie ? " (תיקו עם הבא)" : ""}` +
        `${agree ? ", בדיוק כמו בעמודות." : ", שלא כמו בעמודות."}`;
      charts.innerHTML = `<p class="ce-title">החלק של כל אדם</p>${bars(rows, peak)}` +
        `<p class="ce-title">השבר של כל אדם מול הסף</p>${fractions(rows, T, peak)}`;
    };
    draw();
  };

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".cake-explorer").forEach(setup);
  });
})();
