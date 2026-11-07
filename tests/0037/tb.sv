//@page function automatic int edit_distance(string a, string b);
//@page function automatic lines_t diff
//@page function automatic int edit_distance_within
//@page function automatic int edit_distance_swaps
// Question 0037: the page's SystemVerilog against references written here independently: the
// distance of the suffixes filled from the end of the streams (with or without the swap of two
// neighbours), and for the reports of diff a check that the lines, in order, are an edit script
// of a into b with every packet between them the same, as many lines as the distance. On the
// page's examples and random streams of A to D.
module tb;
  int errors = 0;

  task automatic fail(string what);
    errors++;
    if (errors < 20) $display("%s", what);
  endtask

  // the distance of a[i:] and b[j:], from the end: the first packet of each suffix missing,
  // extra, kept or changed, or (swap) the first two of each in the opposite order
  function automatic int ref_dist(string a, string b, bit swap);
    int s[][];
    int m = a.len(), n = b.len(), v;
    s = new[m + 1];
    foreach (s[i]) s[i] = new[n + 1];
    for (int i = m; i >= 0; i--)
      for (int j = n; j >= 0; j--) begin
        if (i == m) s[i][j] = n - j;
        else if (j == n) s[i][j] = m - i;
        else begin
          v = 1 + s[i + 1][j];
          if (1 + s[i][j + 1] < v) v = 1 + s[i][j + 1];
          if (int'(a[i] != b[j]) + s[i + 1][j + 1] < v) v = int'(a[i] != b[j]) + s[i + 1][j + 1];
          if (swap && i + 1 < m && j + 1 < n && a[i] == b[j + 1] && a[i + 1] == b[j] && 1 + s[i + 2][j + 2] < v)
            v = 1 + s[i + 2][j + 2];
          s[i][j] = v;
        end
      end
    return s[0][0];
  endfunction

  // the lines of a report are an edit script of a into b: reach[(i, j, k)] says that the
  // first k lines take a[0:i] to b[0:j], every packet not in a line the same in both
  function automatic bit consistent(string a, string b, lines_t ops);
    int m = a.len(), n = b.len(), K = ops.size();
    byte kd[], xs[], ys[];
    bit reach[];
    kd = new[K]; xs = new[K]; ys = new[K];
    foreach (ops[k]) begin
      xs[k] = ops[k][0]; ys[k] = ops[k][0];
      if (ops[k] == $sformatf("%c missing", ops[k][0])) kd[k] = "m";
      else if (ops[k] == $sformatf("%c extra", ops[k][0])) kd[k] = "e";
      else if (ops[k].len() == 14 && ops[k].substr(1, 12) == " changed to ") begin kd[k] = "c"; ys[k] = ops[k][13]; end
      else return 0;
    end
    reach = new[(m + 1) * (n + 1) * (K + 1)];
    foreach (reach[x]) reach[x] = 0;
    reach[0] = 1;
    for (int i = 0; i <= m; i++)
      for (int j = 0; j <= n; j++)
        for (int k = 0; k <= K; k++) begin
          if (!reach[(i * (n + 1) + j) * (K + 1) + k]) continue;
          if (i < m && j < n && a[i] == b[j]) reach[((i + 1) * (n + 1) + j + 1) * (K + 1) + k] = 1;
          if (k == K) continue;
          if (kd[k] == "m" && i < m && a[i] == xs[k]) reach[((i + 1) * (n + 1) + j) * (K + 1) + k + 1] = 1;
          if (kd[k] == "e" && j < n && b[j] == ys[k]) reach[(i * (n + 1) + j + 1) * (K + 1) + k + 1] = 1;
          if (kd[k] == "c" && i < m && j < n && a[i] == xs[k] && b[j] == ys[k])
            reach[((i + 1) * (n + 1) + j + 1) * (K + 1) + k + 1] = 1;
        end
    return reach[(m * (n + 1) + n) * (K + 1) + K];
  endfunction

  function automatic string pick(int len);
    string letters = "ABCD", s = "";
    int r;
    repeat (len) begin
      r = $urandom_range(3);
      s = {s, letters.substr(r, r)};
    end
    return s;
  endfunction

  initial begin
    string a, b;
    lines_t r;
    int want, w;

    // the page's examples
    if (edit_distance("ABCDEFGH", "ABDEYGHH") != 3) fail("edit_distance(ABCDEFGH, ABDEYGHH)");
    if (edit_distance("AB", "XAB") != 1 || edit_distance("ABC", "") != 3) fail("edit_distance: row and column 0");
    r = diff("ABCDEFGH", "ABDEYGHH", 0);
    if (r.size() != 3 || r[0] != "C missing" || r[1] != "F changed to Y" || r[2] != "H extra") fail("diff of part a");
    r = diff("ABCDEF", "ABDXEF", 0);
    if (r.size() != 2 || r[0] != "C missing" || r[1] != "X extra") fail("diff of the tie, gaps first");
    r = diff("ABCDEF", "ABDXEF", 1);
    if (r.size() != 2 || r[0] != "C changed to D" || r[1] != "D changed to X") fail("diff of the tie, changed first");
    if (edit_distance_within("ABCDEFGHIJKL", "ABCEFGHIXJKL", 2) != 2) fail("edit_distance_within, d = 2");
    if (edit_distance_within("ABCDEFGHIJKL", "ABCEFGHIXJKL", 1) != -1) fail("edit_distance_within, d = 1");
    if (edit_distance_within("ABC", "ABCDEF", 2) != -1) fail("edit_distance_within, the lengths");
    if (edit_distance_swaps("ABCDEFGH", "ABDCEFHG") != 2 || edit_distance("ABCDEFGH", "ABDCEFHG") != 4) fail("the swaps of part d");
    if (edit_distance_swaps("CA", "ABC") != 3) fail("edit_distance_swaps(CA, ABC)");

    // random streams against the references
    repeat (600) begin
      a = pick($urandom_range(8));
      b = pick($urandom_range(8));
      want = ref_dist(a, b, 0);
      if (edit_distance(a, b) != want) fail($sformatf("edit_distance(%s, %s)", a, b));
      if (edit_distance_swaps(a, b) != ref_dist(a, b, 1)) fail($sformatf("edit_distance_swaps(%s, %s)", a, b));
      for (int d = 0; d <= 9; d++) begin
        w = edit_distance_within(a, b, d);
        if (w != (want <= d ? want : -1)) fail($sformatf("edit_distance_within(%s, %s, %0d) = %0d", a, b, d, w));
      end
      for (int p = 0; p <= 1; p++) begin
        r = diff(a, b, p[0]);
        if (r.size() != want || !consistent(a, b, r)) fail($sformatf("diff(%s, %s, %0d)", a, b, p));
      end
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
