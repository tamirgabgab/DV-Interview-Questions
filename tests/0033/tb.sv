//@flags --assert --timing
// Question 0033: the page's fifo_depth and fifo_fill on the page numbers (24 / 25 for part
// a, 48 for part b, 24 with the read edges 2 ns after the write edges) and against each
// other on random bursts and exact integer periods: with aligned edges the simulation is
// the formula or one more for a reader that never skips, within one word either way for a
// reader that does. Then the page's fifo_depth_check bound to a model of the FIFO (a write
// pointer on wr_clk at 100 MHz writing a burst of 120 words, a read pointer on rd_clk at
// 80 MHz whose edges come a random phase after the write edges, the reader taking a word
// whenever one was there before its edge): the high-water mark equals fifo_fill at that
// phase, the assertion stays quiet with DEPTH = 25 and fires with DEPTH = 24 exactly when
// the mark is 25, and the aligned phase gives the largest mark.
`timescale 1ns / 1ps
//@page module fifo_depth_check

module tb;
  //@page function automatic int fifo_depth

  int errors = 0;

  // ---- the FIFO model and the two checkers -------------------------------------------
  logic wr_clk = 0, rd_clk = 0, rst_n = 0;
  int wptr, rptr, count;
  logic wr_en, full25, full24;
  assign count = wptr - rptr;
  assign wr_en = rst_n && wptr < 120;
  assign full25 = count >= 25;
  assign full24 = count >= 24;
  always_ff @(posedge wr_clk or negedge rst_n)
    if (!rst_n) wptr <= 0;
    else if (wr_en) wptr <= wptr + 1;
  always_ff @(posedge rd_clk or negedge rst_n)       // count is the value before the edge
    if (!rst_n) rptr <= 0;
    else if (count > 0) rptr <= rptr + 1;

  fifo_depth_check #(.DEPTH(25)) chk25 (.wr_clk, .rst_n, .wr_en, .full(full25), .wr_count(count));
  fifo_depth_check #(.DEPTH(24)) chk24 (.wr_clk, .rst_n, .wr_en, .full(full24), .wr_count(count));

  // one burst with the read edges p * 0.05 ns after the write edges
  task automatic burst(int p, output int mark, output int f25, output int f24);
    int o25 = chk25.overflows, o24 = chk24.overflows;
    rst_n = 0;
    #1 rst_n = 1;
    #1;
    fork
      repeat (170) begin wr_clk = 1; #5; wr_clk = 0; #5; end
      begin #(p * 0.05); repeat (140) begin rd_clk = 1; #6.25; rd_clk = 0; #6.25; end end
    join
    if (wptr != 120 || rptr != 120) begin errors++; $display("phase %0d: %0d written, %0d read", p, wptr, rptr); end
    mark = chk25.high_water;
    f25 = chk25.overflows - o25;
    f24 = chk24.overflows - o24;
  endtask

  initial begin
    int depth_a, fill_a, depth_b, fill_b, worst, aligned;
    depth_a = fifo_depth(120, 100, 80);
    fill_a = fifo_fill(120, 200, 250);
    depth_b = fifo_depth(120, 100, 80, 4);
    fill_b = fifo_fill(120, 200, 250, 4);
    $display("part a: formula %0d, simulation %0d; part b: formula %0d, simulation %0d", depth_a, fill_a, depth_b, fill_b);
    if (depth_a != 24 || fill_a != 25) begin errors++; $display("part a expected 24 / 25"); end
    if (depth_b != 48 || fill_b != 48) begin errors++; $display("part b expected 48 / 48"); end
    if (fifo_fill(120, 200, 250, 0, 40) != 24) begin errors++; $display("read edges 2 ns late: expected 24"); end
    if (fifo_depth(64, 100, 120) != 1) begin errors++; $display("a faster reader needs depth 1"); end
    // whole numbers that a real-valued formula rounds up: 40 (1 - 0.7) = 12, 100 (1 - 0.99) = 1
    if (fifo_depth(40, 100, 70) != 12 || fifo_depth(100, 100, 99) != 1 || fifo_depth(120, 100, 80, 8) != 36) begin
      errors++; $display("exact formula: %0d %0d %0d", fifo_depth(40, 100, 70), fifo_depth(100, 100, 99), fifo_depth(120, 100, 80, 8));
    end

    for (int k = 0; k < 300; k++) begin
      int burst_len, tw, tr, idle, d, s;
      burst_len = $urandom_range(1, 300);
      tw = $urandom_range(2, 40);                   // a write every tw steps, a read every tr:
      tr = $urandom_range(tw, 80);                  // the rates are tr and tw, the reader not faster
      idle = ($urandom_range(0, 2) == 0) ? 0 : $urandom_range(2, 8);
      d = fifo_depth(burst_len, tr, tw, idle);
      s = fifo_fill(burst_len, tw, tr, idle);
      if ((idle == 0 && (s < d || s > d + 1)) || (idle != 0 && (s < d - 1 || s > d + 1))) begin
        errors++;
        $display("burst %0d tw %0d tr %0d idle %0d: formula %0d, simulation %0d", burst_len, tw, tr, idle, d, s);
      end
    end

    // the checker on the FIFO model: the aligned phase, the edges of the 24 range, random phases
    worst = 0;
    for (int k = 0; k < 44; k++) begin
      int p, mark, f25, f24, want;
      p = (k == 0) ? 0 : (k == 1) ? 1 : (k == 2) ? 49 : (k == 3) ? 50 : $urandom_range(0, 249);
      burst(p, mark, f25, f24);
      want = fifo_fill(120, 200, 250, 0, p);
      if (k == 0) aligned = mark;
      if (mark > worst) worst = mark;
      if (mark != want || f25 != 0 || (f24 != 0) != (mark == 25)) begin
        errors++;
        $display("phase %0d: high water %0d (fifo_fill %0d), overflows %0d with 25 and %0d with 24", p, mark, want, f25, f24);
      end
    end
    $display("checker: aligned phase %0d words, worst %0d", aligned, worst);
    if (aligned != 25 || worst != 25) begin errors++; $display("the aligned phase should be the worst, 25"); end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
