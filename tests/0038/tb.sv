//@flags --assert --timing
//@page module handshake_checker
// Question 0038: the page's checker on random traffic with injected violations, against a
// procedural reference model of the four rules on the same samples: the four counters of
// the checker must equal the reference counts, and each rule must have failed at least
// once (an assertion that never fails was not tested).
module tb;
  logic clk = 0, rst_n = 0, req = 0, ack = 0;
  int fails;
  int ref_hold = 0, ref_late = 0, ref_orphan = 0, ref_drop = 0;
  int errors = 0;

  handshake_checker #(.MAX_WAIT(3)) chk (.*);

  always #5 clk = ~clk;

  // The reference model: samples at every rising edge, the rules evaluated on the sampled
  // history exactly as the page's Python function does.
  logic hist_req[$], hist_ack[$];
  always @(posedge clk) if (rst_n) begin
    hist_req.push_back(req);
    hist_ack.push_back(ack);
  end

  function automatic void reference();
    int n = hist_req.size();
    for (int t = 0; t < n; t++) begin
      logic prev_req = t ? hist_req[t - 1] : 1'b0;
      logic prev_ack = t ? hist_ack[t - 1] : 1'b0;
      if (t && prev_req && !prev_ack && !hist_req[t]) ref_hold++;
      if (hist_req[t] && !prev_req && t + 3 < n) begin
        if (!hist_ack[t + 1] && !hist_ack[t + 2] && !hist_ack[t + 3]) ref_late++;
      end
      if (hist_ack[t] && !hist_req[t]) ref_orphan++;
      if (t && prev_ack && hist_req[t]) ref_drop++;
    end
  endfunction

  // drive on the falling edge so every value is stable at the sampling edge
  task automatic idle(int cycles);
    repeat (cycles) @(negedge clk);
  endtask

  task automatic transaction(int wait_cycles, bit drop_early, bit hold_after);
    @(negedge clk) req = 1;
    if (drop_early) begin
      repeat (wait_cycles) @(negedge clk);
      req = 0;                                  // gives up before the ack
      return;
    end
    repeat (wait_cycles) @(negedge clk);
    ack = 1;
    @(negedge clk) ack = 0;
    if (!hold_after) req = 0;
    else begin repeat (2) @(negedge clk); req = 0; end
  endtask

  initial begin
    int kind;                                    // assigned per iteration: an initialiser here would run once
    idle(3);
    @(negedge clk) rst_n = 1;
    idle(2);
    for (int k = 0; k < 400; k++) begin
      kind = $urandom_range(0, 9);
      case (kind)
        0: transaction($urandom_range(4, 6), 0, 0);        // late ack (rule 2)
        1: transaction($urandom_range(1, 2), 1, 0);        // req dropped before ack (rules 1, 2)
        2: begin @(negedge clk) ack = 1; @(negedge clk) ack = 0; end   // orphan ack (rule 3)
        3: transaction($urandom_range(1, 3), 0, 1);        // req held after ack (rule 4)
        default: transaction($urandom_range(1, 3), 0, 0);  // a good one
      endcase
      idle($urandom_range(0, 2));
    end
    idle(8);                                     // let every window close
    @(negedge clk);
    reference();
    $display("checker: hold %0d late %0d orphan %0d drop %0d (fails %0d)", chk.fail_hold, chk.fail_late, chk.fail_orphan, chk.fail_drop, fails);
    $display("reference: hold %0d late %0d orphan %0d drop %0d", ref_hold, ref_late, ref_orphan, ref_drop);
    if (chk.fail_hold != ref_hold || chk.fail_late != ref_late || chk.fail_orphan != ref_orphan || chk.fail_drop != ref_drop) begin
      errors++; $display("checker and reference disagree");
    end
    if (fails != chk.fail_hold + chk.fail_late + chk.fail_orphan + chk.fail_drop) begin errors++; $display("fails is not the sum"); end
    if (ref_hold == 0 || ref_late == 0 || ref_orphan == 0 || ref_drop == 0) begin errors++; $display("a rule was never violated: the test is too weak"); end
    if (errors == 0) $display("PASS fails=%0d", fails);
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
