// Simulator limitation (Verilator 5.020): no rand dynamic arrays and no constraints. The
// translation keeps the classes as published, turns every constraint block into a check
// function with the same expression, and replaces randomize() by do_randomize(), a
// step-by-step solver: n uniformly in c_count, then one shape at a time, uniformly among
// the shapes that pass c_on_grid, c_square (while enabled) and c_no_overlap against the
// shapes already placed; if no shape fits, start over with the same n. The published classes themselves were run
// once with real randomize() on Verilator 5.052 + z3 (see HANDOFF).
//@translation-of class square_set; 422825bb4f52
//@translation-of class rect_set extends f718aad08059

module tb;
  //@page function automatic bit shapes_ok

  class square_set;
    int N = 10, M = 8;
    int MAX_SHAPES = 6;

    int n;                               // was: rand
    int x1[], y1[], x2[], y2[];          // was: rand
    bit square_on = 1;                   // c_square.constraint_mode()

    function bit c_count_ok(int nn);
      return nn >= 1 && nn <= MAX_SHAPES;
    endfunction

    function bit c_on_grid_ok(int i);
      return x1[i] >= 1 && x2[i] <= N && x1[i] < x2[i] &&
             y1[i] >= 1 && y2[i] <= M && y1[i] < y2[i];
    endfunction

    virtual function bit c_square_ok(int i);
      return !square_on || x2[i] - x1[i] == y2[i] - y1[i];
    endfunction

    function bit c_no_overlap_ok(int i, int j);
      return x2[j] <= x1[i] || x2[i] <= x1[j] ||
             y2[j] <= y1[i] || y2[i] <= y1[j];
    endfunction

    // Shape k is legal against the shapes 0..k-1
    function bit fits(int k);
      if (!c_on_grid_ok(k) || !c_square_ok(k)) return 0;
      for (int i = 0; i < k; i++) if (!c_no_overlap_ok(i, k)) return 0;
      return 1;
    endfunction

    function int do_randomize();      // stands for randomize()
      int cand[$];                       // packed candidates: x1, y1, x2, y2 in 4 bits each
      int placed, c;
      cand.delete();
      n = $urandom_range(MAX_SHAPES, 1);
      if (!c_count_ok(n)) return 0;
      x1 = new[n]; y1 = new[n]; x2 = new[n]; y2 = new[n];
      forever begin
        for (placed = 0; placed < n; placed++) begin
          cand.delete();
          for (int a = 1; a <= N; a++) for (int b = 1; b <= M; b++)
            for (int cc = 1; cc <= N; cc++) for (int d = 1; d <= M; d++) begin
              x1[placed] = a; y1[placed] = b; x2[placed] = cc; y2[placed] = d;
              if (fits(placed)) cand.push_back((a << 12) | (b << 8) | (cc << 4) | d);
            end
          if (cand.size() == 0) break;   // stuck: start over
          c = cand[$urandom_range(cand.size() - 1, 0)];
          x1[placed] = c >> 12; y1[placed] = (c >> 8) & 15; x2[placed] = (c >> 4) & 15; y2[placed] = c & 15;
        end
        if (placed == n) return 1;
      end
    endfunction
  endclass

  class rect_set extends square_set;
    virtual function bit c_square_ok(int i);   // was: constraint c_square { }
      return 1;
    endfunction
  endclass

  int errors = 0;

  // Reference for shapes_ok: paint the unit cells of every shape, no used twice
  function automatic bit painted_ok(int N, int M, bit squares, int x1[], int y1[], int x2[], int y2[]);
    bit used[11][9];
    foreach (used[a, b]) used[a][b] = 0;
    foreach (x1[i]) begin
      if (x1[i] < 1 || y1[i] < 1 || x2[i] > N || y2[i] > M || x1[i] >= x2[i] || y1[i] >= y2[i]) return 0;
      if (squares && x2[i] - x1[i] != y2[i] - y1[i]) return 0;
      for (int a = x1[i]; a < x2[i]; a++)
        for (int b = y1[i]; b < y2[i]; b++) begin
          if (used[a][b]) return 0;
          used[a][b] = 1;
        end
    end
    return 1;
  endfunction

  // Run one object many times and check every result with the published checker
  task automatic run(square_set o, bit squares, output int seen_n, output int touching, output int non_square);
    seen_n = 0; touching = 0; non_square = 0;
    repeat (400) begin
      if (!o.do_randomize()) errors++;
      if (!shapes_ok(o.N, o.M, squares, o.x1, o.y1, o.x2, o.y2)) errors++;
      if (!painted_ok(o.N, o.M, squares, o.x1, o.y1, o.x2, o.y2)) errors++;
      if (o.x1.size() != o.n) errors++;
      seen_n |= 1 << o.n;
      foreach (o.x1[i]) begin
        if (o.x2[i] - o.x1[i] != o.y2[i] - o.y1[i]) non_square++;
        for (int j = 0; j < i; j++)
          if (o.x2[i] == o.x1[j] || o.x2[j] == o.x1[i] || o.y2[i] == o.y1[j] || o.y2[j] == o.y1[i]) touching++;
      end
    end
  endtask

  initial begin
    square_set s = new();
    rect_set   r = new();
    square_set m = new();
    int seen, touch, nonsq;
    int ax1[], ay1[], ax2[], ay2[];

    run(s, 1, seen, touch, nonsq);
    if (seen != 'b1111110 || touch == 0 || nonsq != 0) errors++;
    run(r, 0, seen, touch, nonsq);
    if (seen != 'b1111110 || touch == 0 || nonsq == 0) errors++;
    m.square_on = 0;                                    // c_square.constraint_mode(0)
    run(m, 0, seen, touch, nonsq);
    if (seen != 'b1111110 || nonsq == 0) errors++;

    // The checker against the painted reference on random sets, legal or not
    repeat (20000) begin
      int k = $urandom_range(4, 1);
      ax1 = new[k]; ay1 = new[k]; ax2 = new[k]; ay2 = new[k];
      foreach (ax1[i]) begin
        ax1[i] = $urandom_range(6, 1); ax2[i] = $urandom_range(7, ax1[i] + 1);
        ay1[i] = $urandom_range(5, 1); ay2[i] = $urandom_range(6, ay1[i] + 1);
      end
      if (shapes_ok(7, 6, 0, ax1, ay1, ax2, ay2) != painted_ok(7, 6, 0, ax1, ay1, ax2, ay2)) errors++;
      if (shapes_ok(7, 6, 1, ax1, ay1, ax2, ay2) != painted_ok(7, 6, 1, ax1, ay1, ax2, ay2)) errors++;
    end

    // The cross: no corner inside the other shape, and still an overlap
    ax1 = '{1, 4}; ay1 = '{4, 1}; ax2 = '{9, 6}; ay2 = '{6, 8};
    if (shapes_ok(9, 8, 0, ax1, ay1, ax2, ay2)) errors++;
    // Shared edge and shared corner are fine
    ax1 = '{1, 3, 5}; ay1 = '{1, 1, 3}; ax2 = '{3, 5, 7}; ay2 = '{3, 3, 5};
    if (!shapes_ok(9, 8, 1, ax1, ay1, ax2, ay2)) errors++;

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
