// The circuit layer (session 32, 22-circuit.css).
//
// - Section dividers (<hr>) are drawn as a data line; the first time one comes into view it
//   gets .is-on, and the stylesheet runs a short bright packet along it once (its length,
//   --cx-run, is the divider's width).
// - A wireframe icosahedron sits in a corner of the home hero and of a level page's header
//   band (still since session 33; ICO_STILL turns it on again): twelve vertices (0, ±1, ±φ) and their cyclic shifts, the thirty edges
//   of length 2, drawn on a canvas in the canvas's CSS colour (22-circuit.css; nothing is
//   hard-coded here). It leans a little toward the pointer, runs only while on screen, and
//   is one still frame under reduced motion and in an automated browser.
(() => {
  const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches || navigator.webdriver;

  // --- the dividers ---------------------------------------------------------------------------
  const dividers = () => {
    const hrs = Array.from(document.querySelectorAll(".md-typeset hr"));
    if (!hrs.length || still || !("IntersectionObserver" in window)) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        const hr = e.target;
        hr.style.setProperty("--cx-run", `${Math.max(0, hr.clientWidth)}px`);
        hr.classList.add("is-on");
        io.unobserve(hr);
      });
    }, { rootMargin: "0px 0px -15% 0px" });
    hrs.forEach((hr) => io.observe(hr));
  };

  // --- the icosahedron ------------------------------------------------------------------------
  const PHI = (1 + Math.sqrt(5)) / 2;
  const VERTS = [];
  for (const [a, b] of [[1, PHI], [1, -PHI], [-1, PHI], [-1, -PHI]]) {
    VERTS.push([0, a, b], [a, b, 0], [b, 0, a]);
  }
  const EDGES = [];
  for (let i = 0; i < VERTS.length; i++) {
    for (let j = i + 1; j < VERTS.length; j++) {
      const d = Math.hypot(VERTS[i][0] - VERTS[j][0], VERTS[i][1] - VERTS[j][1], VERTS[i][2] - VERTS[j][2]);
      if (Math.abs(d - 2) < 1e-6) EDGES.push([i, j]);
    }
  }
  const R = Math.hypot(1, PHI);              // the circumradius, to fit the canvas
  const ICO_STILL = true;                    // drawn once, not turning (session 33)

  const rotate = ([x, y, z], ax, ay) => {    // about y, then about x
    const cy = Math.cos(ay), sy = Math.sin(ay), cx = Math.cos(ax), sx = Math.sin(ax);
    const x1 = x * cy + z * sy, z1 = -x * sy + z * cy;
    return [x1, y * cx - z1 * sx, y * sx + z1 * cx];
  };

  const icosahedron = (host) => {
    const canvas = document.createElement("canvas");
    canvas.className = "cx-ico";
    canvas.setAttribute("aria-hidden", "true");
    host.prepend(canvas);
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    let w = 0, h = 0, dpr = 1, ax = 0.42, ay = 0.6, tx = 0, ty = 0, lx = 0, ly = 0, last = 0, raf = 0, on = false;

    const size = () => {
      dpr = Math.min(2, window.devicePixelRatio || 1);
      w = canvas.clientWidth;
      h = canvas.clientHeight;
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
    };
    const draw = () => {
      if (!w || !h) return;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, w, h);
      const s = (Math.min(w, h) / 2) * 0.86 / R, cx = w / 2, cy = h / 2;
      const pts = VERTS.map((v) => {
        const [x, y, z] = rotate(v, ax + ly, ay + lx);
        const k = 1 + z * 0.12;                  // a little perspective
        return [cx + x * s * k, cy + y * s * k, z];
      });
      const ink = getComputedStyle(canvas).color;
      ctx.strokeStyle = ink;
      ctx.fillStyle = ink;
      ctx.lineCap = "round";
      EDGES.forEach(([i, j]) => {
        const back = pts[i][2] + pts[j][2] < 0;  // the far edges fainter
        ctx.globalAlpha = back ? 0.45 : 1;
        ctx.lineWidth = back ? 1 : 1.6;
        ctx.beginPath();
        ctx.moveTo(pts[i][0], pts[i][1]);
        ctx.lineTo(pts[j][0], pts[j][1]);
        ctx.stroke();
      });
      ctx.globalAlpha = 1;
      pts.forEach(([x, y, z]) => {             // the vertices as vias
        ctx.beginPath();
        ctx.arc(x, y, z > 0 ? 3 : 2, 0, Math.PI * 2);
        ctx.fill();
      });
    };
    const frame = (t) => {
      const dt = last ? Math.min(0.05, (t - last) / 1000) : 0;
      last = t;
      ay += dt * 0.07;
      ax += dt * 0.025;
      lx += (tx - lx) * Math.min(1, dt * 2.5);  // ease toward the pointer's lean
      ly += (ty - ly) * Math.min(1, dt * 2.5);
      draw();
      raf = on ? requestAnimationFrame(frame) : 0;
    };
    const play = (yes) => {
      if (still || yes === on) return;
      on = yes;
      last = 0;
      if (on && !raf) raf = requestAnimationFrame(frame);
    };

    size();
    draw();
    // session 33 (the motion budget of the home page): the board of the hero is the one
    // thing that moves by itself, so the icosahedron is a still drawing everywhere; it keeps
    // its size with the canvas. The turning and the lean toward the pointer stay below.
    if ("ResizeObserver" in window) new ResizeObserver(() => { size(); draw(); }).observe(canvas);
    if (ICO_STILL || still || !canvas.clientWidth) return;        // a still frame, or hidden (a phone)
    host.addEventListener("pointermove", (e) => {
      const r = host.getBoundingClientRect();
      tx = ((e.clientX - r.left) / Math.max(1, r.width) - 0.5) * 0.5;
      ty = ((e.clientY - r.top) / Math.max(1, r.height) - 0.5) * 0.5;
    }, { passive: true });
    host.addEventListener("pointerleave", () => { tx = 0; ty = 0; }, { passive: true });
    if ("IntersectionObserver" in window) new IntersectionObserver((entries) => play(entries.some((e) => e.isIntersecting))).observe(host);
    else play(true);
  };

  document.addEventListener("DOMContentLoaded", () => {
    dividers();
    document.querySelectorAll(".md-typeset .home-hero, .md-typeset .list-band.lb-level").forEach(icosahedron);
  });
})();
