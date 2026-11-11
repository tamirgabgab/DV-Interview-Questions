//@page typedef int poly_t
//@page function automatic void dice_sets
// Question 0101: the page's SystemVerilog against references written here: the histogram of
// the sum counted roll by roll (two dice and three), the pairs of the page (part a, part b with
// a face 0), the sets of three dice of part c with positive faces and with a face 0, and the
// number of sets for k = 1 to 6 dice; every set dice_sets returns is checked with same_sum_k,
// and for two dice dice_sets and dice_pairs must find the same pairs.
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

  // the reference for three dice: the histogram of a + b + c roll by roll
  function automatic bit ref_same3(int a[$], int b[$], int c[$]);
    int got[128], want[128];
    foreach (got[s]) begin got[s] = 0; want[s] = 0; end
    foreach (a[i]) foreach (b[j]) foreach (c[l]) got[a[i] + b[j] + c[l]]++;
    for (int i = 1; i <= 6; i++) for (int j = 1; j <= 6; j++) for (int l = 1; l <= 6; l++) want[i + j + l]++;
    foreach (got[s]) if (got[s] != want[s]) return 0;
    return 1;
  endfunction

  // "1 2 2 3 3 4 + 1 2 3 4 5 6" -> the faces one after another
  function automatic void parse_set(string line, ref int faces[$]);
    int v = -1;
    faces.delete();
    for (int i = 0; i <= line.len(); i++) begin
      if (i < line.len() && line[i] >= "0" && line[i] <= "9") v = (v < 0 ? 0 : 10 * v) + (line[i] - "0");
      else if (v >= 0) begin faces.push_back(v); v = -1; end
    end
  endfunction

  task automatic same_set(string what, string got[$], string want[$]);
    if (got.size() != want.size()) fail($sformatf("%s: %0d found, want %0d", what, got.size(), want.size()));
    foreach (want[i]) if (!has(got, want[i])) fail($sformatf("%s: missing %s", what, want[i]));
  endtask

  initial begin
    string got[$], other[$], want[$];
    int a[$], b[$], n, counts[int];

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

    // part c: k six-sided dice
    if (!same_sum_k('{1, 2, 2, 3, 3, 4, 1, 2, 3, 4, 5, 6, 1, 3, 4, 5, 6, 8})) fail("Sicherman and a standard die");
    if (!same_sum_k('{0, 1, 1, 2, 2, 3, 0, 1, 2, 3, 4, 5, 3, 5, 6, 7, 8, 10})) fail("a shifted set of three");
    if (same_sum_k('{1, 2, 2, 3, 3, 4, 1, 3, 4, 5, 6, 8, 1, 3, 4, 5, 6, 8})) fail("two big Sicherman dice passed");
    if (same_sum_k('{1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5})) fail("a die of five faces passed");
    for (int t = 0; t < 2000; t++) begin    // three dice: random, and now and then shuffled standard
      int f[$];
      a.delete(); b.delete(); f.delete();
      repeat (6) begin a.push_back($urandom_range(0, 9)); b.push_back($urandom_range(0, 9)); f.push_back($urandom_range(0, 9)); end
      if (t % 4 == 0) begin
        a = '{1, 2, 3, 4, 5, 6}; b = '{1, 2, 2, 3, 3, 4}; f = '{1, 3, 4, 5, 6, 8};
        if (t % 8 == 0) a[$urandom_range(0, 5)] = $urandom_range(0, 9);
        a.shuffle(); b.shuffle(); f.shuffle();
      end
      if (same_sum_k({a, b, f}) != ref_same3(a, b, f)) fail($sformatf("same_sum_k differs on %p %p %p", a, b, f));
    end
    dice_sets(3, 1, got);
    want = '{"1 2 2 3 3 4 + 1 2 3 4 5 6 + 1 3 4 5 6 8", "1 2 3 4 5 6 + 1 2 3 4 5 6 + 1 2 3 4 5 6"};
    same_set("dice_sets(3, 1)", got, want);
    dice_sets(3, 0, got);
    want = '{"0 1 1 2 2 3 + 0 1 2 3 4 5 + 3 5 6 7 8 10", "0 1 1 2 2 3 + 0 2 3 4 5 7 + 3 4 5 6 7 8",
             "0 1 1 2 2 3 + 1 2 3 4 5 6 + 2 4 5 6 7 9", "0 1 1 2 2 3 + 1 3 4 5 6 8 + 2 3 4 5 6 7",
             "0 1 2 3 4 5 + 0 1 2 3 4 5 + 3 4 5 6 7 8", "0 1 2 3 4 5 + 0 2 3 4 5 7 + 3 4 4 5 5 6",
             "0 1 2 3 4 5 + 1 2 2 3 3 4 + 2 4 5 6 7 9", "0 1 2 3 4 5 + 1 2 3 4 5 6 + 2 3 4 5 6 7",
             "0 1 2 3 4 5 + 1 3 4 5 6 8 + 2 3 3 4 4 5", "0 2 3 4 5 7 + 1 2 2 3 3 4 + 2 3 4 5 6 7",
             "0 2 3 4 5 7 + 1 2 3 4 5 6 + 2 3 3 4 4 5", "1 2 2 3 3 4 + 1 2 3 4 5 6 + 1 3 4 5 6 8",
             "1 2 3 4 5 6 + 1 2 3 4 5 6 + 1 2 3 4 5 6"};
    same_set("dice_sets(3, 0)", got, want);
    counts = '{1: 1, 2: 2, 3: 2, 4: 3, 5: 3, 6: 4};
    foreach (counts[k]) begin
      dice_sets(k, 1, got);
      if (got.size() != counts[k]) fail($sformatf("dice_sets(%0d, 1): %0d sets, want %0d", k, got.size(), counts[k]));
    end
    counts = '{1: 1, 2: 5, 3: 13, 4: 41, 5: 98, 6: 250};
    foreach (counts[k]) begin
      dice_sets(k, 0, got);
      if (got.size() != counts[k]) fail($sformatf("dice_sets(%0d, 0): %0d sets, want %0d", k, got.size(), counts[k]));
      if (k <= 5) foreach (got[i]) begin    // every set found has the sum of k standard dice
        parse_set(got[i], a);
        if (a.size() != 6 * k || !same_sum_k(a)) fail($sformatf("dice_sets(%0d, 0) gave %s", k, got[i]));
      end
    end
    // two dice: dice_sets and the search of part a find the same pairs
    for (int low = 0; low <= 1; low++) begin
      dice_sets(2, low, got);
      dice_pairs(6, low, other);
      same_set($sformatf("dice_sets(2, %0d) against dice_pairs", low), got, other);
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
