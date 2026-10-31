#!/usr/bin/env python3
"""Figures and tables of question 0063 (the maximum of every window of size k with a
monotonic deque, the longest window whose max - min is at most a limit, and a module that
gives the maximum of the last K samples every cycle).

    python tools/figures/fill.py 63        # put the blocks on the page

The references here are independent of the page code: brute_max() and brute_limit() try
every window, trace_max() and trace_limit() replay the deques event by event (the rows of
the tables and the frames of the slidemax explorer), hw_trace() is the cycle model of the
module with K entries, and van_herk() the block method of the follow-up with its count of
comparisons. blocks() returns, in page order: the deque after every index of part a's
example with its legend, the table of part a's steps, the table of part b's steps, the
block diagram of part c and the table of part c's cycles.
"""

RLM = "‏"
NUMS = [1, 3, -1, -3, 5, 3, 6, 7]
K = 3
NUMS_B = [10, 1, 2, 4, 7, 2]
LIMIT = 5
STREAM = [9, 7, 5, 3, 6, 2, 8, 1]
K_HW = 3


def brute_max(nums, k):
    """The maximum of every window of k consecutive values, every window scanned."""
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]


def brute_limit(nums, limit):
    """The longest window whose max - min is at most limit, every window tried."""
    best = 0
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            w = nums[i:j + 1]
            if max(w) - min(w) <= limit:
                best = max(best, j - i + 1)
    return best


def trace_max(nums, k, strict=False):
    """Part a event by event: the front index that left the window, every index popped from
    the back (a value <= the new one; with strict only a smaller one), and the push of the
    new index with the output of the window it closes. Every event keeps the deque after it
    (indices, front first) and the outputs so far."""
    ev, q, out = [], [], []
    for i, x in enumerate(nums):
        if q and q[0] == i - k:
            ev.append({"kind": "front", "i": i, "idx": q[0], "q": q[1:], "out": list(out)})
            q = q[1:]
        while q and (nums[q[-1]] < x if strict else nums[q[-1]] <= x):
            ev.append({"kind": "pop", "i": i, "idx": q[-1], "q": q[:-1], "out": list(out)})
            q = q[:-1]
        q = q + [i]
        if i >= k - 1:
            out.append(nums[q[0]])
        ev.append({"kind": "push", "i": i, "idx": i, "q": list(q), "out": list(out)})
    return ev


def rows_max(nums, k):
    """One row per index of part a: what left the front, what was popped from the back, the
    deque after the index and the output."""
    rows = []
    for e in trace_max(nums, k):
        if not rows or rows[-1]["i"] != e["i"]:
            rows.append({"i": e["i"], "front": None, "popped": [], "q": [], "out": None})
        r = rows[-1]
        if e["kind"] == "front":
            r["front"] = e["idx"]
        elif e["kind"] == "pop":
            r["popped"].append(e["idx"])
        else:
            r["q"] = e["q"]
            r["out"] = e["out"][-1] if e["i"] >= k - 1 else None
    return rows


def trace_limit(nums, limit):
    """Part b event by event: the pops from the back of hi (the deque of the maximum, values
    decreasing) and of lo (the minimum, values increasing), the push of the new index into
    both, and every step of the left end; the event that ends the right end's turn records
    the length and the best so far."""
    ev, hi, lo, left, best, win = [], [], [], 0, 0, None

    def rec(kind, right, idx=None, measured=False, gone=None):
        ev.append({"kind": kind, "right": right, "idx": idx, "hi": list(hi), "lo": list(lo), "left": left,
                   "best": best, "win": list(win) if win else None, "measured": measured, "gone": gone or []})

    for right, x in enumerate(nums):
        while hi and nums[hi[-1]] <= x:
            idx = hi.pop()
            rec("hipop", right, idx)
        while lo and nums[lo[-1]] >= x:
            idx = lo.pop()
            rec("lopop", right, idx)
        hi.append(right)
        lo.append(right)
        shrink = nums[hi[0]] - nums[lo[0]] > limit
        if not shrink:
            if right - left + 1 > best:
                best, win = right - left + 1, (left, right)
            rec("enter", right, right, measured=True)
            continue
        rec("enter", right, right)
        while nums[hi[0]] - nums[lo[0]] > limit:
            gone = []
            if hi[0] == left:
                gone.append("hi")
                hi.pop(0)
            if lo[0] == left:
                gone.append("lo")
                lo.pop(0)
            left += 1
            ok = nums[hi[0]] - nums[lo[0]] <= limit
            if ok and right - left + 1 > best:
                best, win = right - left + 1, (left, right)
            rec("left", right, left - 1, measured=ok, gone=gone)
    return ev


def hw_trace(stream, k):
    """The module of part c cycle by cycle: before the clock edge the K comparators give
    keep[j] = valid[j] and val[j] > x, a prefix of ones; x goes into slot p, the first zero;
    the entries kept age by one, and when the front reaches age K it leaves and every entry
    moves one slot towards the front. After the edge max_out is val[0]."""
    val, age, vld, rows = [0] * k, [0] * k, [False] * k, []
    for t, x in enumerate(stream):
        keep = [vld[j] and val[j] > x for j in range(k)]
        p = keep.index(False) if False in keep else k
        nval = [val[j] if j < p else x for j in range(p + 1)]
        nage = [age[j] + 1 if j < p else 0 for j in range(p + 1)]
        drop = nage[0] == k
        s = 1 if drop else 0
        nval, nage = nval[s:], nage[s:]
        before = [(val[j], age[j]) for j in range(k) if vld[j]]
        val = nval + [0] * (k - len(nval))
        age = nage + [0] * (k - len(nage))
        vld = [j < len(nval) for j in range(k)]
        rows.append({"t": t, "x": x, "before": before, "keep": keep, "p": p, "drop": drop,
                     "dropped": before[0] if drop else None,
                     "after": [(val[j], age[j]) for j in range(k) if vld[j]], "out": val[0]})
    return rows


def van_herk(nums, k):
    """The block method of the follow-up: prefix maxima from the start of every block of k,
    suffix maxima to its end, and max(suffix[i], prefix[i + k - 1]) for the window at i.
    Returns the maxima and the number of comparisons."""
    n, cmp = len(nums), 0
    pre, suf = list(nums), list(nums)
    for i in range(n):
        if i % k:
            cmp += 1
            pre[i] = max(pre[i - 1], nums[i])
    for i in range(n - 2, -1, -1):
        if (i + 1) % k:
            cmp += 1
            suf[i] = max(suf[i + 1], nums[i])
    out = []
    for i in range(n - k + 1):
        if i % k:
            cmp += 1
            out.append(max(suf[i], pre[i + k - 1]))
        else:
            out.append(pre[i + k - 1])            # the window is one whole block
    return out, cmp


# --- blocks ------------------------------------------------------------------------------

def num(v):
    """A number as the page writes it: the minus sign, not a hyphen."""
    return str(v).replace("-", "−")


def deque_svg(nums, k):
    """The deque after every index of part a, a row per index: the window outlined, the
    indices in the deque filled (the front one framed), the ones that left in that index's
    step struck out in orange, and the output at the end of the row."""
    rows = rows_max(nums, k)
    n, cell, rh, lw, ow, top = len(nums), 34, 36, 58, 56, 30
    W, H = lw + n * cell + ow, top + len(rows) * rh + 6
    s = (f'<svg class="figure sm-fig" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" '
         f'aria-label="המערך {" ".join(map(num, nums))} עם k = {k} : ה-deque אחרי כל אינדקס, והמקסימום של כל חלון">')
    for p in range(n):
        s += f'<text class="tick" x="{lw + p * cell + cell / 2:g}" y="14" text-anchor="middle">{p}</text>'
    s += f'<text class="tick" x="{lw - 8}" y="14" text-anchor="end">index</text>'
    s += f'<text class="tick" x="{lw + n * cell + ow / 2:g}" y="14" text-anchor="middle">max</text>'
    for r in rows:
        i, y = r["i"], top + r["i"] * rh
        gone = ([r["front"]] if r["front"] is not None else []) + r["popped"]
        s += f'<text class="sm-lab" x="{lw - 8}" y="{y + 19}" text-anchor="end">i = {i}</text>'
        lo = max(0, i - k + 1)
        s += f'<rect class="sm-win" x="{lw + lo * cell + 1}" y="{y - 1}" width="{(i - lo + 1) * cell - 2}" height="{rh - 6}" rx="5"/>'
        for p, v in enumerate(nums):
            x = lw + p * cell
            kind = "is-front" if r["q"] and p == r["q"][0] else "is-in" if p in r["q"] else "is-pop" if p in gone else "is-wait" if p > i else "is-off"
            what = {"is-front": "the front of the deque", "is-in": "in the deque", "is-pop": "left the deque at this index",
                    "is-wait": "not read yet", "is-off": "not in the deque"}[kind]
            s += (f'<g class="sm-cell {kind}"><title>i = {i}: place {p}, value {v}, {what}</title>'
                  f'<rect x="{x + 3}" y="{y + 2}" width="{cell - 6}" height="{rh - 12}" rx="4"/>'
                  f'<text x="{x + cell / 2:g}" y="{y + 19}" text-anchor="middle">{num(v)}</text></g>')
            if kind == "is-pop":
                s += f'<line class="sm-strike" x1="{x + 6}" y1="{y + rh - 13}" x2="{x + cell - 6}" y2="{y + 5}"/>'
        out = "–" if r["out"] is None else num(r["out"])
        s += f'<text class="sm-out{"" if r["out"] is None else " is-val"}" x="{lw + n * cell + ow / 2:g}" y="{y + 19}" text-anchor="middle">{out}</text>'
    return s + "</svg>"


def deque_legend():
    return ('<span class="viz-legend"><span><i class="sm-key-win"></i>החלון של k הערכים האחרונים</span>'
            '<span><i class="sm-key-in"></i>אינדקס ב-deque</span><span><i class="sm-key-front"></i>הראש של ה-deque, המקסימום</span>'
            '<span><i class="sm-key-pop"></i>יצא מה-deque באינדקס הזה</span></span>')


def sval(v):
    """A value for a table cell: a negative one in an LTR span, or the RLM before it puts the
    minus after the digits."""
    return f'<span dir="ltr">{num(v)}</span>' if v < 0 else num(v)


def dq(nums, idx):
    """A deque as the values with their indices under them, front first."""
    if not idx:
        return "ריק"
    return '<span dir="ltr">' + " ".join(f"{num(nums[j])}<sub>{j}</sub>" for j in idx) + "</span>"


def table_max(nums, k):
    out = ["| ‏i | הערך | יצא מהראש | יצאו מהזנב | ה-deque אחרי הצעד | המקסימום |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for r in rows_max(nums, k):
        front = f"{RLM}{sval(nums[r['front']])}<sub>{r['front']}</sub>" if r["front"] is not None else "אין"
        popped = (RLM + '<span dir="ltr">' + " ".join(f"{num(nums[j])}<sub>{j}</sub>" for j in r["popped"]) + "</span>") if r["popped"] else "אין"
        o = f"**{RLM}{sval(r['out'])}**" if r["out"] is not None else "עוד אין חלון"
        out.append(f"| {RLM}{r['i']} | {RLM}{sval(nums[r['i']])} | {front} | {popped} | {RLM}{dq(nums, r['q'])} | {o} |")
    return "\n".join(out)


def table_limit(nums, limit):
    """A row per right end of part b: the two deques after the push and after the left end
    moved, the window and its max - min, the best so far."""
    ev = trace_limit(nums, limit)
    out = ["| ‏right | הערך | ‏hi (המקסימום) | ‏lo (המינימום) | ‏left | החלון | ‏max − min | הטוב עד עכשיו |", "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for right in range(len(nums)):
        mine = [e for e in ev if e["right"] == right]
        enter = next(e for e in mine if e["kind"] == "enter")
        last = mine[-1]
        moved = sum(1 for e in mine if e["kind"] == "left")
        before = nums[enter["hi"][0]] - nums[enter["lo"][0]]
        after = nums[last["hi"][0]] - nums[last["lo"][0]]
        spread = f'{RLM}<span dir="ltr">{before} → {after}</span>' if moved else f"{RLM}{after}"
        lft = f"{RLM}{last['left']} (זז {RLM}{moved})" if moved else f"{RLM}{last['left']}"
        out.append(f"| {RLM}{right} | {RLM}{num(nums[right])} | {RLM}{dq(nums, last['hi'])} | {RLM}{dq(nums, last['lo'])} | {lft} | "
                   f"{RLM}{last['left']}..{right} | {spread} | **{RLM}{last['best']}** |")
    return "\n".join(out)


def diagram_svg():
    """The module of part c with K = 3: the entries, a comparator per entry fed by the bus
    of the new sample x, the priority encoder that finds the first entry not larger than
    x, the next-state logic and the feedback into the registers."""
    W, H, k = 400, 270, 3
    cx = [90 + j * 100 for j in range(k)]
    bw = 84
    s = (f'<svg class="figure sm-fig sm-diag" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" '
         'aria-label="המודול עם K = 3 : שלוש כניסות, משווה לכל כניסה מול הדגימה החדשה x, מקודד עדיפות שמוצא את המקום של x, ולוגיקת המצב הבא">')
    tri = lambda x, y, d: (f'<path class="sm-head" d="M{x - 4},{y - 7 * d} L{x + 4},{y - 7 * d} L{x},{y} Z"/>')   # an arrowhead pointing along d
    # max_out from entry 0
    s += f'<text class="sm-lab" x="{cx[0]}" y="14" text-anchor="middle">max_out = val[0]</text>'
    s += f'<line class="sm-wire" x1="{cx[0]}" y1="40" x2="{cx[0]}" y2="22"/>' + tri(cx[0], 20, -1)
    for j in range(k):
        x0 = cx[j] - bw / 2
        s += (f'<rect class="sm-reg" x="{x0}" y="40" width="{bw}" height="40" rx="4"><title>entry {j}: a value and its age</title></rect>'
              f'<text class="sm-lab" x="{cx[j]}" y="56" text-anchor="middle">val[{j}]</text>'
              f'<text class="sm-lab" x="{cx[j]}" y="72" text-anchor="middle">age[{j}]</text>')
        # val[j] down to the comparator, x tapped from the bus
        s += f'<line class="sm-wire" x1="{cx[j] - 16}" y1="80" x2="{cx[j] - 16}" y2="114"/>' + tri(cx[j] - 16, 118, 1)
        s += f'<line class="sm-wire" x1="{cx[j] + 16}" y1="100" x2="{cx[j] + 16}" y2="114"/>' + tri(cx[j] + 16, 118, 1)
        s += f'<circle class="sm-tap" cx="{cx[j] + 16}" cy="100" r="3"/>'
        s += (f'<rect class="sm-cmpbox" x="{x0 + 6}" y="118" width="{bw - 12}" height="26" rx="13"><title>comparator {j}</title></rect>'
              f'<text class="sm-lab" x="{cx[j]}" y="135" text-anchor="middle">val[{j}] &gt; x</text>')
        s += f'<line class="sm-wire" x1="{cx[j]}" y1="144" x2="{cx[j]}" y2="172"/>' + tri(cx[j], 176, 1)
        s += f'<text class="tick" x="{cx[j] + 5}" y="162">keep[{j}]</text>'
    s += f'<line class="sm-bus" x1="{cx[0] - 30}" y1="100" x2="{W - 14}" y2="100"/>'
    s += f'<text class="sm-lab" x="{W - 12}" y="94" text-anchor="end">x</text>'
    ex0, ew = 30, W - 40                      # the wide boxes of the encoder and the next state
    s += (f'<rect class="sm-enc" x="{ex0}" y="176" width="{ew}" height="28" rx="4"/>'
          f'<text class="sm-lab" x="{ex0 + ew / 2:g}" y="194" text-anchor="middle">priority encoder: p = the first 0 of keep</text>')
    s += f'<line class="sm-wire" x1="{(cx[0] + cx[-1]) / 2}" y1="204" x2="{(cx[0] + cx[-1]) / 2}" y2="218"/>' + tri((cx[0] + cx[-1]) / 2, 222, 1)
    s += (f'<rect class="sm-enc" x="{ex0}" y="222" width="{ew}" height="40" rx="4"/>'
          f'<text class="sm-lab" x="{ex0 + ew / 2:g}" y="238" text-anchor="middle">next: j &lt; p kept (age + 1), slot p ← x</text>'
          f'<text class="sm-lab" x="{ex0 + ew / 2:g}" y="254" text-anchor="middle">age[0] = K: shift to the front</text>')
    # the feedback into the registers at the clock edge
    s += (f'<path class="sm-wire" d="M{ex0},{242} H14 V60 H{cx[0] - bw / 2 - 8}"/>' +
          f'<path class="sm-head" d="M{cx[0] - bw / 2 - 7},56 L{cx[0] - bw / 2 - 7},64 L{cx[0] - bw / 2},60 Z"/>' +
          f'<text class="tick" x="18" y="152" text-anchor="start">clk</text>')
    return s + "</svg>"


def entries(es):
    if not es:
        return "ריק"
    return '<span dir="ltr">' + " ".join(f"{v}<sub>{a}</sub>" for v, a in es) + "</span>"


def table_hw(stream, k):
    out = ["| המחזור | ‏x | הכניסות לפני | ‏keep | המקום של x | יוצא בגיל K | הכניסות אחרי | ‏max_out |", "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for r in hw_trace(stream, k):
        keep = RLM + '<span dir="ltr">' + "".join("1" if b else "0" for b in r["keep"]) + "</span>"
        drop = f"{RLM}{r['dropped'][0]}" if r["drop"] else "אין"
        out.append(f"| {RLM}{r['t']} | {RLM}{r['x']} | {RLM}{entries(r['before'])} | {keep} | {RLM}{r['p']} | {drop} | "
                   f"{RLM}{entries(r['after'])} | **{RLM}{r['out']}** |")
    return "\n".join(out)


def blocks():
    """The generated blocks, in page order."""
    return [deque_svg(NUMS, K), deque_legend(), table_max(NUMS, K), table_limit(NUMS_B, LIMIT), diagram_svg(), table_hw(STREAM, K_HW)]


if __name__ == "__main__":
    print(brute_max(NUMS, K), [r["out"] for r in rows_max(NUMS, K)], brute_limit(NUMS_B, LIMIT), [r["out"] for r in hw_trace(STREAM, K_HW)])
    print("\n\n".join(blocks()))
