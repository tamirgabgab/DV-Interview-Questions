//@flags --timing
// Question 0115: written by tests/0115/variants.py --write from the page's blocks and
// tests/0115/env.sv; do not edit. The page's bench as published (race_tb) reports its six
// mismatches at cycles 2, 3, 5, 7, 8 and 10, the page's fix (race_tb_fix) none; race_cfg runs
// every choice of the box that Verilator runs, and tb compares the mismatch cycles of every
// bench, and the waveforms of the two page benches, with tools/figures/q0115.py. A blocking
// write from a program block is still taken by the DUT at the same edge (Verilator does not
// run program blocks in the Reactive region).

module add1 (
  input  logic       clk,
  input  logic       in_valid,
  input  logic [7:0] in_data,
  output logic       out_valid,
  output logic [7:0] out_data
);
  always_ff @(posedge clk) begin
    out_valid <= in_valid;
    out_data  <= in_data + 8'd1;
  end
endmodule

module race_tb;
  localparam int N = 10;
  logic       clk = 0, in_valid = 0, out_valid;
  logic [7:0] in_data = 0, out_data;
  int         cycle = 0, mismatches = 0;
  string      cycles = "";                 // the cycle of every mismatch, for tb

  add1 dut (.*);
  always #5 clk = ~clk;
  always @(mismatches) if (mismatches) cycles = cycles == "" ? $sformatf("%0d", cycle) : $sformatf("%s %0d", cycles, cycle);

  function automatic string item(logic valid, logic [7:0] data);
    return valid ? $sformatf("%0d", data) : "none";
  endfunction

  bit         V[N] = '{1, 1, 1, 0, 0, 1, 1, 1, 0, 0};   // in_valid of every cycle
  logic [7:0] D[N] = '{5, 9, 9, 9, 9, 2, 6, 6, 6, 6};   // in_data, held while in_valid is low

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
      monitor();
      drive();
    join_any
    repeat (3) @(posedge clk);
    $display("%m: %0d mismatches", mismatches);
  end
endmodule

module race_tb_fix;
  localparam int N = 10;
  logic       clk = 0, in_valid = 0, out_valid;
  logic [7:0] in_data = 0, out_data;
  int         cycle = 0, mismatches = 0;
  string      cycles = "";                 // the cycle of every mismatch, for tb

  add1 dut (.*);
  always #5 clk = ~clk;
  always @(mismatches) if (mismatches) cycles = cycles == "" ? $sformatf("%0d", cycle) : $sformatf("%s %0d", cycles, cycle);

  function automatic string item(logic valid, logic [7:0] data);
    return valid ? $sformatf("%0d", data) : "none";
  endfunction

  bit         V[N] = '{1, 1, 1, 0, 0, 1, 1, 1, 0, 0};   // in_valid of every cycle
  logic [7:0] D[N] = '{5, 9, 9, 9, 9, 2, 6, 6, 6, 6};   // in_data, held while in_valid is low


  clocking drv_cb @(posedge clk);            // the driver's side (1)
    output #0 in_valid, in_data;
  endclocking

  clocking mon_cb @(posedge clk);            // the monitor's side (2)
    input #1step in_valid, in_data, out_valid, out_data;
  endclocking

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
      exp_valid = mon_cb.in_valid;                  // what the DUT takes at this edge
      exp_data  = mon_cb.in_data + 8'd1;
    end
  endtask

  initial begin
    fork
      monitor();
      drive();
    join_any
    repeat (3) @(posedge clk);
    $display("%m: %0d mismatches", mismatches);
  end
endmodule

module race_cfg #(int DRV = 0, int MON = 0, bit DRV_FIRST = 0);
  localparam int N = 10;
  logic       clk = 0, in_valid = 0, out_valid;
  logic [7:0] in_data = 0, out_data;
  int         cycle = 0, mismatches = 0;
  string      cycles = "";                 // the cycle of every mismatch, for tb

  add1 dut (.*);
  always #5 clk = ~clk;
  always @(mismatches) if (mismatches) cycles = cycles == "" ? $sformatf("%0d", cycle) : $sformatf("%s %0d", cycles, cycle);

  function automatic string item(logic valid, logic [7:0] data);
    return valid ? $sformatf("%0d", data) : "none";
  endfunction

  bit         V[N] = '{1, 1, 1, 0, 0, 1, 1, 1, 0, 0};   // in_valid of every cycle
  logic [7:0] D[N] = '{5, 9, 9, 9, 9, 2, 6, 6, 6, 6};   // in_data, held while in_valid is low


  clocking drv_cb @(posedge clk);            // the driver's side (1)
    output #0 in_valid, in_data;
  endclocking

  clocking mon_cb @(posedge clk);            // the monitor's side (2)
    input #1step in_valid, in_data, out_valid, out_data;
  endclocking

  clocking mon_cb0 @(posedge clk);            // the monitor's side
    input #0 in_valid, in_data, out_valid, out_data;
  endclocking

  task automatic drive_blk();
    foreach (V[i]) begin
      @(posedge clk);
      in_valid = V[i];
      in_data  = D[i];
    end
  endtask

  task automatic drive_nba();
    foreach (V[i]) begin
      @(posedge clk);
      in_valid <= V[i];
      in_data  <= D[i];
    end
  endtask

  task automatic drive_cb();
    foreach (V[i]) begin
      @(drv_cb);
      drv_cb.in_valid <= V[i];
      drv_cb.in_data  <= D[i];
    end
  endtask

  task automatic drive_neg();
    foreach (V[i]) begin
      @(negedge clk);
      in_valid = V[i];
      in_data  = D[i];
    end
  endtask

  task automatic monitor_edge();                  // the model: out is in + 1, one cycle later
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

  task automatic monitor_s1();                  // the model: out is in + 1, one cycle later
    logic       exp_valid = 0;
    logic [7:0] exp_data  = 0;
    forever begin
      @(mon_cb);
      cycle++;
      if (mon_cb.out_valid != exp_valid || (exp_valid && mon_cb.out_data != exp_data)) begin
        mismatches++;
        $display("cycle %0d: expected %s, got %s", cycle, item(exp_valid, exp_data), item(mon_cb.out_valid, mon_cb.out_data));
      end
      exp_valid = mon_cb.in_valid;                  // what the DUT takes at this edge
      exp_data  = mon_cb.in_data + 8'd1;
    end
  endtask

  task automatic monitor_s0();                  // the model: out is in + 1, one cycle later
    logic       exp_valid = 0;
    logic [7:0] exp_data  = 0;
    forever begin
      @(mon_cb0);
      cycle++;
      if (mon_cb0.out_valid != exp_valid || (exp_valid && mon_cb0.out_data != exp_data)) begin
        mismatches++;
        $display("cycle %0d: expected %s, got %s", cycle, item(exp_valid, exp_data), item(mon_cb0.out_valid, mon_cb0.out_data));
      end
      exp_valid = mon_cb0.in_valid;                  // what the DUT takes at this edge
      exp_data  = mon_cb0.in_data + 8'd1;
    end
  endtask

  task automatic monitor_neg();                  // the model: out is in + 1, one cycle later
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

  task automatic drive();
    case (DRV)
      0: drive_blk();
      1: drive_nba();
      2: drive_cb();
      3: drive_neg();
    endcase
  endtask

  task automatic monitor();
    case (MON)
      0: monitor_edge();
      1: monitor_s1();
      2: monitor_s0();
      3: monitor_neg();
    endcase
  endtask

  initial begin
    if (DRV_FIRST)
      fork
        drive();
        monitor();
      join_any
    else
      fork
        monitor();
        drive();
      join_any
    repeat (3) @(posedge clk);
    $display("%m: %0d mismatches", mismatches);
  end
endmodule

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
  race_tb     bug ();
  race_tb_fix fix ();
  prog_check  prog ();

  // the mismatch cycles of every choice (q0115.mismatch_cycles of q0115.view_of)
  string WANT[32] = '{
    "2 3 5 7 8 10",   // 0: blk edge mdx
    "",               // 1: blk edge dmx
    "2 3 5 7 8 10",   // 2: blk s1 mdx
    "2 3 5 7 8 10",   // 3: blk s1 dmx
    "1 2 4 6 7 9",    // 4: blk s0 mdx
    "1 2 4 6 7 9",    // 5: blk s0 dmx
    "1 2 4 6 7 9",    // 6: blk neg mdx
    "1 2 4 6 7 9",    // 7: blk neg dmx
    "",               // 8: nba edge mdx
    "",               // 9: nba edge dmx
    "",               // 10: nba s1 mdx
    "",               // 11: nba s1 dmx
    "",               // 12: nba s0 mdx
    "",               // 13: nba s0 dmx
    "",               // 14: nba neg mdx
    "",               // 15: nba neg dmx
    "",               // 16: cb edge mdx
    "",               // 17: cb edge dmx
    "",               // 18: cb s1 mdx
    "",               // 19: cb s1 dmx
    "2 3 5 7 8 10",   // 20: cb s0 mdx
    "2 3 5 7 8 10",   // 21: cb s0 dmx
    "",               // 22: cb neg mdx
    "",               // 23: cb neg dmx
    "",               // 24: neg edge mdx
    "",               // 25: neg edge dmx
    "",               // 26: neg s1 mdx
    "",               // 27: neg s1 dmx
    "2 3 5 7 8 10",   // 28: neg s0 mdx
    "2 3 5 7 8 10",   // 29: neg s0 dmx
    "2 3 5 7 8 10",   // 30: neg neg mdx
    ""                // 31: neg neg dmx
  };
  int bad = 0;
  for (genvar g = 0; g < 32; g++) begin : m
    race_cfg #(.DRV(g / 8), .MON(g / 2 % 4), .DRV_FIRST(g % 2)) b ();
    initial begin
      #200;
      if (b.cycles != WANT[g]) begin
        bad++;
        $display("race_cfg %0d: mismatch cycles \"%s\", want \"%s\"", g, b.cycles, WANT[g]);
      end
    end
  end

  // the waveform of the dump: valid/data of the input and the output after every edge, read
  // half a cycle later (q0115.wave_string)
  string wave_bug = "", wave_fix = "";
  string WANT_WAVE_BUG = "1/5:1/6 1/9:1/10 1/9:1/10 0/9:0/10 0/9:0/10 1/2:1/3 1/6:1/7 1/6:1/7 0/6:0/7 0/6:0/7 0/6:0/7 0/6:0/7";
  string WANT_WAVE_FIX = "1/5:0/1 1/9:1/6 1/9:1/10 0/9:1/10 0/9:0/10 1/2:0/10 1/6:1/3 1/6:1/7 0/6:1/7 0/6:0/7 0/6:0/7 0/6:0/7";
  function automatic string snap(logic iv, logic [7:0] id, logic ov, logic [7:0] od);
    return $sformatf("%0d/%0d:%0d/%0d", iv, id, ov, od);
  endfunction
  function automatic string join1(string s, string c);
    return s == "" ? c : {s, " ", c};
  endfunction
  always @(negedge bug.clk) if ($time <= 120) wave_bug = join1(wave_bug, snap(bug.in_valid, bug.in_data, bug.out_valid, bug.out_data));
  always @(negedge fix.clk) if ($time <= 120) wave_fix = join1(wave_fix, snap(fix.in_valid, fix.in_data, fix.out_valid, fix.out_data));

  // the program block: what the DUT took at the first edge (10: the value written at that edge)
  int prog_q = -1;
  initial begin
    @(negedge prog.clk);
    prog_q = prog.q;
  end

  initial begin
    #250;
    if (bug.cycles != "2 3 5 7 8 10") begin bad++; $display("race_tb: mismatch cycles %s", bug.cycles); end
    if (fix.cycles != "") begin bad++; $display("race_tb_fix: mismatch cycles %s", fix.cycles); end
    if (wave_bug != WANT_WAVE_BUG) begin bad++; $display("wave bug: %s", wave_bug); end
    if (wave_fix != WANT_WAVE_FIX) begin bad++; $display("wave fix: %s", wave_fix); end
    if (prog_q != 10) begin bad++; $display("program block: the DUT took %0d at the first edge", prog_q - 1); end
    if (bad == 0) $display("PASS: 0115 the page's bench, its fix and 32 choices of the box (%0d mismatches as found)", bug.mismatches);
    else $display("FAIL: 0115 %0d differences", bad);
    $finish;
  end
endmodule
