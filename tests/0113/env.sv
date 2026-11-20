// Question 0113: the UVM environment of the page's SystemVerilog tabs, the counterpart of
// env.py. Not run (Verilator has no UVM library); test_0113.py checks it against env.py.

interface pipe_if (input logic clk);
  logic       rst_n, in_valid, out_valid;
  logic [7:0] in_data, out_data;
endinterface

class item extends uvm_sequence_item;
  `uvm_object_utils(item)
  bit [7:0] data;
  function new(string name = "item"); super.new(name); endfunction
endclass

class item_seq extends uvm_sequence #(item);
  `uvm_object_utils(item_seq)
  function new(string name = "item_seq"); super.new(name); endfunction
  task body();
    for (int k = 0; k < 8; k++) begin
      item it = item::type_id::create("item");
      start_item(it);
      it.data = 8'h10 + k;
      finish_item(it);
    end
  endtask
endclass

class driver extends uvm_driver #(item);
  `uvm_component_utils(driver)
  virtual pipe_if vif;
  function new(string name, uvm_component parent); super.new(name, parent); endfunction
  task run_phase(uvm_phase phase);
    vif.rst_n <= 0;
    vif.in_valid <= 0;
    repeat (2) @(posedge vif.clk);
    vif.rst_n <= 1;
    forever begin
      seq_item_port.get_next_item(req);
      vif.in_valid <= 1;
      vif.in_data <= req.data;
      @(posedge vif.clk);
      vif.in_valid <= 0;
      seq_item_port.item_done();
    end
  endtask
endclass

class in_monitor extends uvm_monitor;
  `uvm_component_utils(in_monitor)
  virtual pipe_if vif;
  uvm_analysis_port #(bit [7:0]) ap;
  function new(string name, uvm_component parent); super.new(name, parent); ap = new("ap", this); endfunction
  task run_phase(uvm_phase phase);
    forever begin
      @(negedge vif.clk);
      if (vif.in_valid) ap.write(vif.in_data);
    end
  endtask
endclass

class out_monitor extends uvm_monitor;
  `uvm_component_utils(out_monitor)
  virtual pipe_if vif;
  uvm_analysis_port #(bit [7:0]) ap;
  function new(string name, uvm_component parent); super.new(name, parent); ap = new("ap", this); endfunction
  task run_phase(uvm_phase phase);
    forever begin
      @(negedge vif.clk);
      if (vif.out_valid) ap.write(vif.out_data);
    end
  endtask
endclass

class scoreboard extends uvm_component;
  `uvm_component_utils(scoreboard)
  uvm_tlm_analysis_fifo #(bit [7:0]) sent, seen;
  function new(string name, uvm_component parent);
    super.new(name, parent);
    sent = new("sent", this);
    seen = new("seen", this);
  endfunction
  function void check_phase(uvm_phase phase);
    bit [7:0] x, out;
    int n = 0, bad = 0, missing;
    while (seen.try_get(out)) begin
      void'(sent.try_get(x));
      n++;
      if (out != 8'(x + 1)) bad++;
    end
    missing = sent.used();
    `uvm_info("SB", $sformatf("%0t: %0d compared, %0d mismatches, %0d missing", $time, n, bad, missing), UVM_LOW)
    if (bad || missing) `uvm_error("SB", "TEST FAILED")
    else                `uvm_info("SB", "TEST PASSED", UVM_LOW)
  endfunction
endclass

class pipe_env extends uvm_env;
  `uvm_component_utils(pipe_env)
  virtual pipe_if         vif;
  uvm_sequencer #(item)   seqr;
  driver                  drv;
  in_monitor              mon_in;
  out_monitor             mon_out;
  scoreboard              sb;
  function new(string name, uvm_component parent); super.new(name, parent); endfunction
  function void build_phase(uvm_phase phase);
    if (!uvm_config_db #(virtual pipe_if)::get(this, "", "vif", vif)) `uvm_fatal("ENV", "no vif")
    seqr    = uvm_sequencer #(item)::type_id::create("seqr", this);
    drv     = driver::type_id::create("drv", this);
    mon_in  = in_monitor::type_id::create("mon_in", this);
    mon_out = out_monitor::type_id::create("mon_out", this);
    sb      = scoreboard::type_id::create("sb", this);
  endfunction
  function void connect_phase(uvm_phase phase);
    drv.vif = vif;
    mon_in.vif = vif;
    mon_out.vif = vif;
    drv.seq_item_port.connect(seqr.seq_item_export);
    mon_in.ap.connect(sb.sent.analysis_export);
    mon_out.ap.connect(sb.seen.analysis_export);
  endfunction
endclass

module top;
  logic clk = 0;
  always #5 clk = ~clk;
  pipe_if pif (clk);
  pipe dut (.clk, .rst_n(pif.rst_n), .in_valid(pif.in_valid), .in_data(pif.in_data),
            .out_valid(pif.out_valid), .out_data(pif.out_data));
  initial begin
    uvm_config_db #(virtual pipe_if)::set(null, "uvm_test_top.env", "vif", pif);
    run_test();                     // +UVM_TESTNAME=smoke_test
  end
endmodule
