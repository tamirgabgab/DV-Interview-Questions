//@flags --timing
// Question 0112: the page's DUT on its own, without cocotb: items with a right and a wrong
// parity bit on both channels, and items with valid low (never counted). The counters must
// count exactly the valid items whose bit was wrong, each channel on its own.
//@page module parity_rx (

module tb;
  logic       clk = 0, valid0 = 0, valid1 = 0, par0 = 0, par1 = 0;
  logic [7:0] data0 = 0, data1 = 0, errs0, errs1;
  int         want0 = 0, want1 = 0, bad = 0;

  parity_rx dut (.*);
  always #5 clk = ~clk;

  initial begin
    if (errs0 !== 0 || errs1 !== 0) bad++;               // the counters start at 0
    for (int n = 0; n < 40; n++) begin
      @(negedge clk);
      valid0 = n % 3 != 2;
      valid1 = n % 5 != 4;
      data0  = 8'(37 * n);
      data1  = 8'(91 * n + 5);
      par0   = ^data0 ^ (n % 4 == 3);                     // wrong every fourth item
      par1   = ^data1 ^ (n % 7 == 1);
      if (valid0 && n % 4 == 3) want0++;
      if (valid1 && n % 7 == 1) want1++;
    end
    @(negedge clk);
    if (errs0 != want0 || errs1 != want1) bad++;
    $display("errs0 = %0d (want %0d), errs1 = %0d (want %0d)", errs0, want0, errs1, want1);
    if (bad == 0 && want0 > 0 && want1 > 0) $display("PASS parity_rx counts the wrong parity bits");
    else $display("FAIL parity_rx");
    $finish;
  end
endmodule
