// Question 0052: the page's corr, expected_tosses and p_first on the page's numbers (6, 4,
// 14, 18, 30; a 1/2 race and Penney's 7/8), and a simulation with $urandom: the mean
// number of tosses and the share of races won within a few standard errors of the page.
module tb;
  //@page function automatic longint corr
  //@page function automatic real p_first

  int errors = 0;

  function automatic string toss();
    return ($urandom & 1) ? "H" : "T";
  endfunction

  // tosses until p appears (the last len(p) tosses kept in a string)
  function automatic int wait_for(string p);
    string seen = "";
    int n = 0;
    while (1) begin
      seen = {seen, toss()};
      if (seen.len() > p.len()) seen = seen.substr(1, seen.len() - 1);
      n++;
      if (seen == p) return n;
    end
  endfunction

  // 1 when a appears before b
  function automatic int race(string a, string b);
    string seen = "";
    int keep = a.len() > b.len() ? a.len() : b.len();
    while (1) begin
      seen = {seen, toss()};
      if (seen.len() > keep) seen = seen.substr(1, seen.len() - 1);
      if (seen.len() >= a.len() && seen.substr(seen.len() - a.len(), seen.len() - 1) == a) return 1;
      if (seen.len() >= b.len() && seen.substr(seen.len() - b.len(), seen.len() - 1) == b) return 0;
    end
  endfunction

  task automatic check_mean(string p, int runs);
    real sum = 0.0, sq = 0.0, m, sd;
    int t;
    for (int r = 0; r < runs; r++) begin t = wait_for(p); sum += t; sq += real'(t) * t; end
    m = sum / runs; sd = $sqrt(sq / runs - m * m);
    if (m < expected_tosses(p) - 4.0 * sd / $sqrt(runs) || m > expected_tosses(p) + 4.0 * sd / $sqrt(runs)) begin
      errors++; $display("%s: simulated %f, expected %0d", p, m, expected_tosses(p));
    end
  endtask

  task automatic check_race(string a, string b, int runs);
    int wins = 0;
    real p = p_first(a, b), share;
    for (int r = 0; r < runs; r++) wins += race(a, b);
    share = real'(wins) / runs;
    if (share < p - 4.0 * $sqrt(p * (1 - p) / runs) || share > p + 4.0 * $sqrt(p * (1 - p) / runs)) begin
      errors++; $display("%s vs %s: simulated %f, page %f", a, b, share, p);
    end
  endtask

  initial begin
    void'($urandom(52));
    if (expected_tosses("HH") != 6 || expected_tosses("HT") != 4 || expected_tosses("HHH") != 14) begin
      errors++; $display("expected_tosses wrong");
    end
    if (expected_tosses("HTHH") != 18 || expected_tosses("HHHH") != 30) begin errors++; $display("1011 / 1111 wrong"); end
    if (p_first("HT", "HH") != 0.5 || p_first("THH", "HHH") != 0.875) begin errors++; $display("p_first wrong"); end
    check_mean("HH", 20000);
    check_mean("HT", 20000);
    check_mean("HTH", 20000);
    check_race("HT", "HH", 20000);
    check_race("THH", "HHH", 20000);
    check_race("HHT", "HTT", 20000);
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
