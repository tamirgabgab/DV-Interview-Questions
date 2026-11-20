//@flags --timing
// Question 0115: the page's benches on Verilator 5.053, all at once, each its own instance
// with its own clock. The bench as found reports its six mismatches at cycles 2, 3, 5, 7, 8
// and 10; the clocking-block fix and the two driver fixes report none; the variants the page
// talks about (the fork swapped, a clocking block for the monitor only, the monitor on the
// falling edge) do what the page says; and a blocking write from a program block is still
// taken by the DUT at the same edge (Verilator does not run program blocks in the Reactive
// region). The want strings are checked against the model of tools/figures/q0115.py by
// tests/0115/test_0115.py, which also checks that the copies below are the page's code with
// only the named change (tests/0115/variants.py).
//@page module add1 (
//@page module race_tb;
//@page module race_tb_cb;

// ---- the copies: python tests/0115/variants.py --write ----
module race_tb_swap;
  localparam int N = 10;
  bit         V[N] = '{1, 1, 1, 0, 0, 1, 1, 1, 0, 0};   // in_valid of every cycle
  logic [7:0] D[N] = '{5, 9, 9, 9, 9, 2, 6, 6, 6, 6};   // in_data, held while in_valid is low
  logic       clk = 0, in_valid = 0, out_valid;
  logic [7:0] in_data = 0, out_data;
  int         cycle = 0, mismatches = 0;

  add1 dut (.*);
  always #5 clk = ~clk;

  function automatic string item(logic valid, logic [7:0] data);
    return valid ? $sformatf("%0d", data) : "none";
  endfunction

  task automatic drive();
    foreach (V[i]) begin
      @(posedge clk);
      in_valid = V[i];
      in_data  = D[i];
    end
  endtask

  task automatic monitor();                  // the model: out is in + 1, one cycle later
    logic       exp_valid = 0;
    logic [7:0] exp_data  = 0;
    forever begin
      @(posedge clk);
      cycle++;
      if (out_valid != exp_valid || (exp_valid && out_data != exp_data)) begin
        mismatches++;
        $display("cycle %0d: expected %s, got %s", cycle, item(exp_valid, exp_data), item(out_valid, out_data));
      end
      exp_valid = in_valid;                  // what the DUT takes at this edge
      exp_data  = in_data + 8'd1;
    end
  endtask

  initial begin
    fork
      drive();
      monitor();
    join_any
    repeat (3) @(posedge clk);
    $display("%0d mismatches", mismatches);
    $finish;
  end
endmodule

module race_tb_nba;
  localparam int N = 10;
  bit         V[N] = '{1, 1, 1, 0, 0, 1, 1, 1, 0, 0};   // in_valid of every cycle
  logic [7:0] D[N] = '{5, 9, 9, 9, 9, 2, 6, 6, 6, 6};   // in_data, held while in_valid is low
  logic       clk = 0, in_valid = 0, out_valid;
  logic [7:0] in_data = 0, out_data;
  int         cycle = 0, mismatches = 0;

  add1 dut (.*);
  always #5 clk = ~clk;

  function automatic string item(logic valid, logic [7:0] data);
    return valid ? $sformatf("%0d", data) : "none";
  endfunction

  task automatic drive();
    foreach (V[i]) begin
      @(posedge clk);
      in_valid <= V[i];                        // written in the NBA region
      in_data  <= D[i];
    end
  endtask

  task automatic monitor();                  // the model: out is in + 1, one cycle later
    logic       exp_valid = 0;
    logic [7:0] exp_data  = 0;
    forever begin
      @(posedge clk);
      cycle++;
      if (out_valid != exp_valid || (exp_valid && out_data != exp_data)) begin
        mismatches++;
        $display("cycle %0d: expected %s, got %s", cycle, item(exp_valid, exp_data), item(out_valid, out_data));
      end
      exp_valid = in_valid;                  // what the DUT takes at this edge
      exp_data  = in_data + 8'd1;
    end
  endtask

  initial begin
    fork
      monitor();
      drive();
    join_any
    repeat (3) @(posedge clk);
    $display("%0d mismatches", mismatches);
    $finish;
  end
endmodule

module race_tb_neg;
  localparam int N = 10;
  bit         V[N] = '{1, 1, 1, 0, 0, 1, 1, 1, 0, 0};   // in_valid of every cycle
  logic [7:0] D[N] = '{5, 9, 9, 9, 9, 2, 6, 6, 6, 6};   // in_data, held while in_valid is low
  logic       clk = 0, in_valid = 0, out_valid;
  logic [7:0] in_data = 0, out_data;
  int         cycle = 0, mismatches = 0;

  add1 dut (.*);
  always #5 clk = ~clk;

  function automatic string item(logic valid, logic [7:0] data);
    return valid ? $sformatf("%0d", data) : "none";
  endfunction

  task automatic drive();
    foreach (V[i]) begin
      @(negedge clk);                          // half a cycle away from the sampling edge
      in_valid = V[i];
      in_data  = D[i];
    end
  endtask

  task automatic monitor();                  // the model: out is in + 1, one cycle later
    logic       exp_valid = 0;
    logic [7:0] exp_data  = 0;
    forever begin
      @(posedge clk);
      cycle++;
      if (out_valid != exp_valid || (exp_valid && out_data != exp_data)) begin
        mismatches++;
        $display("cycle %0d: expected %s, got %s", cycle, item(exp_valid, exp_data), item(out_valid, out_data));
      end
      exp_valid = in_valid;                  // what the DUT takes at this edge
      exp_data  = in_data + 8'd1;
    end
  endtask

  initial begin
    fork
      monitor();
      drive();
    join_any
    repeat (3) @(posedge clk);
    $display("%0d mismatches", mismatches);
    $finish;
  end
endmodule

module race_tb_negmon;
  localparam int N = 10;
  bit         V[N] = '{1, 1, 1, 0, 0, 1, 1, 1, 0, 0};   // in_valid of every cycle
  logic [7:0] D[N] = '{5, 9, 9, 9, 9, 2, 6, 6, 6, 6};   // in_data, held while in_valid is low
  logic       clk = 0, in_valid = 0, out_valid;
  logic [7:0] in_data = 0, out_data;
  int         cycle = 0, mismatches = 0;

  add1 dut (.*);
  always #5 clk = ~clk;

  function automatic string item(logic valid, logic [7:0] data);
    return valid ? $sformatf("%0d", data) : "none";
  endfunction

  task automatic drive();
    foreach (V[i]) begin
      @(posedge clk);
      in_valid = V[i];
      in_data  = D[i];
    end
  endtask

  task automatic monitor();                  // the model: out is in + 1, one cycle later
    logic       exp_valid = 0;
    logic [7:0] exp_data  = 0;
    forever begin
      @(negedge clk);
      cycle++;
      if (out_valid != exp_valid || (exp_valid && out_data != exp_data)) begin
        mismatches++;
        $display("cycle %0d: expected %s, got %s", cycle, item(exp_valid, exp_data), item(out_valid, out_data));
      end
      exp_valid = in_valid;                  // what the DUT takes at this edge
      exp_data  = in_data + 8'd1;
    end
  endtask

  initial begin
    fork
      monitor();
      drive();
    join_any
    repeat (3) @(posedge clk);
    $display("%0d mismatches", mismatches);
    $finish;
  end
endmodule

module race_tb_cb_swap;
  localparam int N = 10;
  bit         V[N] = '{1, 1, 1, 0, 0, 1, 1, 1, 0, 0};   // in_valid of every cycle
  logic [7:0] D[N] = '{5, 9, 9, 9, 9, 2, 6, 6, 6, 6};   // in_data, held while in_valid is low
  logic       clk = 0, in_valid = 0, out_valid;
  logic [7:0] in_data = 0, out_data;
  int         cycle = 0, mismatches = 0;

  add1 dut (.*);
  always #5 clk = ~clk;

  clocking drv_cb @(posedge clk);            // the driver's side (1)
    output #0 in_valid, in_data;
  endclocking

  clocking mon_cb @(posedge clk);            // the monitor's side (2)
    input #1step in_valid, in_data, out_valid, out_data;
  endclocking

  function automatic string item(logic valid, logic [7:0] data);
    return valid ? $sformatf("%0d", data) : "none";
  endfunction

  task automatic drive();
    foreach (V[i]) begin
      @(drv_cb);
      drv_cb.in_valid <= V[i];
      drv_cb.in_data  <= D[i];
    end
  endtask

  task automatic monitor();                  // the model: out is in + 1, one cycle later
    logic       exp_valid = 0;
    logic [7:0] exp_data  = 0;
    forever begin
      @(mon_cb);
      cycle++;
      if (mon_cb.out_valid != exp_valid || (exp_valid && mon_cb.out_data != exp_data)) begin
        mismatches++;
        $display("cycle %0d: expected %s, got %s", cycle, item(exp_valid, exp_data), item(mon_cb.out_valid, mon_cb.out_data));
      end
      exp_valid = mon_cb.in_valid;           // the value from before the edge
      exp_data  = mon_cb.in_data + 8'd1;
    end
  endtask

  initial begin
    fork
      drive();
      monitor();
    join_any
    repeat (3) @(posedge clk);
    $display("%0d mismatches", mismatches);
    $finish;
  end
endmodule

module race_tb_cb_mon;
  localparam int N = 10;
  bit         V[N] = '{1, 1, 1, 0, 0, 1, 1, 1, 0, 0};   // in_valid of every cycle
  logic [7:0] D[N] = '{5, 9, 9, 9, 9, 2, 6, 6, 6, 6};   // in_data, held while in_valid is low
  logic       clk = 0, in_valid = 0, out_valid;
  logic [7:0] in_data = 0, out_data;
  int         cycle = 0, mismatches = 0;

  add1 dut (.*);
  always #5 clk = ~clk;

  clocking drv_cb @(posedge clk);            // the driver's side (1)
    output #0 in_valid, in_data;
  endclocking

  clocking mon_cb @(posedge clk);            // the monitor's side (2)
    input #1step in_valid, in_data, out_valid, out_data;
  endclocking

  function automatic string item(logic valid, logic [7:0] data);
    return valid ? $sformatf("%0d", data) : "none";
  endfunction

  task automatic drive();
    foreach (V[i]) begin
      @(posedge clk);
      in_valid = V[i];
      in_data  = D[i];
    end
  endtask

  task automatic monitor();                  // the model: out is in + 1, one cycle later
    logic       exp_valid = 0;
    logic [7:0] exp_data  = 0;
    forever begin
      @(mon_cb);
      cycle++;
      if (mon_cb.out_valid != exp_valid || (exp_valid && mon_cb.out_data != exp_data)) begin
        mismatches++;
        $display("cycle %0d: expected %s, got %s", cycle, item(exp_valid, exp_data), item(mon_cb.out_valid, mon_cb.out_data));
      end
      exp_valid = mon_cb.in_valid;           // the value from before the edge
      exp_data  = mon_cb.in_data + 8'd1;
    end
  endtask

  initial begin
    fork
      monitor();
      drive();
    join_any
    repeat (3) @(posedge clk);
    $display("%0d mismatches", mismatches);
    $finish;
  end
endmodule
// ---- end of the copies ----

// a driver in a program block, writing with = at the edge
program automatic prog_drive (input logic clk, output logic [7:0] d);
  initial begin
    d = 8'd5;
    @(posedge clk);
    d = 8'd9;
  end
endprogram

module prog_check;
  logic       clk = 0, v;
  logic [7:0] d, q;
  add1 dut (.clk, .in_valid(1'b1), .in_data(d), .out_valid(v), .out_data(q));
  always #5 clk = ~clk;
  prog_drive drv (.clk, .d);
endmodule

module tb;
  race_tb         bug ();
  race_tb_swap    swap ();
  race_tb_nba     nba ();
  race_tb_neg     neg ();
  race_tb_negmon  negmon ();
  race_tb_cb      cb ();
  race_tb_cb_swap cb_swap ();
  race_tb_cb_mon  cb_mon ();
  prog_check      prog ();

  // the cycles of every mismatch, per bench (q0115.mismatch_cycles)
  string got[8] = '{"", "", "", "", "", "", "", ""};
  string WANT[8] = '{
    "2 3 5 7 8 10",       // bug: the page's bench
    "",                   // swap: drive() first in the fork
    "",                   // nba: the driver with <=
    "",                   // neg: the driver on the falling edge
    "1 2 4 6 7 9",        // negmon: the monitor on the falling edge, the driver as found
    "",                   // cb: the page's fix
    "",                   // cb_swap: the fix, drive() first
    "2 3 5 7 8 10"        // cb_mon: a clocking block for the monitor only
  };
  function automatic void add(int b, int c);
    got[b] = got[b] == "" ? $sformatf("%0d", c) : $sformatf("%s %0d", got[b], c);
  endfunction
  always @(bug.mismatches)     if (bug.mismatches)     add(0, bug.cycle);
  always @(swap.mismatches)    if (swap.mismatches)    add(1, swap.cycle);
  always @(nba.mismatches)     if (nba.mismatches)     add(2, nba.cycle);
  always @(neg.mismatches)     if (neg.mismatches)     add(3, neg.cycle);
  always @(negmon.mismatches)  if (negmon.mismatches)  add(4, negmon.cycle);
  always @(cb.mismatches)      if (cb.mismatches)      add(5, cb.cycle);
  always @(cb_swap.mismatches) if (cb_swap.mismatches) add(6, cb_swap.cycle);
  always @(cb_mon.mismatches)  if (cb_mon.mismatches)  add(7, cb_mon.cycle);

  // the waveform of the dump: valid/data of the input and the output after every edge, read
  // half a cycle later (q0115.wave_rows)
  string wave_bug = "", wave_cb = "", wave_nba = "";
  string WANT_WAVE_BUG = "1/5:1/6 1/9:1/10 1/9:1/10 0/9:0/10 0/9:0/10 1/2:1/3 1/6:1/7 1/6:1/7 0/6:0/7 0/6:0/7 0/6:0/7 0/6:0/7";
  string WANT_WAVE_FIX = "1/5:0/1 1/9:1/6 1/9:1/10 0/9:1/10 0/9:0/10 1/2:0/10 1/6:1/3 1/6:1/7 0/6:1/7 0/6:0/7 0/6:0/7 0/6:0/7";
  function automatic string snap(logic iv, logic [7:0] id, logic ov, logic [7:0] od);
    return $sformatf("%0d/%0d:%0d/%0d", iv, id, ov, od);
  endfunction
  function automatic string join1(string s, string c);
    return s == "" ? c : {s, " ", c};
  endfunction
  always @(negedge bug.clk) wave_bug = join1(wave_bug, snap(bug.in_valid, bug.in_data, bug.out_valid, bug.out_data));
  always @(negedge cb.clk)  wave_cb  = join1(wave_cb, snap(cb.in_valid, cb.in_data, cb.out_valid, cb.out_data));
  always @(negedge nba.clk) wave_nba = join1(wave_nba, snap(nba.in_valid, nba.in_data, nba.out_valid, nba.out_data));

  // the program block: what the DUT took at the first edge (10: the value written at that edge)
  int prog_q = -1;
  initial begin
    @(negedge prog.clk);
    prog_q = prog.q;
  end

  final begin
    int errors = 0;
    foreach (WANT[i])
      if (got[i] != WANT[i]) begin
        errors++;
        $display("bench %0d: mismatch cycles \"%s\", want \"%s\"", i, got[i], WANT[i]);
      end
    if (wave_bug != WANT_WAVE_BUG) begin errors++; $display("wave bug: %s", wave_bug); end
    if (wave_cb != WANT_WAVE_FIX)  begin errors++; $display("wave cb: %s", wave_cb); end
    if (wave_nba != WANT_WAVE_FIX) begin errors++; $display("wave nba: %s", wave_nba); end
    if (prog_q != 10) begin errors++; $display("program block: the DUT took %0d at the first edge", prog_q - 1); end
    if (errors == 0) $display("PASS: 0115 the race, its three fixes and the variants (%0d mismatches as found)", bug.mismatches);
    else $display("FAIL: 0115 %0d differences", errors);
  end
endmodule
