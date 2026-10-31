// Question 0060: the page's first_round against the page's Python numbers (an exact
// recomputation of the three parts' closed forms here), and best_wand in the six cases
// of parts a to d.
module tb;
  //@page function automatic real duel_first

  int errors = 0;

  function automatic void check(int me, real r0, real r1, real chance, real wand_want);
    real rivals[2], q, got;
    rivals[0] = r0; rivals[1] = r1;
    got = best_wand(me, rivals, q);
    if (got - chance > 1e-6 || chance - got > 1e-6 || q - wand_want > 1e-6 || wand_want - q > 1e-6) begin
      errors++;
      $display("me %0d rivals %f %f: %f at %f, want %f at %f", me, r0, r1, got, q, chance, wand_want);
    end
  endfunction

  initial begin
    real p[3], win[3];
    p = '{0.6 - 1e-9, 0.6, 0.8};
    first_round(p, win);
    if (win[0] - 513.0 / 805.0 > 1e-6 || 513.0 / 805.0 - win[0] > 1e-6) begin errors++; $display("part a: %f", win[0]); end
    p = '{1.0, 0.6, 0.8};
    first_round(p, win);
    if (win[0] - 0.4 > 1e-9 || 0.4 - win[0] > 1e-9) begin errors++; $display("sniper: %f", win[0]); end
    check(1, 0.6, 0.8, 513.0 / 805.0, 0.6);
    check(2, 0.6, 0.8, 513.0 / 805.0, 0.6);
    check(3, 0.6, 0.8, 13101.0 / 20125.0, 0.6);
    check(1, 0.8, 0.4, 0.6, 1.0);
    check(2, 0.8, 0.4, 233.0 / 550.0, 0.4);
    check(3, 0.8, 0.4, 1187.0 / 2750.0, 0.4);
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
