//@flags --assert --timing
//@page function automatic logic [7:0] isqrt16
//@page module isqrt_seq
//@page function automatic void divide16
// Question 0097: the page's SystemVerilog. isqrt16 on every 16-bit input against a reference
// that counts up the squares; isqrt_seq on every 16-bit input through start / busy / done,
// with the page's checker (isqrt_check) bound to it, 8 busy clocks each and rem = n - root²,
// and the trace of n = 1000 clock by clock (root, rem, k and the trial, as the page's table); divide16 against / and % on every dividend with
// many divisors (and d = 0); icbrt24 on every n below 2^20 and around every cube up to 255³.
module tb;
  logic clk = 0, rst_n = 0, start = 0;
  logic [15:0] n_in = 0;
  logic        busy, done;
  logic [7:0]  root;
  logic [15:0] rem;
  int errors = 0;

  isqrt_seq   dut (.clk, .rst_n, .start, .n(n_in), .busy, .done, .root, .rem);
  isqrt_check chk (.clk, .done, .n(n_in), .root);

  always #5 clk = ~clk;

  task automatic fail(string what);
    errors++;
    if (errors < 20) $display("%s", what);
  endtask

  // run the module on n: start for one clock, count the busy clocks, check the result
  task automatic run(int n, output int r, output int rr, output int cycles);
    @(negedge clk) begin n_in = 16'(n); start = 1; end
    @(negedge clk) start = 0;
    cycles = 0;
    while (!done) begin
      if (busy) cycles++;
      @(negedge clk);
    end
    r = root; rr = rem;
  endtask

  initial begin
    int s, r, rr, cyc, want_q, want_r;
    logic [15:0] q16, r16;
    int trace_root[$], trace_rem[$], trace_k[$], trace_trial[$];
    int ds[10] = '{1, 2, 3, 7, 10, 255, 256, 1000, 40000, 65535};

    // isqrt16 on every input; s steps up through the squares
    s = 0;
    for (int n = 0; n < 65536; n++) begin
      if ((s + 1) * (s + 1) <= n) s++;
      if (isqrt16(16'(n)) != s) fail($sformatf("isqrt16(%0d) = %0d, want %0d", n, isqrt16(16'(n)), s));
    end

    // the module: the trace of 1000 first, clock by clock after start
    repeat (2) @(posedge clk);
    #1 rst_n = 1;
    @(negedge clk) begin n_in = 1000; start = 1; end
    @(negedge clk) start = 0;
    while (!done) begin
      trace_root.push_back(root); trace_rem.push_back(rem);
      trace_k.push_back(dut.k); trace_trial.push_back(dut.trial);
      @(negedge clk);
    end
    trace_root.push_back(root); trace_rem.push_back(rem);
    if (trace_root.size() != 9) fail($sformatf("1000: %0d clocks, want 9", trace_root.size()));
    begin
      int wr[9] = '{0, 0, 0, 0, 16, 24, 28, 30, 31};
      int wm[9] = '{1000, 1000, 1000, 1000, 744, 424, 216, 100, 39};
      foreach (wr[i]) if (i < trace_root.size() && (trace_root[i] != wr[i] || trace_rem[i] != wm[i]))
        fail($sformatf("1000 clock %0d: root %0d rem %0d, want %0d %0d", i, trace_root[i], trace_rem[i], wr[i], wm[i]));
    end
    // the page's table: k and the trial in the busy cycles 1 to 8
    begin
      int wk[8] = '{7, 6, 5, 4, 3, 2, 1, 0};
      int wt[8] = '{16384, 4096, 1024, 256, 320, 208, 116, 61};
      foreach (wk[i]) if (i < trace_k.size() && (trace_k[i] != wk[i] || trace_trial[i] != wt[i]))
        fail($sformatf("1000 cycle %0d: k %0d trial %0d, want %0d %0d", i + 1, trace_k[i], trace_trial[i], wk[i], wt[i]));
    end
    @(negedge clk);
    if (done) fail("done stays high for more than one clock");

    // the module on every input
    s = 0;
    for (int n = 0; n < 65536; n++) begin
      if ((s + 1) * (s + 1) <= n) s++;
      run(n, r, rr, cyc);
      if (r != s || rr != n - s * s || cyc != 8)
        fail($sformatf("isqrt_seq(%0d): root %0d rem %0d after %0d busy clocks, want %0d %0d 8", n, r, rr, cyc, s, n - s * s));
    end

    // divide16: every dividend with a set of divisors, and the division by zero
    for (int a = 0; a < 65536; a++)
      foreach (ds[i]) begin
        divide16(16'(a), 16'(ds[i]), q16, r16);
        if (q16 != a / ds[i] || r16 != a % ds[i]) fail($sformatf("divide16(%0d, %0d) = %0d r %0d", a, ds[i], q16, r16));
      end
    for (int k = 0; k < 20000; k++) begin
      int a, d;
      a = $urandom_range(65535); d = $urandom_range(65535, 1);
      divide16(16'(a), 16'(d), q16, r16);
      if (q16 != a / d || r16 != a % d) fail($sformatf("divide16(%0d, %0d) = %0d r %0d", a, d, q16, r16));
    end
    divide16(16'd1000, 16'd0, q16, r16);
    if (q16 != 16'hffff || r16 != 1000) fail($sformatf("divide16(1000, 0) = %0d r %0d", q16, r16));
    divide16(16'd1000, 16'd7, q16, r16);
    if (q16 != 142 || r16 != 6) fail($sformatf("divide16(1000, 7) = %0d r %0d", q16, r16));

    // icbrt24: every n below 2^20, then around every cube
    s = 0;
    for (int n = 0; n < (1 << 20); n++) begin
      if ((s + 1) * (s + 1) * (s + 1) <= n) s++;
      if (icbrt24(24'(n)) != s) fail($sformatf("icbrt24(%0d) = %0d, want %0d", n, icbrt24(24'(n)), s));
    end
    for (int c = 1; c < 256; c++) begin
      int c3;
      c3 = c * c * c;
      if (icbrt24(24'(c3)) != c) fail($sformatf("icbrt24(%0d^3) = %0d", c, icbrt24(24'(c3))));
      if (icbrt24(24'(c3 - 1)) != c - 1) fail($sformatf("icbrt24(%0d^3 - 1) = %0d", c, icbrt24(24'(c3 - 1))));
    end
    if (icbrt24(24'hffffff) != 255) fail("icbrt24(2^24 - 1) != 255");
    if (icbrt24(24'd1000) != 10) fail("icbrt24(1000) != 10");

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
