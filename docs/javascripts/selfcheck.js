// Self-checks (V4): a short question on a page, before the solution, whose answer is a
// number. The page writes
//   <div class="selfcheck" data-answer="13/27" data-show="13/27 ≈ 0.481" data-hint="..." markdown>
//   the question
//   </div>
// and this file adds a field, a check button, the reply and, after a wrong answer, the
// hint and a button that shows the answer. A right answer is remembered per page in the
// browser (a ✓ on the next visit); it does not mark the question solved. tools/lint_pages.py
// checks the attributes, and tests/tools/test_selfcheck.py checks every answer.
(() => {
  const STORE = "dvq-check";
  const NB = " ";
  // "17", "2.5", "2,872", "1/3", "−0.5" -> a number, or NaN
  const parse = (text) => {
    const t = String(text).trim().replace(/[\s,]/g, "").replace(/[−–]/g, "-");
    const m = /^(-?\d*\.?\d+)\/(\d*\.?\d+)$/.exec(t);
    if (m) return Number(m[2]) ? Number(m[1]) / Number(m[2]) : NaN;
    return /^-?\d*\.?\d+$/.test(t) ? Number(t) : NaN;
  };
  // a whole answer is exact; a fraction or a decimal takes three decimal places
  const same = (got, want) => (Number.isInteger(want) ? got === want : Math.abs(got - want) <= Math.max(5e-4, Math.abs(want) * 1e-3));
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k) { try { localStorage.setItem(k, "1"); } catch (e) { /* storage off */ } },
  };
  const mount = (box, i) => {
    const want = parse(box.dataset.answer), key = `${STORE}:${location.pathname}:${i}`;
    const show = box.dataset.show || box.dataset.answer;
    const tag = document.createElement("p");
    tag.className = "selfcheck__tag";
    tag.textContent = "בדקו את עצמכם";
    box.prepend(tag);
    const row = document.createElement("div");
    row.className = "selfcheck__row";
    row.innerHTML = `<input type="text" class="selfcheck__in" inputmode="decimal" dir="ltr" spellcheck="false" aria-label="התשובה שלכם, מספר">` +
      `<button type="button" class="md-button md-button--primary selfcheck__go">בדיקה</button>` +
      `<button type="button" class="md-button selfcheck__show" hidden>הצגת התשובה</button>`;
    const msg = document.createElement("p");
    msg.className = "selfcheck__msg";
    msg.setAttribute("role", "status");
    box.append(row, msg);
    const input = row.querySelector("input"), go = row.querySelector(".selfcheck__go"), reveal = row.querySelector(".selfcheck__show");
    const say = (cls, html) => { msg.className = `selfcheck__msg ${cls}`; msg.innerHTML = html; };
    const check = () => {
      const got = parse(input.value);
      if (Number.isNaN(got)) { say("is-info", "הקלידו מספר, למשל ‎17‎, ‎2.5‎ או ‎1/3‎."); return; }
      if (same(got, want)) {
        say("is-ok", `✓ נכון. ההסבר בפתרון שלמטה.`);
        box.classList.add("is-done");
        reveal.hidden = true;
        store.set(key);
        return;
      }
      say("is-bad", `לא נכון. רמז${NB}: ${box.dataset.hint}`);
      reveal.hidden = false;
    };
    go.addEventListener("click", check);
    input.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); check(); } });
    reveal.addEventListener("click", () => say("is-info", `התשובה${NB}: <bdi dir="ltr">${show}</bdi>. ההסבר בפתרון שלמטה.`));
    if (store.get(key)) { box.classList.add("is-done"); say("is-ok", "✓ עניתם נכון בביקור קודם."); }
  };
  document.addEventListener("DOMContentLoaded", () => document.querySelectorAll(".selfcheck").forEach(mount));
})();
