// Question 0032: the page's river_safe against the rule in words on all sixteen states, and
// river_plan replayed crossing by crossing: every crossing legal, every state safe, seven
// crossings, everyone across at the end.
module tb;
  //@page function automatic int river_plan

  int errors = 0;

  function automatic bit safe_by_words(int s);
    bit f = s & 1, w = (s >> 1) & 1, g = (s >> 2) & 1, c = (s >> 3) & 1;
    bit eaten = (w == g && g != f) || (g == c && g != f);
    return !eaten;
  endfunction

  initial begin
    string plan;
    int n, s, i, item, nxt, crossings;
    bit forward;

    for (s = 0; s < 16; s++)
      if (river_safe(s) != safe_by_words(s)) begin
        errors++;
        $display("state %04b: safe=%0d, expected %0d", s, river_safe(s), safe_by_words(s));
      end

    n = river_plan(plan);
    $display("plan: %s (%0d crossings)", plan, n);
    if (n != 7) begin errors++; $display("expected 7 crossings, got %0d", n); end
    if (!(plan == "G> -< W> G< C> -< G>" || plan == "G> -< C> G< W> -< G>")) begin
      errors++;
      $display("unexpected plan '%s'", plan);
    end

    // replay
    s = 0; i = 0; crossings = 0;
    while (i < plan.len()) begin
      case (plan[i])
        "-": item = 0;
        "W": item = WOLF;
        "G": item = GOAT;
        "C": item = CABBAGE;
        default: begin errors++; $display("bad letter at %0d", i); item = 0; end
      endcase
      forward = (s & FARMER) == 0;
      if (plan[i + 1] != (forward ? ">" : "<")) begin errors++; $display("bad direction at %0d", i + 1); end
      if (item != 0 && ((s & item) != 0) != ((s & FARMER) != 0)) begin errors++; $display("item on the other bank at %0d", i); end
      nxt = s ^ FARMER ^ item;
      if (!river_safe(nxt)) begin errors++; $display("unsafe state %04b after crossing %0d", nxt, crossings + 1); end
      s = nxt; crossings++;
      i += 3;
    end
    if (s != EVERYONE) begin errors++; $display("the plan ends at %04b", s); end
    if (crossings != n) begin errors++; $display("replayed %0d crossings, function says %0d", crossings, n); end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
