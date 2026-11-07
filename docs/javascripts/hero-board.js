// The home page hero's background (session 30, in place of the rolling waves): a chip in
// the middle with its fan-out, as on a real board. A pin's wire leaves the chip, steps out
// (the outer pins turn first, so no wire crosses another), spreads and runs to the edge;
// wires only run across and up or down, with small round corners. Amber electrons run
// out of the chip and into it, and a pin lights when one arrives. Every few seconds a
// burst of three or four faster white electrons runs along one wire, like a packet.
//
// The chip sits in .hh-chip-slot, a place the page keeps for it (21-interview.css): a
// column between the text and the interview builder on a wide screen, a strip under the
// numbers otherwise. The wires pass under the builder (they are not drawn in its box) and
// run on to the edge on the text's side, where a soft calm patch under every line of text
// and every control keeps the text clear (drawn once per layout, then stamped each frame). One still frame under reduced motion and in an automated browser
// (the page checks see a still page); the animation runs only while the hero is on screen.
(() => {
  const AMBER = "255,194,51", WHITE = "255,255,255";
  const SPEED = 120;            // pixels per second
  const EVERY = 0.16;           // a new electron every so many seconds
  const BURST = [2.6, 4.2];     // a white burst every so many seconds (a random time between)
  const FAST = 1.7;             // a burst runs this many times faster
  const BUDGET = 60;            // seconds of running before the board stops by itself
  const STOP_KEY = "dvq-hero-still";   // the reader stopped the board: it stays still
  const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches || navigator.webdriver;

  // a polyline of horizontal and vertical steps, with its length
  const route = (pts) => {
    const seg = [];
    let L = 0;
    for (let i = 1; i < pts.length; i++) {
      const d = Math.abs(pts[i][0] - pts[i - 1][0]) + Math.abs(pts[i][1] - pts[i - 1][1]);
      seg.push(d);
      L += d;
    }
    return { pts, seg, L };
  };
  const at = (r, d) => {
    if (d <= 0) return r.pts[0];
    for (let i = 0; i < r.seg.length; i++) {
      if (d <= r.seg[i]) {
        const a = r.pts[i], b = r.pts[i + 1], f = r.seg[i] ? d / r.seg[i] : 0;
        return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f];
      }
      d -= r.seg[i];
    }
    return r.pts[r.pts.length - 1];
  };

  // The chip of side S at (cx, cy), seven pins a side. Each pin: out by its step, then up
  // or down (or across) to its spread, then on to the edge; the text side's wires end in
  // a via a little way in.
  const layout = (cx, cy, S, w, h) => {
    const n = 7, pitch = S / (n + 1), half = S / 2, wires = [], pins = [];
    const step = (i) => (i < 3 ? i : i > 3 ? 6 - i : 3) * Math.max(7, pitch * 0.9) + 10;
    const spread = (i) => (i - 3) * pitch * 2.3;
    for (let i = 0; i < n; i++) {
      const o = -half + pitch * (i + 1);
      let p = [cx - half, cy + o];                                       // the builder's side
      pins.push({ p, horiz: true });
      wires.push(route([p, [p[0] - step(i), p[1]], [p[0] - step(i), cy + spread(i)], [-20, cy + spread(i)]]));
      p = [cx + o, cy - half];                                            // top
      pins.push({ p, horiz: false });
      wires.push(route([p, [p[0], p[1] - step(i)], [cx + spread(i), p[1] - step(i)], [cx + spread(i), -20]]));
      p = [cx + o, cy + half];                                            // bottom
      pins.push({ p, horiz: false });
      wires.push(route([p, [p[0], p[1] + step(i)], [cx + spread(i), p[1] + step(i)], [cx + spread(i), h + 20]]));
      p = [cx + half, cy + o];                                            // the text's side
      pins.push({ p, horiz: true });
      wires.push(route([p, [p[0] + step(i), p[1]], [p[0] + step(i), cy + spread(i) * 0.8], [w + 20, cy + spread(i) * 0.8]]));
    }
    return { wires, pins, cx, cy, S };
  };

  // any CSS colour (the dark hero is a color-mix) as "r,g,b", through a one-pixel canvas
  const toRgb = (css) => {
    const c = document.createElement("canvas");
    c.width = c.height = 1;
    const x = c.getContext("2d");
    x.fillStyle = css;
    x.fillRect(0, 0, 1, 1);
    const [r, g, b] = x.getImageData(0, 0, 1, 1).data;
    return `${r},${g},${b}`;
  };

  const board = (hero, canvas, slot) => {
    const ctx = canvas.getContext("2d");
    let W = 0, H = 0, geo = null, hide = null, calm = null, bg = "rgb(27,42,74)", rgb = "27,42,74";
    let flows = [], lit = new Map(), t = 0, last = 0, spawned = 0, nextBurst = 1.2, running = false, frame = 0;

    const measure = () => {
      const hr = hero.getBoundingClientRect(), d = Math.min(2, window.devicePixelRatio || 1);
      W = hr.width; H = hr.height;
      canvas.width = Math.round(W * d); canvas.height = Math.round(H * d);
      ctx.setTransform(d, 0, 0, d, 0, 0);
      bg = getComputedStyle(hero).backgroundColor || bg;
      rgb = toRgb(bg);
      const local = (r) => ({ x: r.left - hr.left, y: r.top - hr.top, w: r.width, h: r.height });
      const s = local(slot.getBoundingClientRect());
      const column = s.h > s.w;                                           // the middle column, or a strip
      const S = column ? Math.min(78, s.w * 0.5) : Math.min(58, s.h * 0.42);
      geo = layout(s.x + s.w / 2, s.y + s.h / 2, S, W, H);
      const builder = hero.querySelector(".hh-builder:not([hidden])");
      hide = builder ? local(builder.getBoundingClientRect()) : null;
      // the text stays readable: a soft patch of the hero's colour under each line of text and
      // each control, drawn once here on a canvas of its own
      calm = calmMask(hero, hr, d);
      flows = [];
      if (still || !running) seed();
      draw();
    };

    // a few electrons already on their way, for the still frame and the first one
    const seed = () => {
      for (let k = 0; k < 9; k++) flows.push({ i: (k * 11 + 3) % geo.wires.length, t0: t - 0.35 - k * 0.27, dir: k % 2 ? 1 : -1 });
      burst(5, -1, t - 0.6);                                              // and one packet on its way in
    };
    // three or four white electrons close together on one wire, faster than the rest
    const burst = (i, dir, t0) => {
      const n = 3 + (Math.random() < 0.5 ? 1 : 0);
      for (let k = 0; k < n; k++) flows.push({ i, t0: t0 + k * 0.075, dir, v: FAST, white: true });
    };
    const calmMask = (root, hr, d) => {
      const c = document.createElement("canvas");
      c.width = canvas.width; c.height = canvas.height;
      const x = c.getContext("2d");
      x.setTransform(d, 0, 0, d, 0, 0);
      x.fillStyle = `rgb(${rgb})`; x.shadowColor = `rgb(${rgb})`; x.shadowBlur = 14;
      const patch = (r, px, py) => { x.beginPath(); x.roundRect(r.left - hr.left - px, r.top - hr.top - py, r.width + 2 * px, r.height + 2 * py, 6); x.fill(); };
      root.querySelectorAll(":scope > :is(h1, p)").forEach((el) => {
        const range = document.createRange();
        range.selectNodeContents(el);
        Array.from(range.getClientRects()).forEach((r) => patch(r, 8, 3));
      });
      root.querySelectorAll(".hh-tools :is(.hh-actions > *, .hh-search, .hh-suggest > *, .hh-stats > *)").forEach((el) => patch(el.getBoundingClientRect(), 6, 4));
      return c;
    };

    const stroke = (pts) => {
      ctx.beginPath();
      ctx.moveTo(pts[0][0], pts[0][1]);
      for (let i = 1; i < pts.length - 1; i++) ctx.arcTo(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 4);
      ctx.lineTo(pts[pts.length - 1][0], pts[pts.length - 1][1]);
      ctx.stroke();
    };
    const electron = (r, d, dir, col) => {
      const head = at(r, d);
      const g = ctx.createRadialGradient(head[0], head[1], 0, head[0], head[1], 9);
      g.addColorStop(0, `rgba(${col},0.45)`);
      g.addColorStop(1, `rgba(${col},0)`);
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(head[0], head[1], 9, 0, 7); ctx.fill();
      for (let k = 14; k >= 0; k--) {
        const dd = d - dir * k * 2.6;
        if (dd < 0 || dd > r.L) continue;
        const p = at(r, dd);
        ctx.fillStyle = `rgba(${col},${(Math.pow(1 - k / 15, 1.6) * 0.95).toFixed(3)})`;
        ctx.beginPath(); ctx.arc(p[0], p[1], 2.3 - k * 0.09, 0, 7); ctx.fill();
      }
    };

    const draw = () => {
      ctx.clearRect(0, 0, W, H);
      ctx.save();
      if (hide) {                                                         // not under the builder
        ctx.beginPath();
        ctx.rect(0, 0, W, H);
        ctx.rect(hide.x - 2, hide.y - 2, hide.w + 4, hide.h + 4);
        ctx.clip("evenodd");
      }
      ctx.lineJoin = "round"; ctx.lineCap = "round";
      ctx.strokeStyle = `rgba(${WHITE},0.13)`; ctx.lineWidth = 1.6;
      geo.wires.forEach((r) => stroke(r.pts));
      ctx.strokeStyle = `rgba(${WHITE},0.2)`; ctx.lineWidth = 1.2;
      geo.wires.forEach((r) => {
        const e = r.pts[r.pts.length - 1];
        if (e[0] > 0 && e[0] < W && e[1] > 0 && e[1] < H) { ctx.beginPath(); ctx.arc(e[0], e[1], 3.2, 0, 7); ctx.stroke(); }
      });
      // electrons
      flows = flows.filter((f) => {
        const r = geo.wires[f.i], s = (t - f.t0) * SPEED * (f.v || 1);
        if (s > r.L) { if (f.dir < 0) lit.set(f.i, t + 0.6); return false; }
        if (s >= 0) electron(r, f.dir > 0 ? s : r.L - s, f.dir, f.white ? WHITE : AMBER);
        return true;
      });
      // the calm patches under the text, then the chip over everything
      if (calm) { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(calm, 0, 0); ctx.restore(); }
      // the pins, then the chip (no marking on it)
      geo.pins.forEach(({ p, horiz }, i) => {
        const l = Math.max(0, (lit.get(i) || 0) - t);
        ctx.fillStyle = l > 0 ? `rgba(${AMBER},${(0.35 + 0.6 * l).toFixed(3)})` : `rgba(${WHITE},0.32)`;
        ctx.fillRect(p[0] - (horiz ? 4 : 1.6), p[1] - (horiz ? 1.6 : 4), horiz ? 8 : 3.2, horiz ? 3.2 : 8);
      });
      const glow = Math.min(1, Math.max(0, ...Array.from(lit.values(), (v) => v - t)));
      const { cx, cy, S } = geo, x = cx - S / 2, y = cy - S / 2;
      ctx.fillStyle = bg; ctx.beginPath(); ctx.roundRect(x, y, S, S, 5); ctx.fill();
      ctx.fillStyle = `rgba(${WHITE},0.06)`; ctx.strokeStyle = `rgba(${WHITE},0.28)`; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.roundRect(x, y, S, S, 5); ctx.fill(); ctx.stroke();
      ctx.strokeStyle = `rgba(${WHITE},0.09)`;
      ctx.beginPath(); ctx.roundRect(x + 7, y + 7, S - 14, S - 14, 3); ctx.stroke();
      ctx.fillStyle = `rgba(${WHITE},0.2)`;
      ctx.beginPath(); ctx.arc(x + 10, y + 10, 2.2, 0, 7); ctx.fill();
      if (glow > 0) {
        ctx.strokeStyle = `rgba(${AMBER},${(0.6 * glow).toFixed(3)})`; ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.roundRect(x - 1, y - 1, S + 2, S + 2, 6); ctx.stroke();
      }
      ctx.restore();
    };

    const tick = (now) => {
      if (!running) return;
      const dt = last ? Math.min(0.05, (now - last) / 1000) : 0;
      last = now;
      t += dt;
      if (t - budgetFrom > BUDGET) { stop(false); return; }     // a minute, then a still frame
      if (t - spawned > EVERY) {
        spawned = t;
        flows.push({ i: Math.floor(Math.random() * geo.wires.length), t0: t, dir: Math.random() < 0.5 ? 1 : -1 });
      }
      if (t > nextBurst) {
        nextBurst = t + BURST[0] + Math.random() * (BURST[1] - BURST[0]);
        burst(Math.floor(Math.random() * geo.wires.length), Math.random() < 0.6 ? -1 : 1, t);
      }
      draw();
      frame = requestAnimationFrame(tick);
    };
    const play = (on) => {
      on = on && seen && !paused;
      if (still || on === running) return;
      running = on;
      last = 0;
      if (on) frame = requestAnimationFrame(tick);
      else cancelAnimationFrame(frame);
    };

    // WCAG 2.2.2: the moving board can be stopped. A button in the hero's corner stops and
    // starts it (a stop chosen by the reader is remembered in this browser), and the board
    // also stops by itself after BUDGET seconds of running; starting it again gives it
    // another BUDGET. Under reduced motion there is no motion and no button.
    let seen = false, paused = false, budgetFrom = 0;
    const pauseBtn = document.createElement("button");
    pauseBtn.type = "button";
    pauseBtn.className = "hh-pause";
    const label = () => {
      pauseBtn.setAttribute("aria-label", paused ? "הפעלת האנימציה של הלוח" : "עצירת האנימציה של הלוח");
      pauseBtn.dataset.tip = pauseBtn.getAttribute("aria-label");
      pauseBtn.classList.toggle("is-paused", paused);
    };
    const stop = (chosen) => {
      paused = true;
      if (chosen) { try { localStorage.setItem(STOP_KEY, "1"); } catch (e) { /* storage off */ } }
      label();
      play(false);
    };
    pauseBtn.addEventListener("click", () => {
      if (!paused) { stop(true); return; }
      paused = false;
      budgetFrom = t;
      try { localStorage.removeItem(STOP_KEY); } catch (e) { /* storage off */ }
      label();
      play(true);
    });
    try { paused = localStorage.getItem(STOP_KEY) === "1"; } catch (e) { /* storage off */ }
    if (!still) { label(); hero.append(pauseBtn); }

    new ResizeObserver(measure).observe(hero);
    // the builder appears once the question list has loaded, which moves the slot
    const builder = hero.querySelector(".hh-builder");
    if (builder) new MutationObserver(measure).observe(builder, { attributes: true, attributeFilter: ["hidden"] });
    // the hero's colour follows the light / dark switch
    new MutationObserver(measure).observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
    new IntersectionObserver((entries) => { seen = entries.some((e) => e.isIntersecting); play(seen); }).observe(hero);
    // the calm patches follow the text, whose lines move once the web font is in
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
    measure();
  };

  document.addEventListener("DOMContentLoaded", () => {
    const hero = document.querySelector(".home-hero");
    const canvas = hero && hero.querySelector("canvas.hh-board");
    const slot = hero && hero.querySelector(".hh-chip-slot");
    if (!canvas || !slot || !canvas.getContext || !("ResizeObserver" in window)) return;
    board(hero, canvas, slot);
  });
})();
