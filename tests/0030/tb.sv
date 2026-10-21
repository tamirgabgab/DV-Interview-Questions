// Question 0030: the page's shortest_path (the periodic strip) against distances and exit
// points computed by tests/0030/reference.py (every face sequence unfolded separately),
// then symmetry checks on a random sweep: mirroring the box in y or z, or swapping the
// spider and the fly, must not change the distance, and the exit point must sit on an
// edge of the spider's wall.
module tb;
  //@page function automatic real shortest_path

  typedef struct {
    real a, b, h, y0, z0, y1, z1;   // the box and the two points
    real d;                          // the shortest distance, from reference.py
    real ey1, ez1, ey2, ez2;         // the exit points of the tied best routes (one or two)
  } case_t;

  localparam int N = 16;
  case_t cases[N] = '{
    '{30.0, 12.0, 12.0, 6.0, 11.0, 6.0, 1.0,     40.000000000, 6.75, 12.0, 5.25, 12.0},
    '{30.0, 12.0, 12.0, 6.0, 1.0, 6.0, 11.0,     40.000000000, 5.25, 0.0, 6.75, 0.0},
    '{30.0, 12.0, 12.0, 6.0, 11.0, 6.0, 6.0,     37.000000000, 6.0, 12.0, 6.0, 12.0},
    '{2.0, 12.0, 12.0, 6.0, 11.0, 6.0, 1.0,      14.000000000, 6.0, 0.0, 6.0, 12.0},
    '{10.0, 4.0, 8.0, 1.0, 7.5, 3.5, 0.5,        15.206906326, 4.0, 5.944444444, 1.477272727, 8.0},
    '{30.0, 12.0, 12.0, 12.0, 11.0, 0.0, 1.0,    38.418745425, 12.0, 11.0, 12.0, 11.0},
    '{0.5, 12.0, 12.0, 6.0, 11.0, 6.0, 1.0,      12.500000000, 6.0, 0.0, 6.0, 12.0},
    '{30.0, 12.0, 2.0, 10.08, 1.55, 2.99, 0.1,   32.434404573, 9.732780, 0.0, 9.732780, 0.0},
    '{10.0, 3.0, 12.0, 1.41, 2.96, 1.63, 6.89,   13.542765596, 3.0, 3.442153, 3.0, 3.442153},
    '{5.0, 7.0, 25.0, 1.96, 22.91, 5.36, 3.99,   22.234855520, 7.0, 14.745890, 7.0, 14.745890},
    '{5.0, 7.0, 25.0, 0.89, 0.04, 6.1, 5.24,     11.524864424, 0.910272, 0.0, 0.910272, 0.0},
    '{10.0, 7.0, 6.0, 2.03, 5.77, 3.77, 4.07,    12.283859328, 2.062911, 6.0, 2.062911, 6.0},
    '{10.0, 7.0, 6.0, 6.77, 5.36, 2.09, 2.17,    15.115756680, 7.0, 5.450789, 7.0, 5.450789},
    '{10.0, 7.0, 12.0, 0.46, 3.62, 4.22, 0.04,   13.104029914, 0.0, 3.276533, 0.0, 3.276533},
    '{30.0, 3.0, 12.0, 1.07, 3.67, 2.09, 2.22,   32.871995680, 3.0, 3.584784, 3.0, 3.584784},
    '{1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 0.5,         2.000000000, 0.5, 0.0, 0.5, 1.0}
  };

  int errors = 0;

  function automatic bit near(real x, real y, real tol = 1e-6);
    return (x > y ? x - y : y - x) <= tol;
  endfunction

  // The point (0, y, z) is on an edge of the wall x = 0
  function automatic bit on_edge(real y, real z, real b, real h);
    bit in_wall = y >= -1e-9 && y <= b + 1e-9 && z >= -1e-9 && z <= h + 1e-9;
    return in_wall && (near(y, 0.0, 1e-9) || near(y, b, 1e-9) || near(z, 0.0, 1e-9) || near(z, h, 1e-9));
  endfunction

  initial begin
    real a, b, h, y0, z0, y1, z1, air;
    real d, ey, ez, d2, ey2, ez2;

    // the reference cases
    for (int i = 0; i < N; i++) begin
      case_t c = cases[i];
      d = shortest_path(c.a, c.b, c.h, c.y0, c.z0, c.y1, c.z1, ey, ez);
      if (!near(d, c.d)) begin
        errors++;
        $display("case %0d: distance %f, expected %f", i, d, c.d);
      end
      if (!((near(ey, c.ey1) && near(ez, c.ez1)) || (near(ey, c.ey2) && near(ez, c.ez2)))) begin
        errors++;
        $display("case %0d: exit (%f, %f), expected (%f, %f) or (%f, %f)", i, ey, ez, c.ey1, c.ez1, c.ey2, c.ez2);
      end
    end

    // random boxes: never shorter than through the air, exit on an edge, symmetric
    void'($urandom(30));
    for (int i = 0; i < 2000; i++) begin
      // assigned, not declared with initialisers: a static block would initialise them once
      a = 1.0 + ($urandom % 300) / 10.0;
      b = 1.0 + ($urandom % 200) / 10.0;
      h = 1.0 + ($urandom % 200) / 10.0;
      y0 = ($urandom % 1001) / 1000.0 * b; z0 = ($urandom % 1001) / 1000.0 * h;
      y1 = ($urandom % 1001) / 1000.0 * b; z1 = ($urandom % 1001) / 1000.0 * h;
      air = $sqrt(a * a + (y1 - y0) * (y1 - y0) + (z1 - z0) * (z1 - z0));
      d = shortest_path(a, b, h, y0, z0, y1, z1, ey, ez);
      if (d < air - 1e-9 || d > a + b + 2.0 * h + 1e-9) begin
        errors++;
        $display("random %0d: distance %f outside [%f, %f]", i, d, air, a + b + 2.0 * h);
      end
      if (!on_edge(ey, ez, b, h)) begin
        errors++;
        $display("random %0d: exit (%f, %f) is not on an edge of the wall", i, ey, ez);
      end
      // the spider walks to the exit point in a straight line inside its wall
      if ($sqrt((ey - y0) * (ey - y0) + (ez - z0) * (ez - z0)) > d + 1e-9) begin
        errors++;
        $display("random %0d: the exit point is farther than the whole path", i);
      end
      d2 = shortest_path(a, b, h, y1, z1, y0, z0, ey2, ez2);             // swap the two
      if (!near(d, d2)) begin errors++; $display("random %0d: swap gives %f, not %f", i, d2, d); end
      d2 = shortest_path(a, b, h, b - y0, z0, b - y1, z1, ey2, ez2);     // mirror in y
      if (!near(d, d2)) begin errors++; $display("random %0d: y mirror gives %f, not %f", i, d2, d); end
      d2 = shortest_path(a, b, h, y0, h - z0, y1, h - z1, ey2, ez2);     // mirror in z
      if (!near(d, d2)) begin errors++; $display("random %0d: z mirror gives %f, not %f", i, d2, d); end
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
