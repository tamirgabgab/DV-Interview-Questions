//@flags --timing
// Question 0110: the page's six modules, the code under review of every part and its fix, run
// side by side on the inputs of the page's waveforms. Every cycle is checked against the want
// strings below (tests/0110/test_0110.py checks the same strings against the references of
// tools/figures/q0110.py, the page's Python models and the figures). Then random runs: the
// fixed delay line, gate and average meet the designer's intent (the average on all 65,536
// pairs), and the code under review behaves exactly as the solutions explain (q3 one cycle
// behind d, y holding the last d with en high, avg 128 too small whenever a + b >= 256). Also
// the traps: the blocking lines in reverse order, the race of a swap with blocking lines in two
// processes, (a + b) / 2, and the follow-ups on widths and signedness.
//@page module delay3 (
//@page module delay3_fixed
//@page module en_gate (
//@page module en_gate_fixed
//@page module avg8 (
//@page module avg8_fixed

// The trap of part a: the page's blocking lines in reverse order, in the module of the page
module delay3_reversed (
  input  logic clk,
  input  logic d,
  output logic q3
);
  logic q1, q2;
  //@page reversed:
endmodule

// The race of the trap: the page's two processes, from a = 3 and b = 9
module swap_race (
  input  logic clk,
  output logic [3:0] a_out,
  output logic [3:0] b_out
);
  logic [3:0] a = 4'd3, b = 4'd9;
  //@page two processes
  assign a_out = a;
  assign b_out = b;
endmodule

// The same two processes with <=, which swap
module swap_nb (
  input  logic clk,
  output logic [3:0] a_out,
  output logic [3:0] b_out
);
  logic [3:0] a = 4'd3, b = 4'd9;
  always_ff @(posedge clk) a <= b;
  always_ff @(posedge clk) b <= a;
  assign a_out = a;
  assign b_out = b;
endmodule

module tb;
  localparam int N = 8;
  // the inputs of the page's waveforms, cycle by cycle (q0110.D_A, EN_B, D_B, A_C, B_C)
  int D_A[N]  = '{0, 1, 1, 0, 1, 0, 0, 0};
  int EN_B[N] = '{0, 1, 1, 0, 0, 1, 0, 0};
  int D_B[N]  = '{3, 5, 9, 12, 7, 6, 10, 1};
  int A_C[N]  = '{10, 100, 200, 127, 128, 255, 255, 60};
  int B_C[N]  = '{20, 50, 100, 128, 128, 255, 1, 61};
  // what the page draws: q1, q2, q3 as bits per cycle, y and avg per cycle
  string WANT_A_BUG[3] = '{"00110100", "00110100", "00110100"};
  string WANT_A_FIX[3] = '{"00110100", "00011010", "00001101"};
  string WANT_B_BUG = "0 5 9 9 9 6 6 6";
  string WANT_B_FIX = "0 5 9 0 0 6 0 0";
  string WANT_C_BUG = "15 75 22 127 0 127 0 60";
  string WANT_C_FIX = "15 75 150 127 128 255 128 60";

  logic clk = 0;
  int errors = 0;

  logic       d = 0, qb3, qf3, qr3;
  logic       en = 0;
  logic [3:0] gd = '0, yb, yf;
  logic [7:0] a = '0, b = '0, avg_b, avg_f;
  logic [3:0] ra, rb, sa, sb;

  delay3          a_bug (.clk, .d, .q3(qb3));
  delay3_fixed    a_fix (.clk, .d, .q3(qf3));
  delay3_reversed a_rev (.clk, .d, .q3(qr3));
  en_gate         b_bug (.en, .d(gd), .y(yb));
  en_gate_fixed   b_fix (.en, .d(gd), .y(yf));
  avg8            c_bug (.a, .b, .avg(avg_b));
  avg8_fixed      c_fix (.a, .b, .avg(avg_f));
  swap_race       race  (.clk, .a_out(ra), .b_out(rb));
  swap_nb         swap  (.clk, .a_out(sa), .b_out(sb));

  task automatic fail(string what);
    errors++;
    if (errors < 20) $display("FAIL: %s", what);
  endtask

  function automatic string join_int(int v[N]);
    string s = "";
    foreach (v[k]) s = {s, k ? " " : "", $sformatf("%0d", v[k])};
    return s;
  endfunction

  // one cycle: the edge that starts it, the inputs just after the edge, then the values
  // during the cycle are read before the next edge
  task automatic edge_then(input logic nd, input logic nen, input logic [3:0] ngd, input logic [7:0] na, input logic [7:0] nb);
    clk = 1;
    #1 d = nd; en = nen; gd = ngd; a = na; b = nb;
    #4 clk = 0;
    #4;
  endtask

  initial begin
    string ab[3], af[3];
    int yb_v[N], yf_v[N], cb_v[N], cf_v[N];
    logic hist[$];
    logic [3:0] held;
    int wrong, big, k;
    logic [7:0] x, y8;
    int i;
    logic [7:0] n;
    logic signed [7:0] s8;

    // --- the page's waveforms, cycle by cycle -----------------------------------------------
    #1;
    if (ra != 4'd3 || rb != 4'd9 || sa != 4'd3 || sb != 4'd9) fail("the swap modules do not start at a = 3, b = 9");
    foreach (ab[r]) begin ab[r] = ""; af[r] = ""; end
    for (k = 0; k < N; k++) begin
      edge_then(D_A[k][0], EN_B[k][0], 4'(D_B[k]), 8'(A_C[k]), 8'(B_C[k]));
      // the race of the trap, at the first edge: the blocking pair leaves a and b equal, at
      // one of the old values; the nonblocking pair swaps them
      if (k == 0 && (ra != rb || !(ra == 4'd3 || ra == 4'd9))) fail($sformatf("swap_race after one edge: a = %0d, b = %0d", ra, rb));
      if (k == 0 && (sa != 4'd9 || sb != 4'd3)) fail($sformatf("swap_nb after one edge: a = %0d, b = %0d", sa, sb));
      ab[0] = {ab[0], $sformatf("%0d", a_bug.q1)}; ab[1] = {ab[1], $sformatf("%0d", a_bug.q2)}; ab[2] = {ab[2], $sformatf("%0d", a_bug.q3)};
      af[0] = {af[0], $sformatf("%0d", a_fix.q1)}; af[1] = {af[1], $sformatf("%0d", a_fix.q2)}; af[2] = {af[2], $sformatf("%0d", a_fix.q3)};
      yb_v[k] = int'(yb); yf_v[k] = int'(yf); cb_v[k] = int'(avg_b); cf_v[k] = int'(avg_f);
      if (qr3 !== a_fix.q3) fail($sformatf("cycle %0d: the reversed lines give q3 = %0d, the fix %0d", k, qr3, a_fix.q3));
    end
    for (int r = 0; r < 3; r++) begin
      if (ab[r] != WANT_A_BUG[r]) fail($sformatf("delay3 q%0d = %s, want %s", r + 1, ab[r], WANT_A_BUG[r]));
      if (af[r] != WANT_A_FIX[r]) fail($sformatf("delay3_fixed q%0d = %s, want %s", r + 1, af[r], WANT_A_FIX[r]));
    end
    if (join_int(yb_v) != WANT_B_BUG) fail($sformatf("en_gate y = %s, want %s", join_int(yb_v), WANT_B_BUG));
    if (join_int(yf_v) != WANT_B_FIX) fail($sformatf("en_gate_fixed y = %s, want %s", join_int(yf_v), WANT_B_FIX));
    if (join_int(cb_v) != WANT_C_BUG) fail($sformatf("avg8 = %s, want %s", join_int(cb_v), WANT_C_BUG));
    if (join_int(cf_v) != WANT_C_FIX) fail($sformatf("avg8_fixed = %s, want %s", join_int(cf_v), WANT_C_FIX));

    // --- part a: 400 random cycles ---------------------------------------------------------
    // q3 of the fix (and of the reversed lines) is d three cycles back; the code under review
    // has q1 = q2 = q3 = d one cycle back
    for (k = 0; k < N; k++) hist.push_back(D_A[k][0]);
    for (k = 0; k < 400; k++) begin
      edge_then(1'($urandom()), 0, '0, '0, '0);
      if (a_fix.q3 !== hist[hist.size() - 3]) fail($sformatf("random cycle %0d: delay3_fixed q3 = %0d, want %0d", k, a_fix.q3, hist[hist.size() - 3]));
      if (qr3 !== hist[hist.size() - 3]) fail($sformatf("random cycle %0d: reversed q3 = %0d", k, qr3));
      if (a_fix.q1 !== hist[hist.size() - 1] || a_fix.q2 !== hist[hist.size() - 2]) fail("random: delay3_fixed q1 / q2");
      if (a_bug.q3 !== hist[hist.size() - 1] || a_bug.q1 !== a_bug.q3 || a_bug.q2 !== a_bug.q3) fail($sformatf("random cycle %0d: delay3 is not d one cycle back", k));
      hist.push_back(d);
    end

    // --- part b: 400 random cycles ---------------------------------------------------------
    // the fix is en ? d : 0; the code under review holds the last d seen with en high
    held = yb;
    for (k = 0; k < 400; k++) begin
      edge_then(0, 1'($urandom_range(2) == 0), 4'($urandom()), '0, '0);
      if (en) held = gd;
      if (yf !== (en ? gd : 4'd0)) fail($sformatf("random cycle %0d: en_gate_fixed y = %0d with en %0d, d %0d", k, yf, en, gd));
      if (yb !== held) fail($sformatf("random cycle %0d: en_gate y = %0d, want the held %0d", k, yb, held));
    end

    // --- part c: all 65,536 pairs ----------------------------------------------------------
    wrong = 0; big = 0;
    for (int va = 0; va < 256; va++)
      for (int vb = 0; vb < 256; vb++) begin
        a = 8'(va); b = 8'(vb);
        #1;
        if (avg_f != 8'((va + vb) / 2)) fail($sformatf("avg8_fixed(%0d, %0d) = %0d", va, vb, avg_f));
        if (avg_b != avg_f) begin
          wrong++;
          if (int'(avg_f) - int'(avg_b) != 128) fail($sformatf("avg8(%0d, %0d) = %0d, not 128 below %0d", va, vb, avg_b, avg_f));
        end
        if ((va + vb >= 256) != (avg_b != avg_f)) fail($sformatf("avg8(%0d, %0d): wrong exactly when a + b >= 256", va, vb));
        if (va + vb >= 256) big++;
      end
    if (wrong != 32640 || big != 32640) fail($sformatf("avg8 is wrong on %0d pairs (%0d with a + b >= 256), want 32640", wrong, big));

    // --- the follow-ups on widths and signedness -------------------------------------------
    x = 8'd200; y8 = 8'd100;
    if ($bits(x + y8) != 8) fail("$bits(a + b) is not 8");
    if ($sformatf("%0d", x + y8) != "44") fail($sformatf("$display of a + b prints %0d", x + y8));
    if (!(x + y8 > 255)) fail("a + b > 255 is false");
    if (x + y8 > 8'd255) fail("a + b > 8'd255 is true");
    if (8'((x + y8) / 2) != 8'd150) fail("(a + b) / 2 is not 150");
    if (8'((x + y8) / 8'd2) != 8'd22) fail("(a + b) / 8'd2 is not 22");
    if (8'((x + y8) >> 1) != 8'd22) fail("(a + b) >> 1 in 8 bits is not 22");
    i = -1; n = 8'd5; s8 = -8'sd1;
    if (i < n) fail("int -1 < logic [7:0] 5 is true");
    if (s8 < n) fail("logic signed [7:0] -1 < logic [7:0] 5 is true");
    if (!(i < int'(n))) fail("-1 < int'(n) is false");
    if (!(s8 < 5)) fail("logic signed [7:0] -1 < 5 is false");

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end

endmodule
