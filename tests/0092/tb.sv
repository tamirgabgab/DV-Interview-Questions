// Question 0092: the page's SystemVerilog. regions_by_chords, regions and euler_regions for
// n from 0 to 12 against C(n, 4) + C(n, 2) + 1 computed here; count_regions on the figures'
// points (16 for the pentagon, 31 for six points in general position, 30 for the regular
// hexagon), on the regular polygons up to 12 against the table of the page, and on random
// points (general position) up to 9 against the formula.
module tb;
  //@page function automatic int regions_by_chords
  //@page function automatic longint regions
  //@page function automatic int count_regions

  int errors = 0;

  function automatic longint ref_regions(int n);
    longint c4 = 0, c2 = 0;
    if (n >= 4) c4 = longint'(n) * (n - 1) * (n - 2) * (n - 3) / 24;
    if (n >= 2) c2 = longint'(n) * (n - 1) / 2;
    return c4 + c2 + 1;
  endfunction

  task automatic check(string what, longint got, longint want);
    if (got != want) begin
      errors++;
      $display("FAIL %s: got %0d, want %0d", what, got, want);
    end
  endtask

  initial begin
    int reg_table[13] = '{0, 1, 2, 4, 8, 16, 30, 57, 88, 163, 230, 386, 456};
    real ang[$];
    for (int n = 0; n <= 12; n++) begin
      check($sformatf("regions_by_chords(%0d)", n), regions_by_chords(n), ref_regions(n));
      check($sformatf("regions(%0d)", n), regions(n), ref_regions(n));
      check($sformatf("euler_regions(%0d)", n), euler_regions(n), ref_regions(n));
    end
    ang = '{90.0, 162.0, 234.0, 306.0, 18.0};
    check("pentagon", count_regions(ang), 16);
    ang = '{85.0, 152.0, 203.0, 271.0, 324.0, 32.0};
    check("six points", count_regions(ang), 31);
    for (int n = 1; n <= 12; n++) begin
      ang = {};
      for (int k = 0; k < n; k++) ang.push_back(90.0 + 360.0 * k / n);
      check($sformatf("regular %0d-gon", n), count_regions(ang), reg_table[n]);
    end
    void'($urandom(92));
    for (int n = 0; n <= 9; n++)
      for (int r = 0; r < 3; r++) begin
        ang = {};
        for (int k = 0; k < n; k++) ang.push_back(($urandom % 360000) / 1000.0);
        check($sformatf("random %0d points", n), count_regions(ang), ref_regions(n));
      end
    if (errors == 0) $display("PASS regions and count_regions");
    else $display("FAILED with %0d errors", errors);
    $finish;
  end
endmodule
