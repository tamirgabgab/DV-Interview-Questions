module tb;
  typedef string labels_t[3];
  string content[3];                      // what is really inside each box

  // Provided API from the question
  function automatic string draw(int i);
    if (content[i] == "MIXED") return ($urandom_range(0, 1) == 1) ? "RED" : "BLACK";
    return content[i];
  endfunction

  //@page function automatic labels_t fix_labels_simple
  //@page function automatic void fix_labels

  initial begin
    string   names[3] = '{"RED", "BLACK", "MIXED"};
    int      perm[6][3] = '{'{0,1,2}, '{0,2,1}, '{1,0,2}, '{1,2,0}, '{2,0,1}, '{2,1,0}};
    labels_t labels, expected, got;
    int      cases = 0, errors = 0;
    bit      all_wrong;

    foreach (perm[p]) foreach (perm[c]) begin
      all_wrong = 1;
      for (int i = 0; i < 3; i++) if (perm[p][i] == perm[c][i]) all_wrong = 0;
      if (!all_wrong) continue;
      cases++;
      for (int i = 0; i < 3; i++) begin
        labels[i]   = names[perm[p][i]];
        expected[i] = names[perm[c][i]];
        content[i]  = expected[i];
      end
      repeat (5) begin
        got = fix_labels_simple(labels);
        if (got != expected) errors++;
        got = labels;
        fix_labels(got);
        if (got != expected) errors++;
      end
    end
    if (cases == 12 && errors == 0) $display("PASS cases=%0d", cases);
    else $display("FAIL cases=%0d errors=%0d", cases, errors);
    $finish;
  end
endmodule
