//@flags --assert --timing
//@page function automatic longint unsigned paths_rd
//@page module paths_rows #(
//@page function automatic longint unsigned pow_mod
//@page module paths_cols
//@page module paths_rows_check
// Question 0022: the page's SystemVerilog against references written here independently: a
// full table over the cells for right and down, and for right, up and down a sum over every
// pair of rows of a column whose cells between them are all open. paths_rows is fed a row a
// clock and paths_cols a column a clock, exact (64 bits) and mod 10^9 + 7 (32 bits), on the
// page's boards (9 and 32, the zigzag 0 and 9), empty boards (28, 729, C(18, 9), 10^9) and
// random boards; paths_rd on every board up to 34 x 34 against the table; pow_mod against
// repeated multiplication. The per-clock tables of the page (paths_rows on the board of part
// b, paths_cols on the zigzag) against the registers after every clock, and the follow-up's
// paths_rows_check bound to both paths_rows instances (its assertions stop the run when they
// fail; the corners it covers are counted here and must all be reached).
module tb;
  localparam longint unsigned P = 64'd1000000007;
  logic clk = 0, rst_n = 0, valid = 0, first = 0;
  logic [9:0] blk = 0;                 // a row (for paths_rows) or a column (for paths_cols)
  logic [63:0] r7, r10, c3, c10;
  logic [31:0] r7m, c3m;
  int errors = 0;

  paths_rows #(.N(7),  .W(64))           u_r7  (.clk, .rst_n, .valid, .first, .block(blk[6:0]), .count(r7));
  paths_rows #(.N(7),  .W(32), .P(P))    u_r7m (.clk, .rst_n, .valid, .first, .block(blk[6:0]), .count(r7m));
  paths_rows #(.N(10), .W(64))           u_r10 (.clk, .rst_n, .valid, .first, .block(blk),      .count(r10));
  paths_cols #(.M(3),  .W(64))           u_c3  (.clk, .rst_n, .valid, .first, .block(blk[2:0]), .count(c3));
  paths_cols #(.M(3),  .W(32), .P(P))    u_c3m (.clk, .rst_n, .valid, .first, .block(blk[2:0]), .count(c3m));
  paths_cols #(.M(10), .W(64))           u_c10 (.clk, .rst_n, .valid, .first, .block(blk),      .count(c10));
  always #5 clk = ~clk;

  paths_rows_check #(.N(7))  u_k7  (.clk, .rst_n, .valid, .first, .block(blk[6:0]), .count(r7));
  paths_rows_check #(.N(10)) u_k10 (.clk, .rst_n, .valid, .first, .block(blk),      .count(r10));
  // the corners of the checker's cover properties on the 7-column instance, counted here
  int hit_s = 0, hit_t = 0, hit_wall = 0;
  always @(posedge clk) if (rst_n && valid) begin
    if (first && blk[0]) hit_s++;
    if (blk[6]) hit_t++;
    if (&blk[6:0]) hit_wall++;
  end

  // the board: g[r][c] = 1 is an obstacle; m rows, n columns
  bit g[12][12];
  int m, n;

  task automatic fail(string what);
    errors++;
    if (errors < 20) $display("%s", what);
  endtask

  // right and down: the full table
  function automatic longint unsigned ref_rd();
    longint unsigned f[12][12];
    for (int r = 0; r < m; r++)
      for (int c = 0; c < n; c++)
        f[r][c] = g[r][c] ? 0 : (r == 0 && c == 0) ? 1 : (r ? f[r - 1][c] : 0) + (c ? f[r][c - 1] : 0);
    return f[m - 1][n - 1];
  endfunction

  // right, up and down: the paths that end at (b, c) entered column c at a row a with every
  // cell from a to b open
  function automatic longint unsigned ref_rud();
    longint unsigned f[12][12], in_a;
    bit open;
    for (int c = 0; c < n; c++)
      for (int b = 0; b < m; b++) begin
        f[b][c] = 0;
        if (g[b][c]) continue;
        for (int a = 0; a < m; a++) begin
          open = 1;
          for (int k = (a < b ? a : b); k <= (a < b ? b : a); k++) if (g[k][c]) open = 0;
          if (!open) continue;
          in_a = c == 0 ? longint'(a == 0) : f[a][c - 1];
          f[b][c] += in_a;
        end
      end
    return f[m - 1][n - 1];
  endfunction

  function automatic void random_board(int mm, int nn, int pct);
    m = mm; n = nn;
    for (int r = 0; r < 12; r++) for (int c = 0; c < 12; c++) g[r][c] = $urandom_range(99) < pct;
    g[0][0] = 0;
    if ($urandom_range(9) != 0) g[m - 1][n - 1] = 0;
  endfunction

  function automatic void board_of(string rows[$]);
    m = rows.size(); n = rows[0].len();
    foreach (rows[r]) for (int c = 0; c < n; c++) g[r][c] = rows[r][c] == "1";
  endfunction

  // the board a row a clock (paths_rows) or a column a clock (paths_cols), now and then with
  // an idle clock between two; the count is read the clock after the last one
  task automatic feed(bit by_rows);
    int len = by_rows ? m : n;
    for (int i = 0; i < len; i++) begin
      @(negedge clk);
      valid = 1; first = i == 0; blk = '0;
      for (int k = 0; k < (by_rows ? n : m); k++) blk[k] = by_rows ? g[i][k] : g[k][i];
      if ($urandom_range(3) == 0) begin @(negedge clk); valid = 0; first = 0; end
    end
    @(negedge clk); valid = 0; first = 0;
  endtask

  task automatic check_rows(longint unsigned want);
    feed(1);
    if (n == 7 && (r7 != want || r7m != 32'(want % P))) fail($sformatf("paths_rows N=7 %0dx%0d: %0d / %0d, want %0d", m, n, r7, r7m, want));
    if (n == 10 && r10 != want) fail($sformatf("paths_rows N=10 %0dx%0d: %0d, want %0d", m, n, r10, want));
  endtask

  task automatic check_cols(longint unsigned want);
    feed(0);
    if (m == 3 && (c3 != want || c3m != 32'(want % P))) fail($sformatf("paths_cols M=3 %0dx%0d: %0d / %0d, want %0d", m, n, c3, c3m, want));
    if (m == 10 && c10 != want) fail($sformatf("paths_cols M=10 %0dx%0d: %0d, want %0d", m, n, c10, want));
  endtask

  initial begin
    longint unsigned x, want;
    string b[$], z[$];
    b = '{"0000010", "0100000", "0001000"};
    z = '{"0100000", "0101000", "0001000"};
    #12 rst_n = 1;

    // the per-clock tables of the page: the registers after every clock
    begin
      longint unsigned want_r[3][7] = '{'{1, 1, 1, 1, 1, 0, 0}, '{1, 0, 1, 2, 3, 3, 3}, '{1, 1, 2, 0, 3, 6, 9}};
      longint unsigned want_c[7][3] = '{'{1, 1, 1}, '{0, 0, 1}, '{1, 1, 1}, '{1, 0, 0}, '{1, 1, 1}, '{3, 3, 3}, '{9, 9, 9}};
      logic [6:0] rows_b[3] = '{7'b0100000, 7'b0000010, 7'b0001000};
      logic [2:0] cols_z[7] = '{3'b000, 3'b011, 3'b000, 3'b110, 3'b000, 3'b000, 3'b000};
      for (int i = 0; i < 3; i++) begin
        @(negedge clk); valid = 1; first = i == 0; blk = '0; blk[6:0] = rows_b[i];
        @(negedge clk); valid = 0; first = 0;
        for (int c = 0; c < 7; c++)
          if (u_r7.row[c] != want_r[i][c]) fail($sformatf("paths_rows clock %0d: row[%0d] = %0d, want %0d", i + 1, c, u_r7.row[c], want_r[i][c]));
        if (r7 != want_r[i][6]) fail($sformatf("paths_rows clock %0d: count %0d", i + 1, r7));
      end
      for (int i = 0; i < 7; i++) begin
        @(negedge clk); valid = 1; first = i == 0; blk = '0; blk[2:0] = cols_z[i];
        @(negedge clk); valid = 0; first = 0;
        for (int r = 0; r < 3; r++)
          if (u_c3.out[r] != want_c[i][r]) fail($sformatf("paths_cols clock %0d: out[%0d] = %0d, want %0d", i + 1, r, u_c3.out[r], want_c[i][r]));
        if (c3 != want_c[i][2]) fail($sformatf("paths_cols clock %0d: count %0d", i + 1, c3));
      end
    end

    // the corners of the checker: S blocked, a fully blocked row, T blocked
    board_of('{"1000000", "0000000", "0000000"});
    check_rows(0);
    board_of('{"0000000", "1111111", "0000000"});
    check_rows(0);
    board_of('{"0000000", "0000000", "0000001"});
    check_rows(0);

    // the page's boards and the empty ones
    board_of(b);
    if (ref_rd() != 9 || ref_rud() != 32) fail("the references on the board of part b");
    check_rows(9); check_cols(32);
    board_of(z);
    if (ref_rd() != 0 || ref_rud() != 9) fail("the references on the zigzag");
    check_rows(0); check_cols(9);
    board_of('{"0000000", "0000000", "0000000"});
    check_rows(28); check_cols(729);
    m = 10; n = 10;
    foreach (g[r, c]) g[r][c] = 0;
    check_rows(48620); check_cols(1000000000);
    m = 10; n = 12;
    check_cols(64'd100000000000);
    m = 3; n = 12;
    check_cols(177147);

    // random boards
    repeat (150) begin
      random_board(1 + $urandom_range(9), 7, $urandom_range(40));
      check_rows(ref_rd());
      random_board(1 + $urandom_range(9), 10, $urandom_range(40));
      check_rows(ref_rd());
      random_board(3, 1 + $urandom_range(11), $urandom_range(40));
      check_cols(ref_rud());
      random_board(10, 1 + $urandom_range(11), $urandom_range(30));
      check_cols(ref_rud());
    end
    // a long empty board mod P: 3^40 is far above 2^32
    m = 3; n = 41;
    foreach (g[r, c]) g[r][c] = 0;
    for (int i = 0; i < n; i++) begin
      @(negedge clk); valid = 1; first = i == 0; blk = '0;
    end
    @(negedge clk); valid = 0; first = 0;
    if (c3m != 32'(pow_mod(3, 40, P))) fail($sformatf("paths_cols mod P on 3 x 41: %0d", c3m));

    // paths_rd: every board up to 12 x 12 against the table, and the largest square in 64 bits
    for (int mm = 1; mm <= 12; mm++)
      for (int nn = 1; nn <= 12; nn++) begin
        m = mm; n = nn;
        foreach (g[r, c]) g[r][c] = 0;
        if (paths_rd(mm, nn) != ref_rd()) fail($sformatf("paths_rd(%0d, %0d) = %0d", mm, nn, paths_rd(mm, nn)));
      end
    if (paths_rd(3, 7) != 28 || paths_rd(34, 34) != 64'd7219428434016265740) fail("paths_rd(34, 34)");

    // pow_mod against repeated multiplication, and the m^(n-1) of part c
    repeat (200) begin
      longint unsigned base, e, pp;
      base = $urandom; e = $urandom_range(300); pp = 2 + $urandom_range(2000000000);
      x = 1 % pp;
      for (int i = 0; i < e; i++) x = x * (base % pp) % pp;
      if (pow_mod(base, e, pp) != x) fail($sformatf("pow_mod(%0d, %0d, %0d)", base, e, pp));
    end
    if (paths_rud_mod(3, 7) != 729 || paths_rud_mod(10, 10) != 1000000000 || paths_rud_mod(10, 11) != 64'd999999937)
      fail("paths_rud_mod");

    if (hit_s == 0 || hit_t == 0 || hit_wall == 0) fail($sformatf("corners not reached: %0d %0d %0d", hit_s, hit_t, hit_wall));
    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
