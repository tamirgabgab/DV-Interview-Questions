// Question 0062: the page's tags_needed against a count of the open transactions at every
// send time, and pools against tags_needed on each kind alone and on all together, on the
// page's examples and on random lists of up to 9 transactions.
module tb;
  //@page function automatic int tags_needed
  //@page function automatic void pools

  int errors = 0;

  // the most open at once: at every send time, the transactions sent at or before it and
  // not yet answered
  function automatic int brute(int s[], int e[]);
    int best = 0, open_now;
    foreach (s[i]) begin
      open_now = 0;
      foreach (s[j]) if (s[j] <= s[i] && s[i] < e[j]) open_now++;
      if (open_now > best) best = open_now;
    end
    return best;
  endfunction

  // the transactions of one kind
  function automatic void pick(int s[], int e[], bit is_read[], bit want, output int ps[], output int pe[]);
    int n = 0, k = 0;
    foreach (s[i]) if (is_read[i] == want) n++;
    ps = new[n]; pe = new[n];
    foreach (s[i]) if (is_read[i] == want) begin ps[k] = s[i]; pe[k] = e[i]; k++; end
  endfunction

  initial begin
    int s[], e[], ps[], pe[], n, r, w, a;
    bit is_read[];
    s = '{0, 5, 15}; e = '{30, 10, 20};
    if (tags_needed(s, e) != 2) begin errors++; $display("page example: %0d", tags_needed(s, e)); end
    s = '{0, 10}; e = '{10, 20};
    if (tags_needed(s, e) != 1) begin errors++; $display("a response and a send at 10: %0d", tags_needed(s, e)); end
    s = '{0, 10, 5}; e = '{10, 20, 15};
    if (tags_needed(s, e) != 2) begin errors++; $display("self-check a: %0d", tags_needed(s, e)); end
    s = new[0]; e = new[0];
    if (tags_needed(s, e) != 0) begin errors++; $display("empty"); end
    s = '{0, 2, 20, 22}; e = '{10, 12, 30, 32}; is_read = '{1, 1, 0, 0};
    pools(s, e, is_read, r, w, a);
    if (r != 2 || w != 2 || a != 2) begin errors++; $display("peaks apart: %0d %0d %0d", r, w, a); end
    s = '{0, 2, 3, 5}; e = '{10, 12, 13, 15};
    pools(s, e, is_read, r, w, a);
    if (r != 2 || w != 2 || a != 4) begin errors++; $display("peaks together: %0d %0d %0d", r, w, a); end
    for (int t = 0; t < 300; t++) begin
      n = $urandom_range(0, 9);
      s = new[n]; e = new[n]; is_read = new[n];
      foreach (s[i]) begin
        s[i] = $urandom_range(0, 20);
        e[i] = s[i] + $urandom_range(1, 10);
        is_read[i] = $urandom_range(0, 1);
      end
      if (tags_needed(s, e) != brute(s, e)) begin errors++; $display("run %0d: %0d vs %0d", t, tags_needed(s, e), brute(s, e)); end
      pools(s, e, is_read, r, w, a);
      if (a != tags_needed(s, e)) begin errors++; $display("run %0d shared: %0d vs %0d", t, a, tags_needed(s, e)); end
      pick(s, e, is_read, 1, ps, pe);
      if (r != tags_needed(ps, pe)) begin errors++; $display("run %0d reads: %0d vs %0d", t, r, tags_needed(ps, pe)); end
      pick(s, e, is_read, 0, ps, pe);
      if (w != tags_needed(ps, pe)) begin errors++; $display("run %0d writes: %0d vs %0d", t, w, tags_needed(ps, pe)); end
      if (a > r + w || a < r || a < w) begin errors++; $display("run %0d bounds: %0d %0d %0d", t, r, w, a); end
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
