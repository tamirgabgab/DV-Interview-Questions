// Question 0090: the page's SystemVerilog. simple_sort on the page's stack (7 flips,
// 3 5 2 4 2 3 2) and on every stack up to 6 (sorted, at most 2n - 3 flips, exactly 2n - 3 on
// the worst one); pancake_number for n = 1..8 (0, 1, 3, 4, 5, 7, 8, 9); burnt_simple on every
// burnt stack up to 5 (sorted with every burnt side down, at most 3n - 2 flips and exactly
// that on the worst) and on [-1, -2, -3] (3 1 3 2 1 2 1); burnt_flip on [1, -2, 3].
module tb;
  //@page function automatic int simple_sort
  //@page function automatic int pancake_number
  //@page function automatic int burnt_simple

  int errors = 0;

  // the next permutation in lexicographic order; 0 after the last one
  function automatic bit next_perm(ref int a[$]);
    int i = a.size() - 2, j, t;
    while (i >= 0 && a[i] >= a[i + 1]) i--;
    if (i < 0) return 0;
    j = a.size() - 1;
    while (a[j] <= a[i]) j--;
    t = a[i]; a[i] = a[j]; a[j] = t;
    for (int l = i + 1, r = a.size() - 1; l < r; l++, r--) begin t = a[l]; a[l] = a[r]; a[r] = t; end
    return 1;
  endfunction

  function automatic bit is_sorted(int s[$]);
    foreach (s[i]) if (s[i] != i + 1) return 0;
    return 1;
  endfunction

  initial begin
    int s[$], p[$];
    string flips;
    int n_flips, worst, got;
    int want_p[8] = '{0, 1, 3, 4, 5, 7, 8, 9};

    s = '{3, 1, 5, 4, 2};
    n_flips = simple_sort(s, flips);
    $display("simple_sort [3, 1, 5, 4, 2]: %0d flips: %s", n_flips, flips);
    if (n_flips != 7 || flips != "3 5 2 4 2 3 2 " || !is_sorted(s)) begin errors++; $display("expected 7 flips 3 5 2 4 2 3 2"); end

    for (int n = 2; n <= 6; n++) begin
      p.delete();
      for (int i = 1; i <= n; i++) p.push_back(i);
      worst = 0;
      do begin
        s = p;
        n_flips = simple_sort(s, flips);
        if (!is_sorted(s)) begin errors++; $display("n = %0d: a stack is not sorted", n); end
        if (n_flips > worst) worst = n_flips;
      end while (next_perm(p));
      if (worst != 2 * n - 3) begin errors++; $display("n = %0d: the simple algorithm's worst is %0d, expected %0d", n, worst, 2 * n - 3); end
    end

    for (int n = 1; n <= 8; n++) begin
      got = pancake_number(n);
      $display("P(%0d) = %0d", n, got);
      if (got != want_p[n - 1]) begin errors++; $display("expected %0d", want_p[n - 1]); end
    end

    s = '{1, -2, 3};
    burnt_flip(s, 2);
    if (s != '{2, -1, 3}) begin errors++; $display("burnt_flip of 2 on [1, -2, 3]"); end
    s = '{-1, -2, -3};
    n_flips = burnt_simple(s, flips);
    $display("burnt_simple [-1, -2, -3]: %0d flips: %s", n_flips, flips);
    if (n_flips != 7 || flips != "3 1 3 2 1 2 1 " || !is_sorted(s)) begin errors++; $display("expected 3 1 3 2 1 2 1"); end

    for (int n = 1; n <= 5; n++) begin
      p.delete();
      for (int i = 1; i <= n; i++) p.push_back(i);
      worst = 0;
      do begin
        for (int m = 0; m < (1 << n); m++) begin
          s = p;
          foreach (s[i]) if (m[i]) s[i] = -s[i];
          n_flips = burnt_simple(s, flips);
          if (!is_sorted(s)) begin errors++; $display("n = %0d: a burnt stack is not sorted", n); end
          if (n_flips > worst) worst = n_flips;
        end
      end while (next_perm(p));
      if (worst != 3 * n - 2) begin errors++; $display("n = %0d: burnt worst %0d, expected %0d", n, worst, 3 * n - 2); end
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
