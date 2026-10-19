module tb;
  //@page function automatic void completion_splits(

  int errors = 0;

  // Independent reference: every subset of the RCB boundaries inside the request (one bit
  // per boundary), kept when no completion is larger than MPS. Returns the splits as
  // strings "48+64+144" so sets can be compared without caring about the order.
  function automatic void reference(longint unsigned addr, int len, int mps, int rcb, ref string found[$]);
    longint unsigned bounds[$];
    longint unsigned b, pos, cut;
    int size;
    bit ok;
    string s;
    found.delete();
    b = (addr / rcb + 1) * rcb;
    while (b < addr + len) begin
      bounds.push_back(b);
      b += rcb;
    end
    for (int mask = 0; mask < (1 << bounds.size()); mask++) begin
      pos = addr;
      ok = 1;
      s = "";
      for (int i = 0; i <= bounds.size(); i++) begin
        if (i < bounds.size() && !mask[i]) continue;
        cut = (i < bounds.size()) ? bounds[i] : addr + len;
        size = int'(cut - pos);
        if (size > mps) ok = 0;
        s = {s, (s == "") ? "" : "+", $sformatf("%0d", size)};
        pos = cut;
      end
      if (ok) found.push_back(s);
    end
  endfunction

  function automatic string joined(int sizes[$]);
    string s = "";
    foreach (sizes[i]) s = {s, (i == 0) ? "" : "+", $sformatf("%0d", sizes[i])};
    return s;
  endfunction

  // Every cut between two completions on an RCB boundary, nothing above MPS, sum = len
  function automatic bit split_ok(longint unsigned addr, int len, int mps, int rcb, int split[$]);
    longint unsigned pos = addr;
    int total = 0;
    foreach (split[i]) begin
      if (split[i] <= 0 || split[i] > mps) return 0;
      total += split[i];
      pos += split[i];
      if (i < split.size() - 1 && pos % rcb != 0) return 0;
    end
    return total == len;
  endfunction

  initial begin
    int splits[$][$];
    string got[$], want[$];
    longint unsigned addr;
    int len, mps, rcb, c;
    int lens[13] = '{4, 8, 16, 32, 64, 96, 128, 192, 256, 384, 512, 768, 1024};

    // the page example: 16 splits, greedy first, every boundary cut last
    completion_splits(64'h1010, 256, 256, 64, splits);
    if (splits.size() != 16) errors++;
    if (joined(splits[0]) != "256" || joined(splits[1]) != "240+16" || joined(splits[2]) != "176+80") errors++;
    if (joined(splits[$]) != "48+64+64+64+16") errors++;
    completion_splits(64'h1010, 256, 128, 64, splits);
    if (splits.size() != 8) errors++;
    completion_splits(64'h1010, 256, 128, 128, splits);
    if (splits.size() != 1 || joined(splits[0]) != "112+128+16") errors++;
    completion_splits(64'h1000, 256, 128, 64, splits);
    if (splits.size() != 5 || joined(splits[0]) != "128+128") errors++;

    // random requests inside one 4 KB page against the subset reference
    repeat (400) begin
      rcb = $urandom_range(1, 0) ? 64 : 128;
      mps = 128 << $urandom_range(3, 0);
      if (mps < rcb) mps = rcb;
      len = lens[$urandom_range(12, 0)];
      addr = 4 * $urandom_range((4096 - len) / 4, 0);
      completion_splits(addr, len, mps, rcb, splits);
      got.delete();
      foreach (splits[i]) begin
        if (!split_ok(addr, len, mps, rcb, splits[i])) errors++;
        got.push_back(joined(splits[i]));
      end
      reference(addr, len, mps, rcb, want);
      got.sort();
      want.sort();
      if (got != want) begin
        errors++;
        $display("mismatch addr=%0h len=%0d mps=%0d rcb=%0d: %0d vs %0d", addr, len, mps, rcb, got.size(), want.size());
      end
      c = int'((addr + len - 1) / rcb - addr / rcb);
      if (splits[$].size() != c + 1) errors++;                 // a cut on every boundary
      if (mps >= len && splits.size() != (1 << c)) errors++;   // 2^c without the MPS limit
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
