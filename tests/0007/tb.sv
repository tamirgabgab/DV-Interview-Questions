// The classes run as published: Verilator (a development commit after 5.052) with the z3
// solver supports randomize() with the constraints on the angle arrays. A triangle with
// a 230 degree arc must be rejected by the constraints, every drawn triangle must pass the
// independent cross-product check, and the polygon class must do the same for every n
// from 3 to 10, with a 200 degree arc rejected.
//@page class circle_tri;
//@page class circle_poly;

module tb;
  initial begin
    circle_tri t = new();
    circle_poly p = new();
    int errors = 0, n = 0, drawn = 0;
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

    // part b: every n from 3 to 10
    for (int k = 3; k <= 10; k++) begin
      p.n = k;
      repeat (200) begin
        if (!p.randomize()) begin errors++; $display("n=%0d: randomize failed", k); end
        else begin
          if (p.a.size() != k) begin errors++; $display("n=%0d: size %0d", k, p.a.size()); end
          if (!p.center_inside()) begin errors++; $display("n=%0d: centre outside", k); p.print(); end
          for (int i = 1; i < k; i++)
            if (p.a[i] <= p.a[i - 1] || p.a[i] - p.a[i - 1] >= 180) begin errors++; $display("n=%0d: bad arc", k); end
          if (360 - (p.a[k - 1] - p.a[0]) >= 180) begin errors++; $display("n=%0d: bad closing arc", k); end
          drawn++;
        end
      end
    end
    // a square with a 200 degree arc is rejected, one with four 90 degree arcs is accepted
    p.n = 4;
    if (p.randomize() with { a[0] == 0; a[1] == 50; a[2] == 100; a[3] == 160; }) errors++;
    if (!p.randomize() with { a[0] == 10; a[1] == 100; a[2] == 190; a[3] == 280; }) errors++;
    else if (!p.center_inside()) errors++;
    // n = 3 of the polygon class agrees with the triangle class on the page example
    p.n = 3;
    if (!p.randomize() with { a[0] == 20; a[1] == 140; a[2] == 250; }) errors++;
    else if (!p.center_inside()) errors++;

    if (errors == 0) $display("PASS draws=%0d polygons=%0d", n, drawn);
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
