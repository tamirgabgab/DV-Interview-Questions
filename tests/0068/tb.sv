// Question 0068: the page's heap_t, StreamMedian, StreamQuantile and WindowQuantile against
// sorting the prefix or the window: the page's examples (the medians, p = 9/10, p = 1/4,
// W = 4 with p = 1/2, as the Python tests print them), the self-checks, and random streams
// with many duplicates, every p from 0 to 1 and windows from 1 to 7.
module tb;
  //@page class heap_t
  //@page class StreamQuantile
  //@page class WindowQuantile

  int errors = 0;

  // an insertion sort: Verilator's sort() of an int queue orders negative values as unsigned
  function automatic void isort(ref int s[$]);
    int v, j;
    for (int i = 1; i < s.size(); i++) begin
      v = s[i];
      for (j = i - 1; j >= 0 && s[j] > v; j--) s[j + 1] = s[j];
      s[j + 1] = v;
    end
  endfunction

  // the median of the values, doubled (so it stays an integer)
  function automatic int brute_median2(int vals[$]);
    int s[$] = vals;
    int n = s.size();
    isort(s);
    return (n % 2) ? 2 * s[n / 2] : s[n / 2 - 1] + s[n / 2];
  endfunction

  // the p-quantile by the nearest rank, p = num / den
  function automatic int brute_quantile(int vals[$], int num, int den);
    int s[$] = vals;
    int r = (num * s.size() + den - 1) / den;
    isort(s);
    if (r < 1) r = 1;
    return s[r - 1];
  endfunction

  initial begin
    int stream[10] = '{5, 15, 1, 3, 8, 7, 9, 10, 20, 2};
    int med2_want[10] = '{10, 20, 10, 8, 10, 12, 14, 15, 16, 15};      // twice the medians 5 10 5 4 5 6 7 7.5 8 7.5
    int q90_want[10] = '{5, 15, 15, 15, 15, 15, 15, 15, 20, 15};
    int q25_want[10] = '{5, 5, 1, 1, 3, 3, 3, 3, 5, 3};
    int win_want[10] = '{5, 5, 5, 3, 3, 3, 7, 8, 9, 9};
    int prefix[$], win[$], n, w, num, den, m;
    real med;
    StreamMedian sm;
    StreamQuantile q90, q25, sq;
    WindowQuantile wq;
    heap_t h;
    item_t it, nx;
    int x;

    // the heap alone: random pushes come out sorted, ties by the arrival number
    h = new(0);
    for (int i = 0; i < 200; i++) h.push('{$urandom_range(0, 9), i});
    it = h.pop();
    for (int i = 1; i < 200; i++) begin
      nx = h.pop();
      if (nx.v < it.v || (nx.v == it.v && nx.id < it.id)) begin errors++; $display("heap order at %0d", i); end
      it = nx;
    end
    if (h.size() != 0) begin errors++; $display("heap not empty"); end

    // the page's examples
    sm = new(); q90 = new(9, 10); q25 = new(1, 4); wq = new(4, 1, 2);
    foreach (stream[i]) begin
      sm.add(stream[i]); q90.add(stream[i]); q25.add(stream[i]); wq.add(stream[i]);
      med = sm.median();
      if (2.0 * med != med2_want[i]) begin errors++; $display("median after %0d: %f", i + 1, med); end
      if (q90.quantile() != q90_want[i]) begin errors++; $display("p = 0.9 after %0d: %0d", i + 1, q90.quantile()); end
      if (q25.quantile() != q25_want[i]) begin errors++; $display("p = 0.25 after %0d: %0d", i + 1, q25.quantile()); end
      if (wq.quantile() != win_want[i]) begin errors++; $display("W = 4 after %0d: %0d", i + 1, wq.quantile()); end
      // the self-checks: the median after six values is 6, p = 0.9 after ten is 15, the window's last is 9
      if (i == 5 && med != 6.0) begin errors++; $display("self-check a"); end
    end
    if (q90.quantile() != 15 || wq.quantile() != 9) begin errors++; $display("self-checks b, c"); end
    if (sm.low.size() != 5 || sm.high.size() != 5) begin errors++; $display("sizes at the end: %0d %0d", sm.low.size(), sm.high.size()); end

    // random streams against sorting
    for (int r = 0; r < 400; r++) begin
      n = $urandom_range(1, 30);
      w = $urandom_range(1, 7);
      den = 100;
      num = $urandom_range(0, 100);
      if (r % 10 == 0) num = 0;
      if (r % 10 == 1) num = 100;
      sm = new(); sq = new(num, den); wq = new(w, num, den);
      prefix = {};
      for (int i = 0; i < n; i++) begin
        x = int'($urandom_range(0, 12)) - 3;
        prefix.push_back(x);
        sm.add(x); sq.add(x); wq.add(x);
        if (2.0 * sm.median() != brute_median2(prefix)) begin errors++; $display("run %0d median at %0d", r, i); end
        if (sq.quantile() != brute_quantile(prefix, num, den)) begin
          errors++; $display("run %0d p = %0d/%0d at %0d: %0d vs %0d", r, num, den, i, sq.quantile(), brute_quantile(prefix, num, den));
        end
        win = (prefix.size() > w) ? prefix[prefix.size() - w:$] : prefix;
        if (wq.quantile() != brute_quantile(win, num, den)) begin
          errors++; $display("run %0d W = %0d p = %0d at %0d: %0d vs %0d", r, w, num, i, wq.quantile(), brute_quantile(win, num, den));
        end
        // the size invariants: |low| - |high| in {0, 1}; |low| = ceil(p n); the heaps hold at most 2 live + 1
        m = sm.low.size() - sm.high.size();
        if (m < 0 || m > 1) begin errors++; $display("run %0d sizes at %0d", r, i); end
        m = (num * (i + 1) + den - 1) / den; if (m < 1) m = 1;
        if (sq.low.size() != m) begin errors++; $display("run %0d |low| = %0d, target %0d", r, sq.low.size(), m); end
        if (wq.low.size() > 2 * wq.live[0] + 1 || wq.high.size() > 2 * wq.live[1] + 1) begin errors++; $display("run %0d heap too big at %0d", r, i); end
      end
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
