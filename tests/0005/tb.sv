
module tb;
  //@page function automatic longint unsigned by_enumeration

  //@page function automatic string smallest_01_multiple

  // Remainder of a decimal string, so long answers need no big integers.
  function automatic int mod_of(string y, int x);
    int m = 0;
    for (int i = 0; i < y.len(); i++) m = (m * 10 + (y[i] - "0")) % x;
    return m;
  endfunction

  initial begin
    string y;
    int    errors = 0;
    for (int x = 1; x <= 300; x++) begin
      y = smallest_01_multiple(x);
      if (y[0] != "1" || mod_of(y, x) != 0) errors++;
      foreach (y[i]) if (y[i] != "0" && y[i] != "1") errors++;
      // Minimality: the enumeration is minimal by construction (fits 64 bits up to 19 digits)
      if (y.len() <= 18 && $sformatf("%0d", by_enumeration(x)) != y) errors++;
    end
    if (smallest_01_multiple(7) != "1001" || smallest_01_multiple(9999).len() != 36) errors++;
    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
