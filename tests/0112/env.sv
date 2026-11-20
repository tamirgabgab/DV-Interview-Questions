// Question 0112: the part of the UVM SystemVerilog testbench the page describes in words,
// the counterpart of env.py. It does not run (Verilator has no UVM library): test_0112.py
// checks that it and the page's SystemVerilog blocks hold the classes and calls of the
// Python. The page's blocks are the bodies of the extern functions.
`include "uvm_macros.svh"
import uvm_pkg::*;

interface ch_if (input logic clk);
  logic       valid, par;
  logic [7:0] data, errs;
endinterface

class byte_item extends uvm_sequence_item;
  `uvm_object_utils(byte_item)
  bit [7:0] data;
  function new(string name = "item");
    super.new(name);
  endfunction
endclass

class bytes_seq extends uvm_sequence #(byte_item);
  `uvm_object_utils(bytes_seq)
  function new(string name = "bytes");
    super.new(name);
  endfunction
  task body();
    for (int n = 0; n < 8; n++) begin
      req = byte_item::type_id::create($sformatf("item%0d", n));
      start_item(req);
      req.data = 37 * n % 256;
      finish_item(req);
    end
  endtask
endclass

class parity_driver extends uvm_driver #(byte_item);
  `uvm_component_utils(parity_driver)
  virtual ch_if vif;
  int sent;
  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction
  function void build_phase(uvm_phase phase);
    if (!uvm_config_db#(virtual ch_if)::get(this, "", "BUS", vif))
      `uvm_fatal("NOBUS", "no BUS for this driver")
  endfunction
  virtual function bit parity(bit [7:0] data);
    return ^data;
  endfunction
  task run_phase(uvm_phase phase);
    forever begin
      seq_item_port.get_next_item(req);
      @(negedge vif.clk);
      vif.valid <= 1;
      vif.data  <= req.data;
      vif.par   <= parity(req.data);
      sent++;
      @(negedge vif.clk);
      vif.valid <= 0;
      seq_item_port.item_done();
    end
  endtask
endclass

class err_driver extends parity_driver;
  `uvm_component_utils(err_driver)
  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction
  extern function bit parity(bit [7:0] data);
endclass

class agent extends uvm_agent;
  `uvm_component_utils(agent)
  uvm_sequencer #(byte_item) seqr;
  parity_driver drv;
  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction
  extern function void build_phase(uvm_phase phase);
  function void connect_phase(uvm_phase phase);
    drv.seq_item_port.connect(seqr.seq_item_export);
  endfunction
endclass

class tb_env extends uvm_env;
  `uvm_component_utils(tb_env)
  agent agt0, agt1;
  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction
  function void build_phase(uvm_phase phase);
    agt0 = agent::type_id::create("agt0", this);
    agt1 = agent::type_id::create("agt1", this);
  endfunction
endclass

class parity_test extends uvm_test;
  `uvm_component_utils(parity_test)
  tb_env env;
  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction
  task run_phase(uvm_phase phase);
    agent agents[2] = '{env.agt0, env.agt1};
    bytes_seq seq;
    phase.raise_objection(this);
    foreach (agents[i]) begin
      seq = bytes_seq::type_id::create("bytes");
      seq.start(agents[i].seqr);
    end
    phase.drop_objection(this);
  endtask
  function void report_phase(uvm_phase phase);
    agent agents[2] = '{env.agt0, env.agt1};
    foreach (agents[i])
      `uvm_info("REPORT", $sformatf("%s: %s, %0d parity errors", agents[i].drv.get_full_name(),
                agents[i].drv.get_type_name(), agents[i].drv.vif.errs), UVM_NONE)
  endfunction
endclass

class err_test extends parity_test;
  `uvm_component_utils(err_test)
  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction
  extern function void build_phase(uvm_phase phase);
endclass

class chan1_test extends parity_test;
  `uvm_component_utils(chan1_test)
  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction
  extern function void build_phase(uvm_phase phase);
  function void end_of_elaboration_phase(uvm_phase phase);
    uvm_factory factory = uvm_factory::get();
    factory.print(0);
  endfunction
endclass

// the page: err_driver::parity, agent::build_phase, err_test::build_phase,
// chan1_test::build_phase

module top;
  logic clk = 0;
  always #5 clk = ~clk;
  ch_if ch0 (clk), ch1 (clk);
  parity_rx dut (.clk,
                 .valid0(ch0.valid), .data0(ch0.data), .par0(ch0.par), .errs0(ch0.errs),
                 .valid1(ch1.valid), .data1(ch1.data), .par1(ch1.par), .errs1(ch1.errs));
  initial begin
    uvm_config_db#(virtual ch_if)::set(null, "uvm_test_top.env.agt0.*", "BUS", ch0);
    uvm_config_db#(virtual ch_if)::set(null, "uvm_test_top.env.agt1.*", "BUS", ch1);
    run_test("err_test");
  end
endmodule
