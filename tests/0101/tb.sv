//@page function automatic bit same_sum
//@page function automatic void factor_pairs
// Question 0101: the page's SystemVerilog against references written here: the histogram of
// the sum counted roll by roll, the pairs of the page (part a, part b with a face 0, the pairs
// of n = 4 and 8) and the number of pairs for every n up to 12, 16 and 20; the factors
// cyclotomic() returns are checked coefficient by coefficient, and dice_pairs and factor_pairs
// must find the same pairs for n = 2 to 8.
module tb;
  int errors = 0;

  task automatic fail(string what);
    errors++;
    if (errors < 20) $display("%s", what);
  endtask

  // the reference: the histogram of a + b roll by roll, against two standard dice
  function automatic bit ref_same(int a[$], int b[$]);
    int got[64], want[64];
    if (a.size() != b.size()) return 0;
    foreach (got[s]) begin got[s] = 0; want[s] = 0; end
    foreach (a[i]) foreach (b[j]) got[a[i] + b[j]]++;
    for (int i = 1; i <= a.size(); i++) for (int j = 1; j <= a.size(); j++) want[i + j]++;
    foreach (got[s]) if (got[s] != want[s]) return 0;
    return 1;
  endfunction

  function automatic bit has(string q[$], string s);
    foreach (q[i]) if (q[i] == s) return 1;
    return 0;
  endfunction

  task automatic same_set(string what, string got[$], string want[$]);
    if (got.size() != want.size()) fail($sformatf("%s: %0d pairs, want %0d", what, got.size(), want.size()));
    foreach (want[i]) if (!has(got, want[i])) fail($sformatf("%s: missing %s", what, want[i]));
  endtask

  initial begin
    string got[$], other[$], want[$];
    int a[$], b[$], n, counts[int];
    poly_t c;
    int phi12[$] = '{1, 0, -1, 0, 1};
    int phi10[$] = '{1, -1, 1, -1, 1};
    int phi9[$] = '{1, 0, 0, 1, 0, 0, 1};

    // same_sum on the page's pairs and tries
    if (!same_sum('{1, 2, 3, 4, 5, 6}, '{1, 2, 3, 4, 5, 6})) fail("standard dice");
    if (!same_sum('{1, 2, 2, 3, 3, 4}, '{1, 3, 4, 5, 6, 8})) fail("Sicherman dice");
    if (!same_sum('{0, 1, 1, 2, 2, 3}, '{2, 4, 5, 6, 7, 9})) fail("a shift of Sicherman");
    if (same_sum('{1, 1, 2, 3, 4, 5}, '{1, 2, 3, 4, 5, 6})) fail("face 1 twice passed");
    if (same_sum('{1, 2, 2, 3, 3, 4}, '{1, 3, 4, 5, 6, 7})) fail("B's 8 to 7 passed");
    if (same_sum('{1, 2, 3}, '{1, 2, 3, 4})) fail("dice of different sizes passed");
    // and on random dice against the histogram counted here
    for (int t = 0; t < 3000; t++) begin
      n = 1 + $urandom_range(0, 7);
      a.delete(); b.delete();
      repeat (n) begin a.push_back($urandom_range(0, 12)); b.push_back($urandom_range(0, 12)); end
      if (t % 3 == 0) begin                 // now and then a standard die or Sicherman, shuffled
        a.delete(); b.delete();
        for (int f = 1; f <= n; f++) begin a.push_back(f); b.push_back(f); end
        a.shuffle(); b.shuffle();
      end
      if (same_sum(a, b) != ref_same(a, b)) fail($sformatf("same_sum differs on %p %p", a, b));
    end

    // part a and part b
    dice_pairs(6, 1, got);
    want = '{"1 2 2 3 3 4 + 1 3 4 5 6 8", "1 2 3 4 5 6 + 1 2 3 4 5 6"};
    same_set("dice_pairs(6, 1)", got, want);
    dice_pairs(6, 0, got);
    want = '{"1 2 2 3 3 4 + 1 3 4 5 6 8", "1 2 3 4 5 6 + 1 2 3 4 5 6", "0 1 2 3 4 5 + 2 3 4 5 6 7",
             "0 1 1 2 2 3 + 2 4 5 6 7 9", "0 2 3 4 5 7 + 2 3 3 4 4 5"};
    same_set("dice_pairs(6, 0)", got, want);

    // part c: the factors, the counts, the pairs of 4 and 8
    c = cyclotomic(12);
    if (c != phi12) fail($sformatf("Phi_12 = %p", c));
    c = cyclotomic(10);
    if (c != phi10) fail($sformatf("Phi_10 = %p", c));
    c = cyclotomic(9);
    if (c != phi9) fail($sformatf("Phi_9 = %p", c));
    for (int d = 2; d <= 30; d++) begin        // Phi_d(1): p for a power of the prime p, else 1
      int p, m, s;                         // set here: a declaration's value is given once only
      p = 0;
      m = d;
      for (int q = 2; q <= d; q++) if (m % q == 0) begin
        if (p == 0) p = q; else if (q != p) p = -1;
        while (m % q == 0) m /= q;
      end
      c = cyclotomic(d);
      s = c.sum();
      if (s != (p > 0 ? p : 1)) fail($sformatf("Phi_%0d(1) = %0d", d, s));
    end
    counts = '{2: 1, 3: 1, 4: 2, 5: 1, 6: 2, 7: 1, 8: 4, 9: 2, 10: 2, 11: 1, 12: 8, 16: 10, 20: 8};
    foreach (counts[k]) begin
      factor_pairs(k, got);
      if (got.size() != counts[k]) fail($sformatf("factor_pairs(%0d): %0d pairs, want %0d", k, got.size(), counts[k]));
    end
    factor_pairs(4, got);
    want = '{"1 2 2 3 + 1 3 3 5", "1 2 3 4 + 1 2 3 4"};
    same_set("factor_pairs(4)", got, want);
    factor_pairs(8, got);
    want = '{"1 2 2 3 3 4 4 5 + 1 3 5 5 7 7 9 11", "1 2 2 3 5 6 6 7 + 1 3 3 5 5 7 7 9",
             "1 2 3 3 4 4 5 6 + 1 2 5 5 6 6 9 10", "1 2 3 4 5 6 7 8 + 1 2 3 4 5 6 7 8"};
    same_set("factor_pairs(8)", got, want);
    // the search and the factors agree
    for (int k = 2; k <= 8; k++) begin
      dice_pairs(k, 1, got);
      factor_pairs(k, other);
      same_set($sformatf("dice_pairs(%0d) against factor_pairs", k), got, other);
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
