//@flags --timing
//@page function automatic bit luhn_ok
//@page function automatic bit isbn10_ok
//@page module luhn_checker
//@page class luhn_gen
// Question 0098: the page's luhn_ok and isbn10_ok on the test numbers of the page; the page's
// luhn_gen randomized with valid fixed to 0 and to 1, every number checked by luhn_ok and
// fed to the page's luhn_checker one digit a clock (check digit first); and every single
// change and every neighbour swap of the sample numbers fed to the checker, which must agree
// with luhn_ok: every single change caught, only the 0 / 9 swap of 4111 1111 1110 9115
// slipping by.
module tb;
  logic clk = 0, rst_n = 0, in_valid = 0, start = 0, last = 0;
  logic [3:0] digit = 0;
  logic done, ok;
  int errors = 0;

  luhn_checker dut (.clk, .rst_n, .in_valid, .start, .last, .digit, .done, .ok);

  always #5 clk = ~clk;

  // a string of digits as the queue luhn_ok takes, leftmost first
  function automatic void to_q(string s, ref byte unsigned q[$]);
    q.delete();
    for (int i = 0; i < s.len(); i++) q.push_back(byte'(s[i] - "0"));
  endfunction

  // feed a number to the checker, its rightmost digit first; returns ok
  task automatic run(byte unsigned q[$], output bit got);
    int n;
    n = q.size();
    for (int k = 0; k < n; k++) begin
      @(negedge clk);
      in_valid = 1;
      start = (k == 0);
      last = (k == n - 1);
      digit = q[n - 1 - k];
    end
    @(negedge clk);
    in_valid = 0;
    start = 0;
    last = 0;
    if (!done) begin errors++; $display("done is not high one cycle after last"); end
    got = ok;
  endtask

  task automatic expect_ok(string s, bit want);
    byte unsigned q[$];
    bit got;
    to_q(s, q);
    if (luhn_ok(q) != want) begin errors++; $display("luhn_ok(%s) = %0d, expected %0d", s, luhn_ok(q), want); end
    run(q, got);
    if (got != want) begin errors++; $display("checker(%s) = %0d, expected %0d", s, got, want); end
  endtask

  // every single change and every swap of two different neighbours of a valid sample;
  // returns how many swaps slip by (checker and model must agree on each)
  task automatic mutate_all(string s, output int singles, output int slipped);
    byte unsigned q[$], m[$];
    bit got, want;
    singles = 0;
    slipped = 0;
    to_q(s, q);
    for (int i = 0; i < q.size(); i++)
      for (int b = 0; b < 10; b++)
        if (b != q[i]) begin
          m = q;
          m[i] = byte'(b);
          run(m, got);
          if (got || luhn_ok(m)) begin errors++; $display("%s: the change of place %0d to %0d slipped by", s, i, b); end
          singles++;
        end
    for (int i = 0; i + 1 < q.size(); i++)
      if (q[i] != q[i + 1]) begin
        m = q;
        m[i] = q[i + 1];
        m[i + 1] = q[i];
        want = luhn_ok(m);
        run(m, got);
        if (got != want) begin errors++; $display("%s: swap at %0d, checker %0d, model %0d", s, i, got, want); end
        if (want) slipped++;
      end
  endtask

  initial begin
    luhn_gen g;
    byte unsigned q[$], v[10];
    bit got;
    int singles, slipped, valids;
    #12 rst_n = 1;

    // the page's numbers
    expect_ok("4111111111111111", 1);
    expect_ok("4111111111111112", 0);
    expect_ok("4111111111111110", 0);
    expect_ok("5555555555554444", 1);
    expect_ok("378282246310005", 1);
    expect_ok("4111111111109115", 1);
    expect_ok("4111111111190115", 1);
    expect_ok("000000018", 1);
    expect_ok("000000019", 0);
    v = '{0, 3, 0, 6, 4, 0, 6, 1, 5, 2};
    if (!isbn10_ok(v)) begin errors++; $display("isbn10_ok(0306406152) failed"); end
    v = '{0, 8, 0, 4, 4, 2, 9, 5, 7, 10};
    if (!isbn10_ok(v)) begin errors++; $display("isbn10_ok(080442957X) failed"); end
    v = '{0, 3, 0, 6, 4, 0, 6, 1, 5, 3};
    if (isbn10_ok(v)) begin errors++; $display("isbn10_ok(0306406153) passed"); end

    // the generator: valid fixed each call; luhn_ok and the checker agree with it
    g = new;
    valids = 0;
    for (int k = 0; k < 400; k++) begin
      bit want;
      want = k % 2;
      if (!g.randomize() with { valid == want; }) begin errors++; $display("randomize failed"); end
      q.delete();
      for (int i = 15; i >= 0; i--) q.push_back(byte'(g.d[i]));
      foreach (q[i]) if (q[i] > 9) begin errors++; $display("a digit over 9"); end
      if (luhn_ok(q) != want) begin errors++; $display("generated valid=%0d but luhn_ok=%0d", want, luhn_ok(q)); end
      run(q, got);
      if (got != want) begin errors++; $display("generated valid=%0d but the checker said %0d", want, got); end
      valids += got;
    end
    if (valids != 200) begin errors++; $display("%0d valid numbers of 400, expected 200", valids); end

    // every single error and every neighbour swap of the samples
    mutate_all("4111111111111111", singles, slipped);
    if (singles != 144 || slipped != 0) begin errors++; $display("4111...1111: %0d singles, %0d slipped", singles, slipped); end
    mutate_all("5555555555554444", singles, slipped);
    if (singles != 144 || slipped != 0) begin errors++; $display("5555...4444: %0d singles, %0d slipped", singles, slipped); end
    mutate_all("4111111111109115", singles, slipped);
    if (singles != 144 || slipped != 1) begin errors++; $display("4111...9115: %0d singles, %0d slipped", singles, slipped); end

    if (errors == 0) $display("PASS");
    else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
