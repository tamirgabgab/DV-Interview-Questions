//@page function automatic int edit_distance(string a, string b);
//@page function automatic lines_t diff
//@page function automatic int edit_distance_within
//@page function automatic int edit_distance_swaps
// Question 0037: the page's SystemVerilog against references written here independently: the
// distance of the suffixes filled from the end of the streams (with or without the swap of two
// neighbours), and for the reports of diff a check that the lines, in order and at the cells
// they name, are an edit script of a into b with every packet between them the same, as many
// lines as the distance. On the
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

  // one line of a report: "X missing at (i, j)", "X extra at (i, j)" or "X changed to Y at
  // (i, j)"; kd is m, e or c, (i, j) the cell where the line's step ends
  function automatic bit parse(string s, output byte kd, output byte x, output byte y, output int i, output int j);
    int p = -1;
    for (int q = 0; q + 4 < s.len(); q++)
      if (s.substr(q, q + 4) == " at (") begin p = q; break; end
    if (p < 0 || $sscanf(s.substr(p + 5, s.len() - 1), "%d, %d)", i, j) != 2) return 0;
    x = s[0];
    y = s[0];
    if (s == $sformatf("%c missing at (%0d, %0d)", x, i, j)) kd = "m";
    else if (s == $sformatf("%c extra at (%0d, %0d)", x, i, j)) kd = "e";
    else if (s.len() > 14 && s.substr(1, 12) == " changed to " && s == $sformatf("%c changed to %c at (%0d, %0d)", x, s[13], i, j)) begin
      kd = "c";
      y = s[13];
    end else return 0;
    return 1;
  endfunction

  // the lines of a report, at their cells, are an edit script of a into b: from the cell
  // after one line to the start of the next only the same packet on both sides, every line's
  // packets where its cell says, and the same packets again from the last line to the corner
  function automatic bit consistent(string a, string b, lines_t ops);
    int ci = 0, cj = 0, i, j, si, sj;
    byte kd, x, y;
    foreach (ops[k]) begin
      if (!parse(ops[k], kd, x, y, i, j)) return 0;
      si = kd == "e" ? i : i - 1;
      sj = kd == "m" ? j : j - 1;
      if (si < ci || sj < cj || si - ci != sj - cj || i > a.len() || j > b.len()) return 0;
      for (int t = 0; t < si - ci; t++) if (a[ci + t] != b[cj + t]) return 0;
      if (kd == "m" && a[i - 1] != x) return 0;
      if (kd == "e" && b[j - 1] != x) return 0;
      if (kd == "c" && (a[i - 1] != x || b[j - 1] != y || x == y)) return 0;
      ci = i;
      cj = j;
    end
    if (a.len() - ci != b.len() - cj) return 0;
    for (int t = 0; t < a.len() - ci; t++) if (a[ci + t] != b[cj + t]) return 0;
    return 1;
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
    if (r.size() != 3 || r[0] != "C missing at (3, 2)" || r[1] != "F changed to Y at (6, 5)" || r[2] != "H extra at (7, 7)")
      fail("diff of part a");
    r = diff("ABCDEF", "ABDXEF", 0);
    if (r.size() != 2 || r[0] != "C missing at (3, 2)" || r[1] != "X extra at (4, 4)") fail("diff of the tie, gaps first");
    r = diff("ABCDEF", "ABDXEF", 1);
    if (r.size() != 2 || r[0] != "C changed to D at (3, 3)" || r[1] != "D changed to X at (4, 4)") fail("diff of the tie, changed first");
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
