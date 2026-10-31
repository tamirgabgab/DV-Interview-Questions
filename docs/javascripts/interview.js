// Interview mode and the quick jump (session 30): the shared functions and the question
// index. question-tools.js (interview mode), home.js (the interview builder),
// home-extras.js (my map) and quick-jump.js use window.dvqInterview; the pure functions are
// tested under Node (tests/tools/test_interview.py), which requires this file.
//
// The index is questions.json at the site root (hooks/questions.py, on_post_build):
//   {"levels": {...}, "diffs": {...}, "kinds": {...},
//    "qs": [[id, title, level, difficulty, kind, [topic names], url from the root, parts]]}
(function (root) {
  "use strict";
  const ID = 0, TITLE = 1, LEVEL = 2, DIFF = 3, KIND = 4, TAGS = 5, URL_ = 6, PARTS = 7;

  // The time an interviewer would give a question: by its difficulty, and a little more
  // for every part beyond the third.
  const TARGET = { easy: 10, medium: 15, hard: 25 };
  const PART_EXTRA = 3;
  const targetMinutes = (difficulty, parts) =>
    (TARGET[difficulty] || TARGET.medium) + PART_EXTRA * Math.max(0, (Number(parts) || 0) - 3);

  // mulberry32: a small seeded generator, so one seed always gives the same series
  const rng = (seed) => {
    let a = (Number(seed) >>> 0) || 1;
    return () => {
      a = (a + 0x6d2b79f5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  };

  // A series of questions for an interview: the level's questions of the chosen kinds in a
  // seeded random order, the ones not solved yet first, taken while they fit the minutes.
  // When none fits, the shortest one alone (a series is never empty while the pool is not).
  const buildPlan = (qs, opts) => {
    const { level, minutes, kinds, solved = [], seed = 1 } = opts;
    const done = new Set(solved);
    const r = rng(seed);
    const pool = qs.filter((q) => q[LEVEL] === level && kinds.includes(q[KIND]))
      .map((q) => [r(), q]).sort((a, b) => a[0] - b[0]).map((x) => x[1]);
    const ordered = pool.filter((q) => !done.has(q[ID])).concat(pool.filter((q) => done.has(q[ID])));
    const plan = [];
    let used = 0;
    for (const q of ordered) {
      const m = targetMinutes(q[DIFF], q[PARTS]);
      if (used + m <= minutes) { plan.push(q); used += m; }
    }
    if (!plan.length && pool.length) {
      const q = pool.reduce((a, b) => (targetMinutes(b[DIFF], b[PARTS]) < targetMinutes(a[DIFF], a[PARTS]) ? b : a));
      plan.push(q);
      used = targetMinutes(q[DIFF], q[PARTS]);
    }
    return { plan, minutes: used };
  };

  // The quick jump: questions that match what was typed, best first. A number finds the
  // question with that id (59 -> 0059) and then the ids that contain it; words find
  // titles and topic names (every word has to appear, the title counts more).
  const norm = (s) => String(s).toLowerCase()
    .replace(/[֑-ׇ]/g, "")                          // Hebrew points
    .replace(/[-־‐-―_'"׳״`]/g, " ")   // dashes, maqaf, quotes, geresh
    .replace(/\s+/g, " ").trim();
  const score = (q, text) => {
    if (/^\d+$/.test(text)) {
      if (q[ID] === text.padStart(4, "0")) return 100;
      return q[ID].includes(text) ? 60 : 0;
    }
    const title = norm(q[TITLE]), tags = q[TAGS].map(norm), words = text.split(" ");
    if (title.startsWith(text)) return 50;
    if (title.includes(text)) return 45;
    if (tags.includes(text)) return 40;
    if (tags.some((t) => t.includes(text))) return 30;
    if (words.every((w) => title.includes(w))) return 25;
    if (words.every((w) => title.includes(w) || tags.some((t) => t.includes(w)))) return 15;
    return 0;
  };
  const match = (qs, query, limit = 8) => {
    const text = norm(query);
    if (!text) return [];
    return qs.map((q) => [score(q, text), q]).filter((x) => x[0] > 0)
      .sort((a, b) => b[0] - a[0] || (a[1][ID] < b[1][ID] ? -1 : 1))
      .slice(0, limit).map((x) => x[1]);
  };

  const fmt = (secs) => {
    const s = Math.max(0, Math.floor(secs));
    return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
  };

  // ---- browser only: the index, the series and the last interview of each question ----
  const store = {
    get(k) { try { return JSON.parse(root.localStorage.getItem(k) || "null"); } catch (e) { return null; } },
    set(k, v) { try { root.localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* storage off */ } },
    del(k) { try { root.localStorage.removeItem(k); } catch (e) { /* storage off */ } },
  };
  // the site root, from Material's config (relative to this page)
  const siteRoot = () => {
    let base = ".";
    try { base = JSON.parse(root.document.getElementById("__config").textContent).base || "."; } catch (e) { /* default */ }
    return new URL(base.replace(/\/?$/, "/"), root.location.href);
  };
  const siteUrl = (rel) => new URL(rel, siteRoot()).href;
  let index = null;
  const loadIndex = () => {
    if (!index) {
      index = root.fetch(siteUrl("questions.json"))
        .then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))))
        .catch((e) => { index = null; throw e; });
    }
    return index;
  };

  // The series of an interview: {ids, urls, i, minutes}; urls are absolute.
  const PLAN = "dvq-plan";
  const plan = {
    get: () => store.get(PLAN),
    set: (p) => store.set(PLAN, p),
    clear: () => store.del(PLAN),
  };
  // The last interview of a question: {at, secs, target, hints, right, checks, conf}
  const LAST = "dvq-interview:";
  const last = {
    get: (id) => store.get(LAST + id),
    set: (id, v) => store.set(LAST + id, v),
  };

  const api = { ID, TITLE, LEVEL, DIFF, KIND, TAGS, URL: URL_, PARTS, TARGET, PART_EXTRA,
    targetMinutes, rng, buildPlan, norm, match, fmt, loadIndex, siteUrl, plan, last };
  root.dvqInterview = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);
