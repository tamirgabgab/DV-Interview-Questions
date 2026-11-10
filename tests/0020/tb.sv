//@flags --assert --timing
// Question 0020: the page's completion_splits against a subset reference, and the page's
// cpl_checker (the scoreboard follow-up) on random legal splits (no assertion fails, the
// covergroup reaches 100 %) and on five bugs, each failing its own assertion once.
//@page module cpl_checker

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

  // The checker's harness: a request, then its completions one per clock, driven on the
  // falling edge; `bad` names a completion whose Byte Count / Lower Address get an offset.
  logic clk = 0, rst_n = 0, start = 0, cpl = 0;
  logic [63:0] c_addr;
  logic [12:0] c_len;
  logic [9:0]  c_ldw;
  logic [11:0] c_bc;
  logic [6:0]  c_la;
  always #5 clk = ~clk;
  cpl_checker #(.MPS(256), .RCB(64)) chk (.clk, .rst_n, .start, .addr(c_addr), .len(c_len), .cpl,
                                          .length_dw(c_ldw), .byte_count(c_bc), .lower_addr(c_la));

  task automatic send(longint unsigned a, int l, int sizes[$], int bad = -1, int bc_off = 0, int la_off = 0);
    longint unsigned pos = a;
    int left = l;
    @(negedge clk); start = 1; c_addr = a; c_len = 13'(l);
    @(negedge clk); start = 0;
    foreach (sizes[i]) begin
      cpl = 1; c_ldw = 10'(sizes[i] / 4); c_bc = 12'(left); c_la = 7'(pos);   // 1024 DW and 4096 B encode as 0
      if (i == bad) begin c_bc += 12'(bc_off); c_la += 7'(la_off); end
      @(negedge clk);
      pos += sizes[i]; left -= sizes[i];
    end
    cpl = 0;
  endtask

  // a legal split of any length: a random allowed end at every step
  function automatic void random_split(longint unsigned a, int l, int mps, int rcb, ref int sizes[$]);
    longint unsigned pos = a, e = a + l, b;
    longint unsigned cuts[$];
    sizes.delete();
    while (pos < e) begin
      cuts.delete();
      if (pos + mps >= e) cuts.push_back(e);
      for (b = (pos / rcb + 1) * rcb; b < e && b <= pos + mps; b += rcb) cuts.push_back(b);
      b = cuts[$urandom_range(cuts.size() - 1, 0)];
      sizes.push_back(int'(b - pos));
      pos = b;
    end
  endfunction

  function automatic bit fails_are(int s, int bc, int la, int cut, int done);
    return chk.f_size == s && chk.f_bc == bc && chk.f_la == la && chk.f_cut == cut && chk.f_done == done;
  endfunction

  task automatic check_checker(ref int errors);
    int sizes[$], all[$][$];
    int l;
    longint unsigned a;
    int lens[9] = '{16, 128, 256, 300, 512, 1024, 2048, 3072, 4096};
    #12 rst_n = 1;
    // legal traffic: the page's splits for short requests, random walks up to 4 KB
    repeat (400) begin
      l = lens[$urandom_range(8, 0)];
      a = 4 * $urandom_range(1 << 18, 0);
      if (l <= 512) begin
        completion_splits(a, l, 256, 64, all);
        sizes = all[$urandom_range(all.size() - 1, 0)];
      end else random_split(a, l, 256, 64, sizes);
      send(a, l, sizes);
    end
    @(negedge clk);
    if (!fails_are(0, 0, 0, 0, 0)) begin errors++; $display("checker fails on legal splits"); end
    if (chk.cov.get_inst_coverage() != 100.0) begin errors++; $display("coverage %f", chk.cov.get_inst_coverage()); end
    // five bugs, one assertion each
    send(64'h1010, 256, '{128, 128});                           // a cut at 0x1090
    if (!fails_are(0, 0, 0, 1, 0)) begin errors++; $display("bug: cut off the RCB grid"); end
    send(64'h1000, 512, '{512});                                // above MPS
    if (!fails_are(1, 0, 0, 1, 0)) begin errors++; $display("bug: above MPS"); end
    send(64'h1010, 256, '{48, 64, 64, 64, 16}, 2, 4, 0);        // Byte Count off by 4
    if (!fails_are(1, 1, 0, 1, 0)) begin errors++; $display("bug: Byte Count"); end
    send(64'h1010, 256, '{48, 64, 64, 64, 16}, 1, 0, 4);        // Lower Address off by 4
    if (!fails_are(1, 1, 1, 1, 0)) begin errors++; $display("bug: Lower Address"); end
    send(64'h1010, 256, '{48, 64});                             // the rest never comes
    send(64'h1000, 4096, '{256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256});
    if (!fails_are(1, 1, 1, 1, 1)) begin errors++; $display("bug: a missing completion"); end
  endtask

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

    check_checker(errors);

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
