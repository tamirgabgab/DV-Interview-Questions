// The classes run as published: Verilator (development snapshot after 5.052, see the CI
// workflow for the exact commit) with the z3 solver supports rand dynamic arrays whose size
// comes from a constraint, foreach constraints over pairs, constraint_mode() and the
// constraint override in the subclass. Every randomized set is checked with the published
// checker and with an independent "paint the cells" reference. (The 5.052 release left
// some shapes of the subclass unrandomized; the snapshot does not.)

module tb;
  //@page function automatic bit shapes_ok
  //@page class square_set;
  //@page class rect_set extends

  int errors = 0;

  // Reference for shapes_ok: paint the unit cells of every shape, no cell used twice
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

  // Randomize one object many times; count what was seen. `bad` counts illegal results.
  task automatic run(square_set o, bit squares, int draws, output int seen_n, output int touching,
                     output int non_square, output int bad);
    seen_n = 0; touching = 0; non_square = 0; bad = 0;
    repeat (draws) begin
      if (!o.randomize()) begin errors++; continue; end
      if (o.x1.size() != o.n || o.y1.size() != o.n || o.x2.size() != o.n || o.y2.size() != o.n) errors++;
      if (!shapes_ok(o.N, o.M, squares, o.x1, o.y1, o.x2, o.y2) || !painted_ok(o.N, o.M, squares, o.x1, o.y1, o.x2, o.y2)) begin
        bad++;
        continue;
      end
      seen_n |= 1 << o.n;
      foreach (o.x1[i]) begin
        if (o.x2[i] - o.x1[i] != o.y2[i] - o.y1[i]) non_square++;
        for (int j = 0; j < i; j++)
          if (o.x2[i] == o.x1[j] || o.x2[j] == o.x1[i] || o.y2[i] == o.y1[j] || o.y2[j] == o.y1[i]) touching++;
      end
    end
  endtask

  function automatic int popcount(int v);
    int c = 0;
    for (int i = 0; i < 32; i++) c += v[i];
    return c;
  endfunction

  initial begin
    square_set s = new();
    square_set m = new();
    rect_set   r = new();
    int seen, touch, nonsq, bad, k;
    int ax1[], ay1[], ax2[], ay2[];

    // 1. Squares: only legal sets, several different n, touching pairs do occur
    run(s, 1, 60, seen, touch, nonsq, bad);
    if (bad != 0 || popcount(seen) < 3 || touch == 0 || nonsq != 0) errors++;
    $display("square_set: n seen mask=%b touching=%0d bad=%0d", seen, touch, bad);

    // 2. Part b with constraint_mode(0): rectangles appear, still no overlap
    m.c_square.constraint_mode(0);
    run(m, 0, 60, seen, touch, nonsq, bad);
    if (bad != 0 || popcount(seen) < 3 || nonsq == 0) errors++;
    $display("constraint_mode(0): n seen mask=%b non-square shapes=%0d bad=%0d", seen, nonsq, bad);

    // 3. Part b with the subclass (empty c_square override): rectangles appear, still no overlap
    run(r, 0, 60, seen, touch, nonsq, bad);
    if (bad != 0 || popcount(seen) < 3 || nonsq == 0) errors++;
    $display("rect_set: n seen mask=%b non-square shapes=%0d bad=%0d", seen, nonsq, bad);

    // 4. The checker against the painted reference on random sets, legal or not
    repeat (20000) begin
      k = $urandom_range(4, 1);        // assigned, not declared here: a declaration initializer runs once
      ax1 = new[k]; ay1 = new[k]; ax2 = new[k]; ay2 = new[k];
      foreach (ax1[i]) begin
        ax1[i] = $urandom_range(6, 1); ax2[i] = $urandom_range(7, ax1[i] + 1);
        ay1[i] = $urandom_range(5, 1); ay2[i] = $urandom_range(6, ay1[i] + 1);
      end
      if (shapes_ok(7, 6, 0, ax1, ay1, ax2, ay2) != painted_ok(7, 6, 0, ax1, ay1, ax2, ay2)) errors++;
      if (shapes_ok(7, 6, 1, ax1, ay1, ax2, ay2) != painted_ok(7, 6, 1, ax1, ay1, ax2, ay2)) errors++;
    end

    // 5. The cross: no corner inside the other shape, and still an overlap
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
