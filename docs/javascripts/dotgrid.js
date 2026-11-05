// The pad field of the home hero and the level bands (24-living.css, item 7).
//
// Each navy band gets a layer of solder pads: a faint still field in its end corner, drawn
// by CSS alone. With a mouse (a fine pointer that can hover), the pads around the pointer
// light up: this script only moves the light's centre (--lv-x, --lv-y, once per frame at
// most) and marks the layer .is-lit while the pointer is over the band. Nothing runs on
// its own, so there is nothing to pause off screen; on a touch screen, under reduced motion
// and in an automated browser (the page checks) the field stays still.
(() => {
  const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches || navigator.webdriver;
  const mouse = window.matchMedia("(hover: hover) and (pointer: fine)");

  const field = (host) => {
    const dots = document.createElement("span");
    dots.className = "lv-dots";
    dots.setAttribute("aria-hidden", "true");
    host.prepend(dots);
    if (still) return;
    let x = 0, y = 0, raf = 0;
    const place = () => {
      raf = 0;
      dots.style.setProperty("--lv-x", `${x}px`);
      dots.style.setProperty("--lv-y", `${y}px`);
      dots.classList.add("is-lit");
    };
    host.addEventListener("pointermove", (e) => {
      if (e.pointerType !== "mouse" || !mouse.matches) return;
      const r = host.getBoundingClientRect();
      x = e.clientX - r.left;
      y = e.clientY - r.top;
      if (!raf) raf = requestAnimationFrame(place);
    }, { passive: true });
    host.addEventListener("pointerleave", () => {
      if (raf) cancelAnimationFrame(raf);
      raf = 0;
      dots.classList.remove("is-lit");
    }, { passive: true });
  };

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".md-typeset .home-hero, .md-typeset .list-band.lb-level").forEach(field);
  });
})();
