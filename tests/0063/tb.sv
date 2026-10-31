//@flags --timing
// Question 0063: the page's window_max and longest_within against every window, on the
// page's examples, the self-checks and random arrays; and the page's module win_max on
// four lanes (K = 3 on the page's stream then random samples, K = 1, K = 5 with many equal
// samples, K = 8) against the maximum of the last K samples kept in a queue.
//@page module win_max

module tb;
  //@page function automatic void window_max
  //@page function automatic int longest_within

  int errors = 0;

  // every window scanned
  function automatic void brute_max(int nums[], int k, output int out[$]);
    int m;
    out = {};
    for (int i = 0; i + k <= nums.size(); i++) begin
      m = nums[i];
      for (int j = i; j < i + k; j++) if (nums[j] > m) m = nums[j];
      out.push_back(m);
    end
  endfunction

  // every window tried
  function automatic int brute_limit(int nums[], int limit);
    int best = 0, hi, lo;
    for (int i = 0; i < nums.size(); i++) begin
      hi = nums[i]; lo = nums[i];
      for (int j = i; j < nums.size(); j++) begin
        if (nums[j] > hi) hi = nums[j];
        if (nums[j] < lo) lo = nums[j];
        if (hi - lo <= limit && j - i + 1 > best) best = j - i + 1;
      end
    end
    return best;
  endfunction

  // --- the module: four lanes, a sample every cycle -------------------------------------
  localparam int L = 4;
  localparam int KS[L] = '{3, 1, 5, 8};
  logic clk = 0, rst_n = 0;
  logic [7:0] x[L], mx[L];
  always #5 clk = ~clk;

  win_max #(.K(3), .W(8)) dut0 (.clk, .rst_n, .x(x[0]), .max_out(mx[0]));
  win_max #(.K(1), .W(8)) dut1 (.clk, .rst_n, .x(x[1]), .max_out(mx[1]));
  win_max #(.K(5), .W(8)) dut2 (.clk, .rst_n, .x(x[2]), .max_out(mx[2]));
  win_max #(.K(8), .W(8)) dut3 (.clk, .rst_n, .x(x[3]), .max_out(mx[3]));

  initial begin
    int nums[], out[$], want[$], q[$], hist[L][$], m, n, k, limit, page_out[$];
    int stream[8] = '{9, 7, 5, 3, 6, 2, 8, 1};
    // part a on the page's example and the edges
    nums = '{1, 3, -1, -3, 5, 3, 6, 7};
    window_max(nums, 3, out);
    want = '{3, 3, 5, 5, 6, 7};
    if (out != want) begin errors++; $display("page example a"); end
    window_max(nums, 8, out);
    want = '{7};
    if (out != want) begin errors++; $display("k = n"); end
    nums = '{5, 5, 1};
    window_max(nums, 2, out);
    want = '{5, 5};
    if (out != want) begin errors++; $display("5 5 1"); end
    // part b on the page's examples and the self-check
    nums = '{10, 1, 2, 4, 7, 2};
    if (longest_within(nums, 5) != 4) begin errors++; $display("page example b: %0d", longest_within(nums, 5)); end
    nums = '{8, 2, 4, 7};
    if (longest_within(nums, 4) != 2) begin errors++; $display("8 2 4 7"); end
    nums = '{4, 2, 2, 2, 4, 4, 2, 2};
    if (longest_within(nums, 0) != 3) begin errors++; $display("limit 0"); end
    nums = '{1, 5, 6, 7, 8, 10, 6, 5, 6};
    if (longest_within(nums, 4) != 5) begin errors++; $display("self-check b"); end
    nums = new[0];
    if (longest_within(nums, 2) != 0) begin errors++; $display("empty"); end
    for (int r = 0; r < 2000; r++) begin
      n = $urandom_range(1, 14);
      nums = new[n];
      foreach (nums[i]) nums[i] = int'($urandom_range(0, 10)) - 5;
      k = $urandom_range(1, n);
      limit = $urandom_range(0, 6);
      window_max(nums, k, out);
      brute_max(nums, k, want);
      if (out != want) begin errors++; $display("run %0d k %0d: window_max", r, k); end
      if (longest_within(nums, limit) != brute_limit(nums, limit)) begin
        errors++; $display("run %0d limit %0d: %0d vs %0d", r, limit, longest_within(nums, limit), brute_limit(nums, limit));
      end
    end

    // the module: the samples change at the falling edge, the output is read before the next
    for (int l = 0; l < L; l++) x[l] = '0;
    repeat (2) @(negedge clk);
    rst_n = 1;
    for (int c = 0; c <= 600; c++) begin
      @(negedge clk);
      if (c > 0) begin
        for (int l = 0; l < L; l++) begin
          m = 0;
          for (int j = (hist[l].size() > KS[l] ? hist[l].size() - KS[l] : 0); j < hist[l].size(); j++)
            if (hist[l][j] > m) m = hist[l][j];
          if (mx[l] != 8'(m)) begin errors++; $display("lane %0d (K = %0d) cycle %0d: max_out %0d, expected %0d", l, KS[l], c - 1, mx[l], m); end
          if (l == 0 && c <= 8) page_out.push_back(mx[0]);
        end
      end
      if (c < 600) begin
        x[0] = c < 8 ? 8'(stream[c]) : 8'($urandom_range(0, 255));
        x[1] = 8'($urandom_range(0, 255));
        x[2] = 8'($urandom_range(0, 3));                      // many equal samples
        x[3] = (c % 40 < 10) ? 8'(200 - c % 40) : 8'($urandom_range(0, 60));   // decreasing runs fill the entries
        for (int l = 0; l < L; l++) hist[l].push_back(x[l]);
      end
    end
    want = '{9, 9, 9, 7, 6, 6, 8, 8};
    if (page_out != want) begin errors++; $display("the page's stream"); end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
