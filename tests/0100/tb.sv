//@flags --timing
//@page function automatic longint unsigned count_ways(int n, int steps[$]);
//@page module stairs_ways
//@page function automatic longint unsigned count_multisets
//@page function automatic longint unsigned count_ways_exact
// Question 0100: the page's SystemVerilog against references written here independently:
// every climb as the set of stairs it lands on (a bit mask over the stairs 1 .. n-1, the gaps
// checked against S and the broken stairs), its number of jumps for count_ways_exact, and the
// counts of each jump size for count_multisets. stairs_ways is fed a stair a clock (now and
// then with an idle clock), on the page's examples (89, 25, 0) and random sets.
module tb;
  logic clk = 0, rst_n = 0, start = 0, valid = 0, broken = 0;
  logic [6:1] steps = 0;
  logic [63:0] ways;
  int errors = 0;

  stairs_ways #(.K(6), .W(64)) dut (.clk, .rst_n, .start, .valid, .broken, .steps, .ways);
  always #5 clk = ~clk;

  task automatic fail(string what);
    errors++;
    if (errors < 20) $display("%s", what);
  endtask

  function automatic bit has(int s[$], int v);
    foreach (s[k]) if (s[k] == v) return 1;
    return 0;
  endfunction

  // the climbs of n landing on no broken stair, by the stairs they land on; t < 0: any number
  // of jumps, else exactly t jumps
  function automatic longint unsigned ref_ways(int n, int s[$], bit bad[], int t);
    longint unsigned cnt = 0;
    int prev, jumps;
    bit ok;
    if (n == 0) return t <= 0 ? 1 : 0;
    if (bad[n]) return 0;
    for (int mask = 0; mask < (1 << (n - 1)); mask++) begin
      ok = 1; prev = 0; jumps = 0;
      for (int i = 1; i <= n && ok; i++)
        if (i == n || mask[i - 1]) begin
          if (!has(s, i - prev) || bad[i]) ok = 0;
          prev = i; jumps++;
        end
      if (ok && (t < 0 || jumps == t)) cnt++;
    end
    return cnt;
  endfunction

  // the order does not matter: every count of each jump size (sizes 1 to 6)
  function automatic longint unsigned ref_multisets(int n, int s[$]);
    longint unsigned cnt = 0;
    int top[7];
    for (int k = 1; k <= 6; k++) top[k] = has(s, k) ? n / k : 0;
    for (int a = 0; a <= top[1]; a++)
      for (int b = 0; b <= top[2]; b++)
        for (int c = 0; c <= top[3]; c++)
          for (int d = 0; d <= top[4]; d++)
            for (int e = 0; e <= top[5]; e++)
              for (int f = 0; f <= top[6]; f++)
                if (a + 2 * b + 3 * c + 4 * d + 5 * e + 6 * f == n) cnt++;
    return cnt;
  endfunction

  // the stairs 1 .. n into stairs_ways, one a clock after start; the count of every stair
  // is checked against count_ways_broken's table, built here
  task automatic run(int n, int s[$], bit bad[]);
    longint unsigned w[];
    w = new[n + 1];
    w[0] = 1;
    for (int i = 1; i <= n; i++) begin
      w[i] = 0;
      if (!bad[i]) foreach (s[k]) if (s[k] <= i) w[i] += w[i - s[k]];
    end
    steps = '0;
    foreach (s[k]) steps[s[k]] = 1;
    @(negedge clk); start = 1;
    @(negedge clk); start = 0;
    if (ways != 1) fail("start: ways is not 1");
    for (int i = 1; i <= n; i++) begin
      if ($urandom_range(3) == 0) begin valid = 0; @(negedge clk); end
      valid = 1; broken = bad[i];
      @(negedge clk);
      valid = 0; broken = 0;
      if (ways != w[i]) fail($sformatf("stairs_ways stair %0d: %0d, want %0d", i, ways, w[i]));
    end
    if (w[n] != ref_ways(n, s, bad, -1)) fail($sformatf("the table and the listing differ at n = %0d", n));
  endtask

  initial begin
    int s[$], n;
    bit bad[];
    #12 rst_n = 1;

    // the page's examples
    if (count_ways(10, '{1, 2}) != 89 || count_ways(10, '{1, 2, 3}) != 274 || count_ways(10, '{1, 3, 5}) != 47)
      fail("count_ways on the page's examples");
    if (count_multisets(10, '{1, 2}) != 6 || count_multisets(10, '{1, 2, 3}) != 14 || count_multisets(10, '{1, 2, 5}) != 10)
      fail("count_multisets on the page's examples");
    if (count_ways_exact(10, '{1, 2}, 7) != 35) fail("count_ways_exact(10, {1, 2}, 7)");
    if (count_ways(92, '{1, 2}) != 64'd12200160415121876738) fail("count_ways(92, {1, 2}) = F(93)");
    bad = new[11];
    foreach (bad[i]) bad[i] = 0;
    bad[5] = 1;
    run(10, '{1, 2}, bad);
    if (ways != 25) fail($sformatf("stair 5 broken: %0d, want 25", ways));
    bad[6] = 1;
    run(10, '{1, 2}, bad);
    if (ways != 0) fail("stairs 5 and 6 broken: not 0");

    // random sets, stairs and broken stairs against the listings
    repeat (120) begin
      s = {};
      for (int v = 1; v <= 6; v++) if ($urandom_range(2) == 0) s.push_back(v);
      if (s.size() == 0) s.push_back(1 + $urandom_range(5));
      n = 1 + $urandom_range(13);
      bad = new[n + 1];
      foreach (bad[i]) bad[i] = 0;
      if (count_ways(n, s) != ref_ways(n, s, bad, -1)) fail($sformatf("count_ways(%0d)", n));
      if (count_multisets(n, s) != ref_multisets(n, s)) fail($sformatf("count_multisets(%0d)", n));
      for (int t = 0; t <= n + 1; t++)
        if (count_ways_exact(n, s, t) != ref_ways(n, s, bad, t)) fail($sformatf("count_ways_exact(%0d, t = %0d)", n, t));
      for (int i = 1; i <= n; i++) bad[i] = $urandom_range(4) == 0;
      run(n, s, bad);
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
