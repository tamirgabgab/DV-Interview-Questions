// Question 0084: the page's SystemVerilog: lis_dp, lis_from_dp, lis and count_lis on the
// page's examples (the dp row, the two LIS, the counts 4 and 2, the trap [3, 4, 5, 1]) and on
// random arrays of up to 10 values against a brute force over every subsequence (the
// length, the count, and both sequences increasing, of that length, and inside the array).
module tb;
  //@page function automatic int lis_dp
  //@page function automatic void lis(
  //@page function automatic longint count_lis

  int errors = 0;

  task automatic same(string what, longint got, longint want);
    if (got != want) begin errors++; $display("%s: got %0d, expected %0d", what, got, want); end
  endtask

  // the length and the number of index sets of the longest increasing subsequences
  function automatic void brute(int a[$], output int best, output longint count);
    int last, len;
    bit ok;
    best = 0; count = 0;
    for (int mask = 0; mask < (1 << a.size()); mask++) begin
      ok = 1; len = 0; last = 0;
      for (int i = 0; i < a.size(); i++)
        if (mask[i]) begin
          if (len > 0 && a[i] <= last) ok = 0;
          last = a[i]; len++;
        end
      if (ok && len > best) begin best = len; count = 1; end
      else if (ok && len == best) count++;
    end
  endfunction

  // s is increasing, of length n, and a subsequence of a
  function automatic bit good(int s[$], int a[$], int n);
    int k = 0;
    if (s.size() != n) return 0;
    for (int i = 1; i < s.size(); i++) if (s[i] <= s[i - 1]) return 0;
    foreach (a[i]) if (k < s.size() && a[i] == s[k]) k++;
    return k == s.size();
  endfunction

  initial begin
    int a[$], dp[$], prev[$], s1[$], s2[$];
    int n, best;
    longint count;
    int want_dp[8] = '{1, 1, 1, 2, 2, 3, 4, 4};
    int want_prev[8] = '{-1, -1, -1, 2, 2, 3, 5, 5};
    int want_s1[4] = '{2, 5, 7, 101};
    int want_s2[4] = '{2, 3, 7, 18};
    int want_t[3] = '{3, 4, 5};
    a = '{10, 9, 2, 5, 3, 7, 101, 18};
    same("lis_dp(example)", lis_dp(a, dp, prev), 4);
    foreach (dp[i]) same($sformatf("dp[%0d]", i), dp[i], want_dp[i]);
    foreach (prev[i]) same($sformatf("prev[%0d]", i), prev[i], want_prev[i]);
    lis_from_dp(a, dp, prev, s1);
    same("lis_from_dp size", s1.size(), 4);
    foreach (s1[i]) same($sformatf("lis_from_dp[%0d]", i), s1[i], want_s1[i]);
    lis(a, s2);
    same("lis size", s2.size(), 4);
    foreach (s2[i]) same($sformatf("lis[%0d]", i), s2[i], want_s2[i]);
    same("count_lis(example)", count_lis(a), 4);
    a = '{1, 3, 5, 4, 7};
    same("count_lis(1 3 5 4 7)", count_lis(a), 2);
    a = '{3, 4, 5, 1};
    lis(a, s2);
    same("lis(3 4 5 1) size", s2.size(), 3);
    foreach (s2[i]) same($sformatf("lis(3 4 5 1)[%0d]", i), s2[i], want_t[i]);
    a = '{2, 2, 2, 2, 2};
    same("count_lis(2 2 2 2 2)", count_lis(a), 5);

    for (int t = 0; t < 300; t++) begin
      a.delete();
      n = 1 + $urandom_range(9);
      for (int i = 0; i < n; i++) a.push_back(int'($urandom_range(12)) - 3);
      brute(a, best, count);
      same($sformatf("lis_dp, test %0d", t), lis_dp(a, dp, prev), best);
      same($sformatf("count_lis, test %0d", t), count_lis(a), count);
      lis_from_dp(a, dp, prev, s1);
      lis(a, s2);
      if (!good(s1, a, best)) begin errors++; $display("lis_from_dp is not an LIS, test %0d", t); end
      if (!good(s2, a, best)) begin errors++; $display("lis is not an LIS, test %0d", t); end
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
