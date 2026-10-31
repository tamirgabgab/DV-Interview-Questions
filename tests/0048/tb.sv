// Question 0048, part c: the page's tilted_path on the example, at theta = 0 against part a,
// and on random cases: the stops on their lines, the three legs adding up to the length
// (the lower bound |A B2| reached, so the path is the shortest), and no shorter path when
// either stop moves a little.
module tb;
  //@page function automatic real tilted_path

  int errors = 0;
  real PI = 3.14159265358979323846;

  function automatic real seg(real x0, real y0, real x1, real y1);
    return $sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0));
  endfunction

  // the length of the path that takes food at distance s from (0, H) along the food line
  // and water at (q, 0)
  function automatic real path_len(real L, real H, real a, real b, real theta, real s, real q);
    real t = theta * PI / 180.0;
    real fx = s * $cos(t), fy = H + s * $sin(t);
    return seg(0, a, fx, fy) + seg(fx, fy, q, 0) + seg(q, 0, L, b);
  endfunction

  function automatic bit close(real x, real y, real tol);
    return (x - y < tol) && (y - x < tol);
  endfunction

  initial begin
    real L, H, a, b, theta, z, fx, fy, wx, t, s, legs, d;
    // the page's example and the self-check
    z = tilted_path(7, 3, 1, 2, 15, fx, fy, wx);
    if (!close(z * z, 92 + 10 * $sqrt(3.0), 1e-9) || !close(fx, 0.8026860219310012, 1e-9) || !close(wx, 4.6233096782319105, 1e-9)) begin
      errors++; $display("example: z = %f, food (%f, %f), water %f", z, fx, fy, wx);
    end
    z = tilted_path(7, 3, 1, 2, 45, fx, fy, wx);
    if (!close(z * z, 106, 1e-9)) begin errors++; $display("theta = 45: z^2 = %f", z * z); end
    // theta = 0 is part a: z = sqrt(L^2 + (2H + b - a)^2), food at L (H - a) / D
    z = tilted_path(7, 3, 1, 2, 0, fx, fy, wx);
    if (!close(z, $sqrt(98.0), 1e-9) || !close(fx, 2, 1e-9) || !close(fy, 3, 1e-9) || !close(wx, 5, 1e-9)) begin
      errors++; $display("theta = 0: z = %f, food (%f, %f), water %f", z, fx, fy, wx);
    end
    for (int n = 0; n < 3000; n++) begin
      L = 0.5 + 19.5 * $urandom_range(0, 100000) / 100000.0;
      H = 0.5 + 9.5 * $urandom_range(0, 100000) / 100000.0;
      theta = 60.0 * $urandom_range(0, 100000) / 100000.0;
      t = theta * PI / 180.0;
      a = H * $urandom_range(0, 1000) / 1000.0;
      b = (H + L * $sin(t) / $cos(t)) * $urandom_range(0, 1000) / 1000.0;
      z = tilted_path(L, H, a, b, theta, fx, fy, wx);
      // the food stop on the food line, at distance s from (0, H)
      if (theta > 0) s = (fy - H) / $sin(t); else s = fx;
      if (!close((fy - H) * $cos(t), fx * $sin(t), 1e-7 * (L + H))) begin
        errors++; $display("food stop off the food line: L %f H %f a %f b %f theta %f", L, H, a, b, theta);
      end
      legs = seg(0, a, fx, fy) + seg(fx, fy, wx, 0) + seg(wx, 0, L, b);
      if (!close(legs, z, 1e-9 * (L + H))) begin
        errors++; $display("legs %f != z %f: L %f H %f a %f b %f theta %f", legs, z, L, H, a, b, theta);
      end
      // no shorter path when a stop moves
      d = 1e-3 * (L + H);
      if (path_len(L, H, a, b, theta, s + d, wx) < z - 1e-12 || path_len(L, H, a, b, theta, s - d, wx) < z - 1e-12 ||
          path_len(L, H, a, b, theta, s, wx + d) < z - 1e-12 || path_len(L, H, a, b, theta, s, wx - d) < z - 1e-12) begin
        errors++; $display("a shorter path nearby: L %f H %f a %f b %f theta %f", L, H, a, b, theta);
      end
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
