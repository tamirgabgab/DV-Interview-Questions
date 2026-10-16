// The class runs as published: Verilator 5.052 with the z3 solver supports randomize() with
// the constraints on the angle array. A triangle with a 230 degree arc must be rejected by
// the constraints, and every drawn triangle must pass the independent cross-product check.
//@page class circle_tri;

module tb;
  initial begin
    circle_tri t = new();
    int errors = 0, n = 0;
    repeat (500) begin
      if (!t.randomize()) errors++;
      else if (!t.center_inside()) errors++;
      n++;
    end
    // c_gaps must reject a triangle with a 230 degree arc (expected: one UNSATCONSTR warning)
    if (t.randomize() with { a[0] == 20; a[1] == 70; a[2] == 150; }) errors++;
    // ... and accept one with all arcs below 180 degrees
    if (!t.randomize() with { a[0] == 20; a[1] == 140; a[2] == 250; }) errors++;
    else if (!t.center_inside()) errors++;
    if (errors == 0) $display("PASS draws=%0d", n);
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
