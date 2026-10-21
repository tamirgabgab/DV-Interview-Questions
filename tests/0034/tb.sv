// Question 0034: the page's Gray conversions (inverse of each other, one bit per step,
// also on the wrap) and the full / empty rules against the true occupancy, exhaustively
// for pointers of 3, 5 and 7 bits.
module tb;
  //@page function automatic int bin2gray
  //@page function automatic bit fifo_empty

  int errors = 0;

  function automatic int popcount(int x);
    int n = 0;
    for (int i = 0; i < 32; i++) n += (x >> i) & 1;
    return n;
  endfunction

  initial begin
    int widths[3] = '{3, 5, 7};
    int bits, size, half, g, occupancy;
    bit e, f;
    // Declarations inside the loops would be initialised once (a static initial block),
    // so every per-iteration value is assigned, not declared with an initialiser.
    foreach (widths[k]) begin
      bits = widths[k];
      size = 1 << bits;
      half = size / 2;                           // FIFO entries: one wrap bit on top
      for (int b = 0; b < size; b++) begin
        g = bin2gray(b);
        if (gray2bin(g, bits) != b) begin errors++; $display("bits %0d: gray2bin(bin2gray(%0d)) != %0d", bits, b, b); end
        if (popcount(g ^ bin2gray((b + 1) % size)) != 1) begin
          errors++; $display("bits %0d: step %0d -> %0d changes %0d bits", bits, b, (b + 1) % size, popcount(g ^ bin2gray((b + 1) % size)));
        end
      end
      for (int w = 0; w < size; w++)
        for (int r = 0; r < size; r++) begin
          occupancy = (w - r + size) % size;
          e = fifo_empty(bin2gray(w), bin2gray(r));
          f = fifo_full(bin2gray(w), bin2gray(r), bits);
          if (e != (occupancy == 0)) begin errors++; $display("bits %0d: empty wrong for w=%0d r=%0d", bits, w, r); end
          if (f != (occupancy == half)) begin errors++; $display("bits %0d: full wrong for w=%0d r=%0d", bits, w, r); end
        end
    end
    // the page example: w = 23, r = 7 with 5-bit pointers is full
    if (!fifo_full(bin2gray(23), bin2gray(7), 5) || fifo_empty(bin2gray(23), bin2gray(7))) begin
      errors++; $display("page example failed");
    end
    if (bin2gray(7) != 4 || bin2gray(8) != 12) begin errors++; $display("7 -> 0100, 8 -> 1100 expected"); end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
