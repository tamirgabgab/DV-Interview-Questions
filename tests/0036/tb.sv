// Question 0036: the page's lfsr_next and lfsr_period: the two example periods (15 and 6),
// the sequence of the maximal polynomial visits every non-zero state once, zero is a fixed
// point, and the period from 0001 of every x^4 + ... + 1 matches the page table.
module tb;
  //@page function automatic int lfsr_next

  int errors = 0;

  initial begin
    int expected[8] = '{4, 15, 6, 15, 7, 6, 7, 5};       // masks 0001, 0011, 0101, 1001, 0111, 1011, 1101, 1111
    int masks[8]    = '{4'b0001, 4'b0011, 4'b0101, 4'b1001, 4'b0111, 4'b1011, 4'b1101, 4'b1111};
    bit seen[16];
    int s;

    if (lfsr_period(4'b0011, 4) != 15) begin errors++; $display("x^4+x^3+1 period %0d", lfsr_period(4'b0011, 4)); end
    if (lfsr_period(4'b0101, 4) != 6) begin errors++; $display("x^4+x^2+1 period %0d", lfsr_period(4'b0101, 4)); end
    if (lfsr_next(4'b0000, 4'b0011, 4) != 0) begin errors++; $display("zero is not a fixed point"); end

    s = 1;
    for (int k = 0; k < 15; k++) begin
      if (s == 0 || seen[s]) begin errors++; $display("state %04b repeated or zero at step %0d", s, k); end
      seen[s] = 1;
      s = lfsr_next(s, 4'b0011, 4);
    end
    if (s != 1) begin errors++; $display("did not return to 0001 after 15 steps"); end

    foreach (masks[i])
      if (lfsr_period(masks[i], 4) != expected[i]) begin
        errors++; $display("mask %04b: period %0d, expected %0d", masks[i], lfsr_period(masks[i], 4), expected[i]);
      end

    // a maximal 8-bit polynomial: x^8 + x^6 + x^5 + x^4 + 1 (mask bits 0, 2, 3, 4)
    if (lfsr_period(8'b00011101, 8) != 255) begin errors++; $display("8-bit period %0d", lfsr_period(8'b00011101, 8)); end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
