// Question 0066: the page's merge, skyline, above and peak against references written
// into the testbench (the overlap graph for the merge, the total height read at every
// integer point for the pieces and the ranges), on the page's examples, the self-checks,
// the edge cases and random inputs; and the corollary that part a is part b with height 1.
module tb;
  //@page function automatic void merge
  //@page function automatic void skyline
  //@page function automatic void above

  int errors = 0;

  function automatic bit same_spans(span_t a[$], span_t b[$]);
    if (a.size() != b.size()) return 0;
    foreach (a[i]) if (a[i].s != b[i].s || a[i].e != b[i].e) return 0;
    return 1;
  endfunction

  function automatic bit same_pieces(piece_t a[$], piece_t b[$]);
    if (a.size() != b.size()) return 0;
    foreach (a[i]) if (a[i].s != b[i].s || a[i].e != b[i].e || a[i].h != b[i].h) return 0;
    return 1;
  endfunction

  function automatic string show_spans(span_t a[$]);
    string s = "";
    foreach (a[i]) s = {s, $sformatf("[%0d,%0d] ", a[i].s, a[i].e)};
    return s;
  endfunction

  // the merged intervals by the overlap graph: components of "share a point"
  function automatic void brute_merge(span_t iv[], output span_t out[$]);
    int comp[], root, other;
    int lo[int], hi[int];
    int keys[$];
    out = {};
    comp = new[iv.size()];
    foreach (comp[i]) comp[i] = i;
    foreach (iv[i]) foreach (iv[j]) begin
      if (i < j && iv[i].s <= iv[j].e && iv[j].s <= iv[i].e) begin
        root = i; while (comp[root] != root) root = comp[root];
        other = j; while (comp[other] != other) other = comp[other];
        comp[root] = other;
      end
    end
    foreach (iv[i]) begin
      root = i; while (comp[root] != root) root = comp[root];
      if (!lo.exists(root)) begin lo[root] = iv[i].s; hi[root] = iv[i].e; end
      else begin
        if (iv[i].s < lo[root]) lo[root] = iv[i].s;
        if (iv[i].e > hi[root]) hi[root] = iv[i].e;
      end
    end
    foreach (lo[k]) keys.push_back(k);
    keys.sort with (lo[item]);
    foreach (keys[k]) out.push_back('{lo[keys[k]], hi[keys[k]]});
  endfunction

  // the total height at the integer point x
  function automatic int height_at(piece_t iv[], int x);
    int t = 0;
    foreach (iv[i]) if (iv[i].s <= x && x < iv[i].e) t += iv[i].h;
    return t;
  endfunction

  // the pieces read point by point: maximal runs of one non-zero total
  function automatic void brute_skyline(piece_t iv[], output piece_t out[$]);
    int lo, hi, t;
    out = {};
    if (iv.size() == 0) return;
    lo = iv[0].s; hi = iv[0].e;
    foreach (iv[i]) begin
      if (iv[i].s < lo) lo = iv[i].s;
      if (iv[i].e > hi) hi = iv[i].e;
    end
    for (int x = lo; x < hi; x++) begin
      t = height_at(iv, x);
      if (t == 0) continue;
      if (out.size() > 0 && out[$].e == x && out[$].h == t) out[$].e = x + 1;
      else out.push_back('{x, x + 1, t});
    end
  endfunction

  // the ranges with a total of at least t, read point by point
  function automatic void brute_above(piece_t iv[], int t, output span_t out[$]);
    int lo, hi;
    out = {};
    if (iv.size() == 0) return;
    lo = iv[0].s; hi = iv[0].e;
    foreach (iv[i]) begin
      if (iv[i].s < lo) lo = iv[i].s;
      if (iv[i].e > hi) hi = iv[i].e;
    end
    for (int x = lo; x < hi; x++) begin
      if (height_at(iv, x) < t) continue;
      if (out.size() > 0 && out[$].e == x) out[$].e = x + 1;
      else out.push_back('{x, x + 1});
    end
  endfunction

  initial begin
    span_t a[], m[$], want[$], rs[$], wr[$], where[$], one[$];
    piece_t b[], sk[], pieces[$], wantp[$];
    int n, t, top, hmax;
    // part a: the page's example, touching intervals, an unsorted list, a nested one, the self-check
    a = '{'{1, 3}, '{2, 6}, '{8, 10}, '{15, 18}};
    merge(a, m); want = '{'{1, 6}, '{8, 10}, '{15, 18}};
    if (!same_spans(m, want)) begin errors++; $display("page example a: %s", show_spans(m)); end
    a = '{'{1, 4}, '{4, 5}};
    merge(a, m); want = '{'{1, 5}};
    if (!same_spans(m, want)) begin errors++; $display("touching: %s", show_spans(m)); end
    a = '{'{8, 10}, '{1, 3}, '{2, 6}};
    merge(a, m); want = '{'{1, 6}, '{8, 10}};
    if (!same_spans(m, want)) begin errors++; $display("unsorted: %s", show_spans(m)); end
    a = '{'{1, 10}, '{2, 3}, '{4, 5}};
    merge(a, m); want = '{'{1, 10}};
    if (!same_spans(m, want)) begin errors++; $display("nested: %s", show_spans(m)); end
    a = '{'{2, 5}, '{1, 3}, '{6, 9}, '{9, 10}, '{12, 14}};
    merge(a, m);
    if (m.size() != 3) begin errors++; $display("self-check a: %s", show_spans(m)); end
    a = new[0];
    merge(a, m);
    if (m.size() != 0) begin errors++; $display("empty a"); end
    // part b: the page's example, touching with one total, the zero-length trap, a gap, one start
    b = '{'{1, 7, 7}, '{2, 6, 4}};
    skyline(b, pieces); wantp = '{'{1, 2, 7}, '{2, 6, 11}, '{6, 7, 7}};
    if (!same_pieces(pieces, wantp)) begin errors++; $display("page example b"); end
    b = '{'{0, 2, 3}, '{2, 4, 3}};
    skyline(b, pieces); wantp = '{'{0, 4, 3}};
    if (!same_pieces(pieces, wantp)) begin errors++; $display("one piece"); end
    b = '{'{0, 4, 2}, '{4, 8, 2}};
    skyline(b, pieces); wantp = '{'{0, 8, 2}};
    if (!same_pieces(pieces, wantp)) begin errors++; $display("zero-length trap"); end
    b = '{'{0, 2, 1}, '{5, 7, 1}};
    skyline(b, pieces); wantp = '{'{0, 2, 1}, '{5, 7, 1}};
    if (!same_pieces(pieces, wantp)) begin errors++; $display("gap"); end
    b = '{'{0, 4, 1}, '{0, 4, 2}};
    skyline(b, pieces); wantp = '{'{0, 4, 3}};
    if (!same_pieces(pieces, wantp)) begin errors++; $display("same start"); end
    b = '{'{0, 4, 2}, '{2, 6, 3}, '{4, 8, 2}};
    skyline(b, pieces);
    if (pieces.size() != 3) begin errors++; $display("self-check b: %0d pieces", pieces.size()); end
    b = new[0];
    skyline(b, pieces);
    if (pieces.size() != 0) begin errors++; $display("empty b"); end
    // part c: the page's example with T = 4, the peak, the self-check
    b = '{'{0, 4, 2}, '{1, 3, 3}, '{2, 6, 1}, '{5, 8, 4}};
    skyline(b, pieces);
    above(pieces, 4, rs); want = '{'{1, 3}, '{5, 8}};
    if (!same_spans(rs, want)) begin errors++; $display("above 4: %s", show_spans(rs)); end
    top = peak(pieces, where); want = '{'{2, 3}};
    if (top != 6 || !same_spans(where, want)) begin errors++; $display("peak: %0d at %s", top, show_spans(where)); end
    above(pieces, 7, rs);
    if (rs.size() != 0) begin errors++; $display("above 7"); end
    pieces = {};
    top = peak(pieces, where);
    if (top != 0 || where.size() != 0) begin errors++; $display("empty peak"); end

    for (int r = 0; r < 3000; r++) begin
      n = $urandom_range(0, 8);
      a = new[n]; b = new[n]; sk = new[n];
      hmax = $urandom_range(1, 4);
      foreach (a[i]) begin
        a[i].s = $urandom_range(0, 20); a[i].e = a[i].s + $urandom_range(0, 6);
        b[i].s = $urandom_range(0, 20); b[i].e = b[i].s + $urandom_range(1, 6); b[i].h = $urandom_range(1, hmax);
        sk[i] = '{a[i].s, a[i].e + 1, 1};                // never used: kept the same shape as b
      end
      merge(a, m); brute_merge(a, want);
      if (!same_spans(m, want)) begin errors++; $display("run %0d: merge %s vs %s", r, show_spans(m), show_spans(want)); end
      skyline(b, pieces); brute_skyline(b, wantp);
      if (!same_pieces(pieces, wantp)) begin errors++; $display("run %0d: skyline", r); end
      t = $urandom_range(1, 8);
      above(pieces, t, rs); brute_above(b, t, wr);
      if (!same_spans(rs, wr)) begin errors++; $display("run %0d: above %0d", r, t); end
      top = peak(pieces, where);
      brute_above(b, top, wr);
      foreach (pieces[j]) if (pieces[j].h > top) begin errors++; $display("run %0d: peak too small", r); end
      if (top > 0 && !same_spans(where, wr)) begin errors++; $display("run %0d: where", r); end
      // the corollary: part a's intervals (with s < e) as half-open ones of height 1, the
      // ranges with total >= 1 are the merged intervals
      one = {};
      foreach (a[i]) if (a[i].s < a[i].e) one.push_back(a[i]);
      sk = new[one.size()];
      foreach (one[i]) sk[i] = '{one[i].s, one[i].e, 1};
      skyline(sk, pieces); above(pieces, 1, rs);
      a = new[one.size()];
      foreach (one[i]) a[i] = one[i];
      merge(a, m);
      if (!same_spans(rs, m)) begin errors++; $display("run %0d: corollary %s vs %s", r, show_spans(rs), show_spans(m)); end
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
