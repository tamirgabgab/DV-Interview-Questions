// Simulator limitation (Verilator 5.020): cannot randomize arrays with constraints. The translation keeps the
// class as published, turns every constraint block into a check function, and replaces
// randomize() by "draw from the declared ranges until every constraint holds".
//@translation-of class circle_tri; 49ce2e0eb7a4

class circle_tri;

  localparam int  FULL = 360;
  localparam int  HALF = FULL / 2;
  localparam real PI   = 3.14159265358979323846;

  int  a[3];                           // was: rand int a[3]
  real x[3];
  real y[3];

  // constraint c_range
  function bit c_range_ok();
    foreach (a[i]) if (!(a[i] inside {[0 : FULL - 1]})) return 0;
    return 1;
  endfunction

  // constraint c_order
  function bit c_order_ok();
    return a[0] < a[1] && a[1] < a[2];
  endfunction

  // constraint c_gaps
  function bit c_gaps_ok();
    return (a[1] - a[0]) < HALF &&
           (a[2] - a[1]) < HALF &&
           (FULL - (a[2] - a[0])) < HALF;
  endfunction

  // Replacement for randomize(): rejection sampling over the c_range domain
  function bit test_randomize();
    repeat (100000) begin
      foreach (a[i]) a[i] = $urandom_range(0, FULL - 1);
      if (c_range_ok() && c_order_ok() && c_gaps_ok()) begin
        post_randomize();
        return 1;
      end
    end
    return 0;
  endfunction

  function void post_randomize();
    real th;
    foreach (a[i]) begin
      th   = 2.0 * PI * real'(a[i]) / real'(FULL);
      x[i] = $cos(th);
      y[i] = $sin(th);
    end
  endfunction

  function bit center_inside();
    real s[3];
    int  j;
    for (int i = 0; i < 3; i++) begin
      j    = (i + 1) % 3;
      s[i] = (x[j] - x[i]) * (0.0 - y[i]) - (y[j] - y[i]) * (0.0 - x[i]);
    end
    return (s[0] > 0 && s[1] > 0 && s[2] > 0) ||
           (s[0] < 0 && s[1] < 0 && s[2] < 0);
  endfunction

endclass

module tb;
  initial begin
    circle_tri t = new();
    int errors = 0;
    repeat (2000) begin
      if (!t.test_randomize()) errors++;
      else if (!t.center_inside()) errors++;
    end
    // The check must also reject a triangle with a 230 degree arc
    t.a = '{20, 70, 150};
    t.post_randomize();
    if (t.c_gaps_ok() || t.center_inside()) errors++;
    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
