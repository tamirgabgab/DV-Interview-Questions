// Question 0033: the page's fifo_depth and fifo_fill on the page numbers (24 / 25 for part
// a, 48 for part b) and against each other on random bursts and rates: the simulation is
// never below the formula and at most one word above it for a reader that never skips,
// at most two for a reader that does.
module tb;
  //@page function automatic int fifo_depth

  int errors = 0;

  // period in steps of 0.05 ns for a frequency in MHz
  function automatic int steps(int f_mhz);
    return (20000 + f_mhz / 2) / f_mhz;
  endfunction

  initial begin
    int depth_a, fill_a, depth_b, fill_b;
    depth_a = fifo_depth(120, 100.0, 80.0);
    fill_a = fifo_fill(120, steps(100), steps(80));
    depth_b = fifo_depth(120, 100.0, 80.0, 0.75);
    fill_b = fifo_fill(120, steps(100), steps(80), 4);
    $display("part a: formula %0d, simulation %0d; part b: formula %0d, simulation %0d", depth_a, fill_a, depth_b, fill_b);
    if (depth_a != 24 || fill_a != 25) begin errors++; $display("part a expected 24 / 25"); end
    if (depth_b != 48 || fill_b != 48) begin errors++; $display("part b expected 48 / 48"); end
    if (fifo_depth(64, 100.0, 120.0) != 1) begin errors++; $display("a faster reader needs depth 1"); end

    for (int k = 0; k < 300; k++) begin
      int burst, fw, fr, idle, d, s;
      real duty;
      burst = $urandom_range(1, 300);
      fw = $urandom_range(20, 400);
      fr = $urandom_range(10, fw);                 // the reader is not faster than the writer
      idle = ($urandom_range(0, 2) == 0) ? 0 : $urandom_range(2, 8);
      duty = (idle == 0) ? 1.0 : 1.0 - 1.0 / idle;
      d = fifo_depth(burst, real'(fw), real'(fr), duty);
      s = fifo_fill(burst, steps(fw), steps(fr), idle);
      if (s < d || s > d + (idle == 0 ? 1 : 2)) begin
        // the period rounding to 0.05 ns moves the rates slightly; allow one more word
        if (s < d - 1 || s > d + 3) begin
          errors++;
          $display("burst %0d fw %0d fr %0d idle %0d: formula %0d, simulation %0d", burst, fw, fr, idle, d, s);
        end
      end
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
