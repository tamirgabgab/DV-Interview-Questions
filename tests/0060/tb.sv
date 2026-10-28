// Question 0060: the page's longest_ones and longest_same against every window, on the
// page's examples and the self-checks, and on random vectors and bus strings of up to 14
// cells with k up to 4.
module tb;
  //@page function automatic int longest_ones
  //@page function automatic int longest_same

  int errors = 0;

  // every window: the longest with at most k zeros
  function automatic int brute_ones(bit bits[], int k);
    int best = 0, zeros;
    for (int i = 0; i < bits.size(); i++) begin
      zeros = 0;
      for (int j = i; j < bits.size(); j++) begin
        if (!bits[j]) zeros++;
        if (zeros <= k && j - i + 1 > best) best = j - i + 1;
      end
    end
    return best;
  endfunction

  // every window: the longest whose length minus its most frequent value is at most k
  function automatic int brute_same(string s, int k);
    int best = 0, cnt[byte], most;
    for (int i = 0; i < s.len(); i++) begin
      cnt.delete();
      for (int j = i; j < s.len(); j++) begin
        cnt[s[j]]++;
        most = 0;
        foreach (cnt[c]) if (cnt[c] > most) most = cnt[c];
        if (j - i + 1 - most <= k && j - i + 1 > best) best = j - i + 1;
      end
    end
    return best;
  endfunction

  initial begin
    bit bits[];
    string s;
    int n;
    bits = '{1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0};
    if (longest_ones(bits, 2) != 6) begin errors++; $display("page example: %0d", longest_ones(bits, 2)); end
    if (longest_ones(bits, 0) != 4 || longest_ones(bits, 3) != 10 || longest_ones(bits, 11) != 11) begin errors++; $display("k = 0, 3, 11"); end
    bits = '{1, 0, 1, 1, 0, 1, 0, 1, 1, 1};
    if (longest_ones(bits, 1) != 5) begin errors++; $display("self-check a: %0d", longest_ones(bits, 1)); end
    if (longest_same("AAABBCBABA", 2) != 6) begin errors++; $display("bus example: %0d", longest_same("AAABBCBABA", 2)); end
    if (longest_same("AAABBCBABA", 0) != 3 || longest_same("AAABBCBABA", 1) != 4) begin errors++; $display("bus k = 0, 1"); end
    if (longest_same("ABAACAAB", 2) != 7 || longest_same("ABAACAAB", 1) != 5) begin errors++; $display("self-check b"); end
    bits = new[0];
    if (longest_ones(bits, 1) != 0 || longest_same("", 1) != 0) begin errors++; $display("empty"); end
    for (int r = 0; r < 300; r++) begin
      n = $urandom_range(0, 14);
      bits = new[n];
      foreach (bits[i]) bits[i] = ($urandom_range(0, 9) < 6);
      s = "";
      for (int i = 0; i < n; i++) s = {s, $sformatf("%c", "A" + $urandom_range(0, 2))};
      for (int k = 0; k <= 4; k++) begin
        if (longest_ones(bits, k) != brute_ones(bits, k)) begin errors++; $display("run %0d k %0d: %0d vs %0d", r, k, longest_ones(bits, k), brute_ones(bits, k)); end
        if (longest_same(s, k) != brute_same(s, k)) begin errors++; $display("bus run %0d k %0d (%s): %0d vs %0d", r, k, s, longest_same(s, k), brute_same(s, k)); end
      end
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
