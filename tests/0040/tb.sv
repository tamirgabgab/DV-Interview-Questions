//@flags --timing
//@page module seq_detect_1011
//@page module seq_detect #(
// Question 0040: the page's seq_detect_1011 and the parametrised seq_detect (several
// patterns, Mealy and Moore) on random bit streams, against a reference that compares
// the last L bits with the pattern (Moore: one cycle later); the stream of the question
// gives exactly the two detections at cycles 4 and 7.
module tb;
  logic clk = 0, rst_n = 0, din = 0;
  logic f1011, fa, fb, fc, fd, fe, fm;
  int errors = 0, hits = 0;
  logic hist[$];                     // the bits sampled so far

  seq_detect_1011 dut1011 (.clk, .rst_n, .din, .found(f1011));
  seq_detect #(.L(4), .PATTERN(4'b1011))             da (.clk, .rst_n, .din, .found(fa));
  seq_detect #(.L(4), .PATTERN(4'b0110))             db (.clk, .rst_n, .din, .found(fb));
  seq_detect #(.L(4), .PATTERN(4'b1111))             dc (.clk, .rst_n, .din, .found(fc));
  seq_detect #(.L(5), .PATTERN(5'b10101))            dd (.clk, .rst_n, .din, .found(fd));
  seq_detect #(.L(1), .PATTERN(1'b1))                de (.clk, .rst_n, .din, .found(fe));
  seq_detect #(.L(4), .PATTERN(4'b1011), .MOORE(1))  dm (.clk, .rst_n, .din, .found(fm));

  always #5 clk = ~clk;

  // 1 when the last L sampled bits (ending `back` cycles ago) equal the pattern
  function automatic bit tail_is(int L, logic [0:7] pat, int back);
    int n = hist.size() - back;
    if (n < L) return 0;
    for (int i = 0; i < L; i++) if (hist[n - L + i] !== pat[i]) return 0;
    return 1;
  endfunction

  task automatic check(string what, logic got, bit want);
    if (got !== want) begin errors++; if (errors < 20) $display("%s: got %0d, expected %0d after %0d bits", what, got, want, hist.size()); end
  endtask

  // drive a bit on the falling edge; the Mealy outputs are checked while it is on the line,
  // the Moore output after the rising edge that samples it
  task automatic feed(bit b);
    @(negedge clk) din = b;
    #1;
    hist.push_back(b);
    check("seq_detect_1011", f1011, tail_is(4, 8'b1011_0000, 0));
    check("1011", fa, tail_is(4, 8'b1011_0000, 0));
    check("0110", fb, tail_is(4, 8'b0110_0000, 0));
    check("1111", fc, tail_is(4, 8'b1111_0000, 0));
    check("10101", fd, tail_is(5, 8'b10101_000, 0));
    check("1", fe, tail_is(1, 8'b1000_0000, 0));
    check("1011 moore", fm, tail_is(4, 8'b1011_0000, 1));
    if (f1011) hits++;
  endtask

  initial begin
    repeat (2) @(posedge clk);
    #1 rst_n = 1;
    foreach (hist[i]) hist.delete();
    // the question's stream: found at cycles 4 and 7
    feed(1); feed(0); feed(1); feed(1); feed(0); feed(1); feed(1);
    if (hits != 2) begin errors++; $display("1011011: %0d detections, expected 2", hits); end
    // the overlap trap: 10101011 ends with a detection
    feed(1); feed(0); feed(1); feed(0); feed(1); feed(0); feed(1); feed(1);
    if (!f1011) begin errors++; $display("10101011: the overlapping detection is missing"); end
    void'($urandom(40));
    for (int k = 0; k < 3000; k++) feed(1'($urandom_range(0, 1)));
    if (errors == 0) $display("PASS hits=%0d", hits);
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
