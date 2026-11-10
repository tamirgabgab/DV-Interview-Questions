//@flags --assert --timing
// Question 0036: the page's lfsr_next and lfsr_period: the two example periods (15 and 6),
// the sequence of the maximal polynomial visits every non-zero state once, zero is a fixed
// point, and the period from 0001 of every x^4 + ... + 1 matches the page table.
// The hardware follow-up: the page's module lfsr against lfsr_next clock by clock, and
// lfsr_sva on six of them: both primitive polynomials and the 8-bit one pass with full
// coverage; x^4 + x^2 + 1 (period 6) fails a_period and a_first and fills 6 of 15 bins;
// x^4 + x^3 + x^2 + x + 1 (period 5) passes a_period and fails only a_first; a seed of
// zero fails a_nonzero. The two primitive polynomials give different output streams, one
// the time reverse of the other.
//@page module lfsr #(
//@page module lfsr_sva

module tb;
  //@page function automatic int lfsr_next

  int errors = 0;

  logic clk = 0, rst_n = 0;
  always #5 clk = ~clk;
  logic [3:0] s1, s2, s3, s4, s6;
  logic [7:0] s5;
  logic o1, o2, o3, o4, o5, o6;
  lfsr #(.W(4), .TAPS(4'b0011), .SEED(4'b0001)) u1 (.clk, .rst_n, .state(s1), .out(o1));
  lfsr #(.W(4), .TAPS(4'b1001), .SEED(4'b1000)) u2 (.clk, .rst_n, .state(s2), .out(o2));
  lfsr #(.W(4), .TAPS(4'b0101), .SEED(4'b0010)) u3 (.clk, .rst_n, .state(s3), .out(o3));
  lfsr #(.W(4), .TAPS(4'b1111), .SEED(4'b0011)) u4 (.clk, .rst_n, .state(s4), .out(o4));
  lfsr #(.W(8), .TAPS(8'h1D),   .SEED(8'hFF))   u5 (.clk, .rst_n, .state(s5), .out(o5));
  lfsr #(.W(4), .TAPS(4'b0011), .SEED(4'b0000)) u6 (.clk, .rst_n, .state(s6), .out(o6));
  // every checker has its own parameters: two instances of one parameterization of a
  // module with a covergroup do not compile here
  lfsr_sva #(.W(4), .SEED(4'b0001)) c1 (.clk, .rst_n, .state(s1));
  lfsr_sva #(.W(4), .SEED(4'b1000)) c2 (.clk, .rst_n, .state(s2));
  lfsr_sva #(.W(4), .SEED(4'b0010)) c3 (.clk, .rst_n, .state(s3));
  lfsr_sva #(.W(4), .SEED(4'b0011)) c4 (.clk, .rst_n, .state(s4));
  lfsr_sva #(.W(8), .SEED(8'hFF))   c5 (.clk, .rst_n, .state(s5));
  lfsr_sva #(.W(4), .SEED(4'b0000)) c6 (.clk, .rst_n, .state(s6));
  int f_period3 = 0, f_first3 = 0, f_period4 = 0, f_first4 = 0;
  // which assertion fails: the period-6 and the period-5 register, counted apart
  always @(posedge clk) if (rst_n) begin
    if (s3 == 4'b0010) f_first3 <= f_first3 + 1;
    if (s4 == 4'b0011) f_first4 <= f_first4 + 1;
  end

  task automatic hw();
    bit a[15], b[15];
    int m1, m2, m5;
    bit rev;
    repeat (2) @(posedge clk);
    #1 rst_n = 1;
    m1 = 1; m2 = 8; m5 = 255;
    for (int t = 0; t < 600; t++) begin
      if (s1 !== 4'(m1) || s2 !== 4'(m2) || s5 !== 8'(m5)) begin errors++; $display("clock %0d: %04b %04b %02h", t, s1, s2, s5); end
      if (o1 !== s1[0]) begin errors++; $display("out is not s[0]"); end
      if (t < 15) begin a[t] = o1; b[t] = o2; end
      m1 = lfsr_next(m1, 4'b0011, 4); m2 = lfsr_next(m2, 4'b1001, 4); m5 = lfsr_next(m5, 8'h1D, 8);
      @(posedge clk); #1;
    end
    // the output of x^4 + x + 1 is the output of x^4 + x^3 + 1 read backwards, from some phase
    rev = 0;
    for (int sh = 0; sh < 15; sh++) begin
      bit ok = 1;
      for (int i = 0; i < 15; i++) if (b[14 - i] != a[(i + sh) % 15]) ok = 0;
      if (ok) rev = 1;
    end
    if (!rev) begin errors++; $display("the two primitive polynomials: not reversed streams"); end
    begin
      bit same = 1;
      for (int i = 0; i < 15; i++) if (a[i] != b[i]) same = 0;
      if (same) begin errors++; $display("the two primitive polynomials gave one stream"); end
    end
    if (c1.fails != 0 || c2.fails != 0 || c5.fails != 0) begin errors++; $display("a primitive polynomial failed: %0d %0d %0d", c1.fails, c2.fails, c5.fails); end
    if (c1.cov.get_inst_coverage() < 99.999 || c2.cov.get_inst_coverage() < 99.999 || c5.cov.get_inst_coverage() < 99.999) begin
      errors++; $display("coverage %f %f %f", c1.cov.get_inst_coverage(), c2.cov.get_inst_coverage(), c5.cov.get_inst_coverage());
    end
    if (c3.fails == 0 || c4.fails == 0 || c6.fails == 0) begin errors++; $display("a bad register passed: %0d %0d %0d", c3.fails, c4.fails, c6.fails); end
    // period 6: 6 of 15 bins; period 5: 5 of 15, and only a_first fails (once per visit of the seed)
    if (c3.cov.get_inst_coverage() < 39.9 || c3.cov.get_inst_coverage() > 40.1) begin errors++; $display("period 6 coverage %f", c3.cov.get_inst_coverage()); end
    if (c4.cov.get_inst_coverage() < 33.2 || c4.cov.get_inst_coverage() > 33.4) begin errors++; $display("period 5 coverage %f", c4.cov.get_inst_coverage()); end
    if (c4.fails > f_first4) begin errors++; $display("period 5: %0d fails for %0d visits of the seed, a_period failed too", c4.fails, f_first4); end
    if (c3.fails <= f_first3) begin errors++; $display("period 6: a_period did not fail (%0d fails, %0d visits)", c3.fails, f_first3); end
    if (c6.cov.get_inst_coverage() > 0.001) begin errors++; $display("the zero seed covered a bin"); end
  endtask

  initial begin
    int expected[8] = '{4, 15, 6, 15, 7, 6, 7, 5};       // masks 0001, 0011, 0101, 1001, 0111, 1011, 1101, 1111
    int masks[8]    = '{4'b0001, 4'b0011, 4'b0101, 4'b1001, 4'b0111, 4'b1011, 4'b1101, 4'b1111};
    bit seen[16];
    int s;

    hw();

    if (lfsr_period(4'b0011, 4) != 15) begin errors++; $display("x^4+x^3+1 period %0d", lfsr_period(4'b0011, 4)); end
    if (lfsr_period(4'b0101, 4) != 6) begin errors++; $display("x^4+x^2+1 period %0d", lfsr_period(4'b0101, 4)); end
    if (lfsr_next(4'b0000, 4'b0011, 4) != 0) begin errors++; $display("zero is not a fixed point"); end

    s = 1;
    for (int k = 0; k < 15; k++) begin
      if (s == 0 || seen[s]) begin errors++; $display("state %04b repeated or zero at step %0d", s, k); end
      seen[s] = 1;
      s = lfsr_next(s, 4'b0011, 4);
    end
    if (s != 1) begin errors++; $display("did not return to 0001 after 15 steps"); end

    foreach (masks[i])
      if (lfsr_period(masks[i], 4) != expected[i]) begin
        errors++; $display("mask %04b: period %0d, expected %0d", masks[i], lfsr_period(masks[i], 4), expected[i]);
      end

    // a maximal 8-bit polynomial: x^8 + x^6 + x^5 + x^4 + 1 (mask bits 0, 2, 3, 4)
    if (lfsr_period(8'b00011101, 8) != 255) begin errors++; $display("8-bit period %0d", lfsr_period(8'b00011101, 8)); end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
