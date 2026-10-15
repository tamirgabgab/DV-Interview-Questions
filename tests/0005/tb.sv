// Simulator limitation (Verilator 5.020): does not reset an automatic function's local queue between calls
// made from a loop. The translation adds an explicit queue.delete(); the logic is unchanged.
//@translation-of function automatic string smallest_01_multiple 20624da62cab

module tb;
  //@page function automatic longint unsigned by_enumeration

  function automatic string smallest_01_multiple(int x);
    int    parent[];               // remainder we came from
    bit    digit[];                // digit appended to reach this remainder
    bit    visited[];
    int    queue[$];
    int    r, nr, start;
    string result = "";

    queue.delete();                // simulator workaround, see the header
    parent  = new[x];
    digit   = new[x];
    visited = new[x];

    start = 1 % x;                 // the number "1"
    visited[start] = 1;
    parent[start]  = -1;
    digit[start]   = 1;
    queue.push_back(start);

    while (!visited[0]) begin        // stop once remainder 0 is reached
      r = queue.pop_front();
      for (int d = 0; d <= 1; d++) begin   // 0 first -> smaller numbers first
        nr = (r * 10 + d) % x;
        if (!visited[nr]) begin
          visited[nr] = 1;
          parent[nr]  = r;
          digit[nr]   = d;
          queue.push_back(nr);
        end
      end
    end

    // Walk back from remainder 0 to the start, prepending the digits.
    for (r = 0; r != -1; r = parent[r])
      result = {(digit[r] ? "1" : "0"), result};
    return result;
  endfunction

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
