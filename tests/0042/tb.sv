// Question 0042: the page's camel_segments / camel_distance / camel_passes against the
// page's numbers (400 km, the stops at 60 and 160 with 3, 2 and 1 loads, 9 passes, 460
// for an empty arrival, the bonus case T = 200), and on several (a, c, w, T): the
// segments add up to the closed form when T <= c, every pass carries at most c and ends
// non-negative, the depots end with T litres at the far end and nothing behind, and the
// water burned plus the water delivered is w.
module tb;
  //@page function automatic int camel_segments

  int errors = 0;

  task automatic near(string what, real got, real want, real tol);
    if (got < want - tol || got > want + tol) begin errors++; $display("%s: got %f, expected %f", what, got, want); end
  endtask

  task automatic check_case(string what, real a, real c, real w, real T);
    real x0[MAXS], x1[MAXS], carry0[MAXP], carry1[MAXP], depots[MAXS + 1];
    int loads[MAXS], seg[MAXP];
    bit back[MAXP];
    int n = camel_segments(a, c, w, T, x0, x1, loads), p, expect_p = 0;
    real burned = 0.0;
    p = camel_passes(a, c, w, T, seg, back, carry0, carry1, depots);
    if (T <= c) near({what, ": segments vs closed form"}, x1[n - 1], camel_distance(a, c, w, T), 1e-6);
    for (int i = 0; i < n; i++) begin
      expect_p += 2 * loads[i] - 1;
      if (i > 0 && x0[i] != x1[i - 1]) begin errors++; $display("%s: segment %0d does not start where %0d ends", what, i, i - 1); end
      if (x1[i] <= x0[i]) begin errors++; $display("%s: segment %0d has no length", what, i); end
    end
    if (p != expect_p) begin errors++; $display("%s: %0d passes, expected %0d", what, p, expect_p); end
    for (int i = 0; i < p; i++) begin
      burned += carry0[i] - carry1[i];
      if (carry0[i] > c + 1e-9 || carry1[i] < -1e-9) begin errors++; $display("%s: pass %0d carries %f -> %f", what, i, carry0[i], carry1[i]); end
      if (back[i] && carry1[i] != 0.0) begin errors++; $display("%s: pass %0d back arrives with %f", what, i, carry1[i]); end
    end
    near({what, ": delivered"}, depots[n], T, 1e-6);
    near({what, ": burned + delivered"}, burned + depots[n], w, 1e-6);
    for (int i = 0; i < n; i++) if (depots[i] < -1e-9 || depots[i] > 1e-9) begin errors++; $display("%s: depot %0d ends with %f", what, i, depots[i]); end
  endtask

  initial begin
    real x0[MAXS], x1[MAXS], carry0[MAXP], carry1[MAXP], depots[MAXS + 1];
    int loads[MAXS], seg[MAXP];
    bit back[MAXP];
    int n, p;

    near("camel_distance(0.5, 150, 450, 30)", camel_distance(0.5, 150, 450, 30), 400.0, 1e-9);
    near("camel_distance(0.5, 150, 450, 0)", camel_distance(0.5, 150, 450, 0), 460.0, 1e-9);
    near("camel_distance(0.5, 150, 250, 30)", camel_distance(0.5, 150, 250, 30), 920.0 / 3.0, 1e-9);
    near("camel_distance(0.5, 150, 150, 30)", camel_distance(0.5, 150, 150, 30), 240.0, 1e-9);
    n = camel_segments(0.5, 150, 450, 30, x0, x1, loads);
    if (n != 3 || x1[0] != 60.0 || x1[1] != 160.0 || x1[2] != 400.0 || loads[0] != 3 || loads[1] != 2 || loads[2] != 1) begin
      errors++; $display("segments of part a: n=%0d ends %f %f %f loads %0d %0d %0d", n, x1[0], x1[1], x1[2], loads[0], loads[1], loads[2]);
    end
    p = camel_passes(0.5, 150, 450, 30, seg, back, carry0, carry1, depots);
    if (p != 9 || carry0[0] != 150.0 || carry1[0] != 120.0 || !back[1] || carry0[1] != 30.0 || carry0[8] != 150.0 || carry1[8] != 30.0) begin
      errors++; $display("passes of part a: %0d, first %f -> %f, back %0d with %f, last %f -> %f", p, carry0[0], carry1[0], back[1], carry0[1], carry0[8], carry1[8]);
    end
    if (depots[3] != 30.0 || depots[0] != 0.0 || depots[1] != 0.0 || depots[2] != 0.0) begin errors++; $display("depots of part a end %f %f %f %f", depots[0], depots[1], depots[2], depots[3]); end
    // the bonus: 200 litres to deliver, levels 450, 300, 200
    n = camel_segments(0.5, 150, 450, 200, x0, x1, loads);
    if (n != 2 || loads[1] != 2) begin errors++; $display("T = 200: %0d segments, loads[1] = %0d", n, loads[1]); end
    near("T = 200 distance", x1[n - 1], 380.0 / 3.0, 1e-9);

    check_case("part a", 0.5, 150, 450, 30);
    check_case("empty arrival", 0.5, 150, 450, 0);
    check_case("partial load", 0.5, 150, 250, 30);
    check_case("one load", 0.5, 150, 150, 30);
    check_case("T = c", 0.5, 150, 600, 150);
    check_case("ten loads", 1.0, 100, 1000, 0);
    check_case("big camel", 0.2, 300, 3000, 200);
    check_case("T > c", 0.5, 150, 450, 200);
    check_case("odd numbers", 0.3, 120, 1000, 40);
    for (int w = 50; w <= 1500; w += 70) check_case($sformatf("w = %0d", w), 0.4, 130, w, (w > 60) ? 60 : 0);

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
