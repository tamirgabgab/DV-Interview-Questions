// Question 0106: the page's single_twice, single_thrice_count, single_thrice, single_thrice_any
// and single_mod_k on the page's examples, the edge cases (one number, the extremes of 32 bits)
// and random shuffled arrays where every value appears k times but one, which appears p times.
module tb;
  //@page function automatic int single_twice
  //@page function automatic int single_thrice_count
  //@page function automatic int single_mod_k

  int errors = 0;

  function automatic void check(string what, int got, int want);
    if (got != want) begin errors++; $display("%s: %0d, expected %0d", what, got, want); end
  endfunction

  // an array where `single` appears p times and every value of `others` k times, shuffled
  function automatic void build(int single, int p, int others[], int k, output int nums[]);
    int q[$];
    repeat (p) q.push_back(single);
    foreach (others[i]) repeat (k) q.push_back(others[i]);
    q.shuffle();
    nums = new[q.size()];
    foreach (q[i]) nums[i] = q[i];
  endfunction

  function automatic int rnd(int span);
    int v = $urandom();
    if (span == 0) return v;
    return $signed($urandom_range(2 * span, 0)) - span;
  endfunction

  initial begin
    int nums[], others[], single, k, p, n, span;
    int spans[4] = '{5, 50, 1000, 0};
    bit fresh;
    // the page's examples
    nums = '{4, 1, 2, 1, 2};                      check("twice", single_twice(nums), 4);
    nums = '{2, 2, 3, 2};                         check("count", single_thrice_count(nums), 3);
                                                  check("thrice", single_thrice(nums), 3);
                                                  check("mod 3", single_mod_k(nums, 3), 3);
    nums = '{0, 1, 0, 1, 0, 1, 99};               check("99 count", single_thrice_count(nums), 99);
                                                  check("99", single_thrice(nums), 99);
    nums = '{-2, -2, 1, 1, -3, 1, -3, -3, -4, -2}; check("negative count", single_thrice_count(nums), -4);
                                                  check("negative", single_thrice(nums), -4);
                                                  check("negative any", single_thrice_any(nums), -4);
    nums = '{5, 5, 7, 7, 7};                      check("twice among threes", single_thrice_any(nums), 5);
                                                  check("twice among threes, mod 3", single_mod_k(nums, 3), 5);
    nums = '{7, -1, 6, 7, -1, 7, 6, -1, 7, -1, 7, -1}; check("k = 5", single_mod_k(nums, 5), 6);
    // edge cases
    nums = '{7};                                  check("one", single_thrice(nums), 7);
                                                  check("one count", single_thrice_count(nums), 7);
    nums = '{32'h8000_0000};                      check("min", single_thrice_count(nums), 32'h8000_0000);
                                                  check("min thrice", single_thrice(nums), 32'h8000_0000);
    nums = '{-1, -1, -1, 32'h8000_0000};          check("min among -1", single_thrice(nums), 32'h8000_0000);
    nums = '{32'h7fff_ffff, 0, 32'h7fff_ffff, 32'h7fff_ffff}; check("zero", single_thrice_count(nums), 0);
    // random arrays
    for (int r = 0; r < 3000; r++) begin
      span = spans[r % 4];
      n = $urandom_range(7, 0);
      single = rnd(span);
      others = new[n];
      foreach (others[i]) begin
        do begin
          others[i] = rnd(span);
          fresh = others[i] != single;
          for (int j = 0; j < i; j++) if (others[j] == others[i]) fresh = 0;
        end while (!fresh);
      end
      build(single, 1, others, 2, nums);
      check($sformatf("run %0d twice", r), single_twice(nums), single);
      build(single, 1, others, 3, nums);
      check($sformatf("run %0d count", r), single_thrice_count(nums), single);
      check($sformatf("run %0d thrice", r), single_thrice(nums), single);
      check($sformatf("run %0d any", r), single_thrice_any(nums), single);
      build(single, 2, others, 3, nums);
      check($sformatf("run %0d any twice", r), single_thrice_any(nums), single);
      k = $urandom_range(9, 2);
      p = $urandom_range(2 * k, 1);
      if (p % k == 0) p++;
      build(single, p, others, k, nums);
      check($sformatf("run %0d mod %0d, p %0d", r, k, p), single_mod_k(nums, k), single);
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
