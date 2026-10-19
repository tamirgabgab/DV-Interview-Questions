module tb;
  //@page typedef bit [11:0] seq_t
  //@page class dll_transmitter;
  //@page class dll_transmitter_with_replay

  int errors = 0, checks = 0;

  function automatic void expect_eq(string what, int got, int want);
    checks++;
    if (got !== want) begin
      $display("FAIL: %s: got %0d, expected %0d", what, got, want);
      errors++;
    end
  endfunction

  function automatic string seqs(ref pcie_tlp q[$]);
    string s = "";
    foreach (q[i]) s = {s, i ? "," : "", $sformatf("%0d", q[i].seq)};
    return s;
  endfunction

  function automatic void expect_seqs(string what, string got, string want);
    checks++;
    if (got != want) begin
      $display("FAIL: %s: got [%s], expected [%s]", what, got, want);
      errors++;
    end
  endfunction

  function automatic void send(dll_transmitter tx, int n);
    for (int i = 0; i < n; i++) begin
      pcie_tlp t = new(32'hA0 + i);
      tx.send_tlp(t);
    end
  endfunction

  function automatic void pass_tlps(dll_transmitter tx, dll_receiver rx, int n = -1);
    if (n < 0) n = tx.tx_tlps.size();
    repeat (n) rx.receive_tlp(tx.tx_tlps.pop_front());
  endfunction

  function automatic void pass_dllps(dll_transmitter tx, dll_receiver rx);
    while (rx.tx_dllps.size() > 0) tx.receive_dllp(rx.tx_dllps.pop_front());
  endfunction

  function automatic void expect_dllp(string what, pcie_dllp d, dllp_kind_e kind, int seq);
    expect_eq({what, ": kind"}, d.kind, kind);
    expect_eq({what, ": seq"}, d.seq, seq);
  endfunction

  // ---------------------------------------------------------------- the examples of the reference

  function automatic void example_1();
    dll_transmitter_with_replay tx = new(3);
    dll_receiver_with_nak       rx = new(3);
    expect_eq("1: NTS", tx.next_transmit_seq, 3);
    expect_eq("1: ACKD_SEQ", tx.ackd_seq, 2);
    send(tx, 5);
    expect_eq("1: NTS after 5", tx.next_transmit_seq, 8);
    expect_seqs("1: retry", seqs(tx.retry_buffer), "3,4,5,6,7");
    rx.ack_threshold = 99;
    pass_tlps(tx, rx, 3);
    expect_eq("1: NRS", rx.next_rcv_seq, 6);
    rx.flush_ack();
    expect_eq("1: one Ack", rx.tx_dllps.size(), 1);
    expect_dllp("1: Ack 5", rx.tx_dllps[0], DLLP_ACK, 5);
    pass_dllps(tx, rx);
    expect_seqs("1: retry after Ack 5", seqs(tx.retry_buffer), "6,7");
    expect_eq("1: ACKD_SEQ 5", tx.ackd_seq, 5);
  endfunction

  function automatic void example_2();
    dll_transmitter_with_replay tx = new(4094);
    pcie_dllp ack = new(DLLP_ACK, 1);
    send(tx, 5);
    expect_eq("2: NTS wrapped", tx.next_transmit_seq, 3);
    expect_seqs("2: retry", seqs(tx.retry_buffer), "4094,4095,0,1,2");
    tx.receive_dllp(ack);
    expect_seqs("2: retry after Ack 1", seqs(tx.retry_buffer), "2");
    expect_eq("2: ACKD_SEQ", tx.ackd_seq, 1);
  endfunction

  function automatic void example_3();
    dll_transmitter_with_replay tx = new(4094);
    dll_receiver_with_nak       rx = new(4094);
    pcie_tlp bad;
    rx.ack_threshold = 99;
    send(tx, 5);
    pass_tlps(tx, rx, 1);
    expect_eq("3: NRS 4095", rx.next_rcv_seq, 4095);
    bad = tx.tx_tlps.pop_front();
    bad.crc_ok = 0;
    rx.receive_tlp(bad);
    expect_eq("3: one Nak", rx.tx_dllps.size(), 1);
    expect_dllp("3: Nak 4094", rx.tx_dllps[0], DLLP_NAK, 4094);
    expect_eq("3: NAK_SCHEDULED", rx.nak_scheduled, 1);
    pass_tlps(tx, rx, 2);
    expect_eq("3: still one Nak", rx.tx_dllps.size(), 1);
    expect_eq("3: NRS unchanged", rx.next_rcv_seq, 4095);
    expect_eq("3: bad TLPs", rx.bad_tlp_count, 3);
    pass_dllps(tx, rx);
    expect_seqs("3: retry after Nak", seqs(tx.retry_buffer), "4095,0,1,2");
    expect_eq("3: ACKD_SEQ", tx.ackd_seq, 4094);
    expect_seqs("3: link: original 2 then the replay", seqs(tx.tx_tlps), "2,4095,0,1,2");
    expect_eq("3: original not a replay", tx.tx_tlps[0].is_replay, 0);
    expect_eq("3: replay flag", tx.tx_tlps[1].is_replay, 1);
    pass_tlps(tx, rx);
    expect_eq("3: NRS 3", rx.next_rcv_seq, 3);
    expect_eq("3: NAK_SCHEDULED off", rx.nak_scheduled, 0);
    expect_seqs("3: delivered", seqs(rx.received_tlps), "4094,4095,0,1,2");
  endfunction

  function automatic void example_4();
    dll_transmitter_with_replay tx = new(10);
    dll_receiver_with_nak       rx = new(10);
    pcie_dllp ack;
    rx.ack_threshold = 99;
    send(tx, 4);
    pass_tlps(tx, rx, 3);
    rx.flush_ack();
    ack = rx.tx_dllps.pop_front();
    expect_dllp("4: Ack 12", ack, DLLP_ACK, 12);
    ack.crc_ok = 0;
    tx.receive_dllp(ack);
    expect_seqs("4: retry kept", seqs(tx.retry_buffer), "10,11,12,13");
    expect_eq("4: ACKD_SEQ kept", tx.ackd_seq, 9);
    expect_eq("4: bad DLLP counted", tx.bad_dllp_count, 1);
    pass_tlps(tx, rx);
    rx.flush_ack();
    pass_dllps(tx, rx);
    expect_eq("4: retry empty", tx.retry_buffer.size(), 0);
    expect_eq("4: ACKD_SEQ 13", tx.ackd_seq, 13);
  endfunction

  function automatic void example_5();
    dll_transmitter_with_replay tx = new(10);
    dll_receiver_with_nak       rx = new(10);
    pcie_tlp dup = new(32'h11, 11);
    rx.ack_threshold = 99;
    send(tx, 3);
    pass_tlps(tx, rx);
    rx.receive_tlp(dup);
    expect_seqs("5: delivered once", seqs(rx.received_tlps), "10,11,12");
    expect_eq("5: NRS", rx.next_rcv_seq, 13);
    expect_eq("5: one DLLP", rx.tx_dllps.size(), 1);
    expect_dllp("5: Ack 12", rx.tx_dllps[0], DLLP_ACK, 12);
    expect_eq("5: duplicate counted", rx.duplicate_count, 1);
  endfunction

  function automatic void illegal_dllps();
    dll_transmitter_with_replay tx = new(100);
    pcie_dllp d;
    send(tx, 4);
    d = new(DLLP_NAK, 101, 0);
    tx.receive_dllp(d);
    expect_seqs("illegal: corrupt Nak ignored", seqs(tx.retry_buffer), "100,101,102,103");
    expect_eq("illegal: bad DLLP", tx.bad_dllp_count, 1);
    expect_eq("illegal: no replay", tx.tx_tlps.size(), 4);
    d = new(DLLP_ACK, 7);
    tx.receive_dllp(d);
    expect_seqs("illegal: unknown Ack ignored", seqs(tx.retry_buffer), "100,101,102,103");
    expect_eq("illegal: protocol error", tx.protocol_error_count, 1);
    d = new(DLLP_ACK, 99);
    tx.receive_dllp(d);
    expect_eq("illegal: Ack for ACKD_SEQ is legal", tx.protocol_error_count, 1);
    d = new(DLLP_NAK, 99);
    tx.receive_dllp(d);
    expect_eq("illegal: Nak for ACKD_SEQ replays", tx.tx_tlps.size(), 8);
    expect_eq("illegal: replay counted", tx.replay_count, 1);
    d = new(DLLP_NAK, 102);
    tx.receive_dllp(d);
    expect_seqs("illegal: Nak 102 purges", seqs(tx.retry_buffer), "103");
    expect_eq("illegal: ACKD_SEQ 102", tx.ackd_seq, 102);
    expect_eq("illegal: replay of 103 only", tx.tx_tlps.size(), 9);
    expect_eq("illegal: replayed seq", tx.tx_tlps[8].seq, 103);
  endfunction

  function automatic void duplicate_window();
    dll_receiver_with_nak rx = new(0);
    int expected[7] = '{0, 1, 2047, 2048, 2049, 4095, 1234};
    int bad = 0;
    foreach (expected[i]) begin
      rx.next_rcv_seq = seq_t'(expected[i]);
      for (int received = 0; received < 4096; received++) begin
        int behind = (expected[i] - received + 4096) % 4096;
        if (rx.is_duplicate(seq_t'(received)) != (behind > 0 && behind <= 2048)) bad++;
      end
    end
    expect_eq("duplicate window mismatches", bad, 0);
  endfunction

  function automatic void clean_copy();
    dll_transmitter_with_replay tx = new();
    pcie_tlp t = new(32'hAB);
    pcie_dllp nak = new(DLLP_NAK, 4095);
    tx.send_tlp(t);
    tx.tx_tlps[0].crc_ok = 0; tx.tx_tlps[0].seq = 77; tx.tx_tlps[0].payload = 0;
    expect_eq("clean: stored crc_ok", tx.retry_buffer[0].crc_ok, 1);
    expect_eq("clean: stored seq", tx.retry_buffer[0].seq, 0);
    expect_eq("clean: stored payload", tx.retry_buffer[0].payload, 32'hAB);
    tx.receive_dllp(nak);
    expect_eq("clean: replay crc_ok", tx.tx_tlps[1].crc_ok, 1);
    expect_eq("clean: replay flag", tx.tx_tlps[1].is_replay, 1);
  endfunction

  function automatic void ack_sizes();
    dll_transmitter_with_replay tx = new();
    dll_receiver_with_nak       rx = new();
    int seen[5] = '{0, 0, 0, 0, 0};
    int last = 0;
    for (int i = 0; i < 400; i++) begin
      send(tx, 1);
      pass_tlps(tx, rx);
      foreach (rx.tx_dllps[j]) begin
        seen[rx.received_tlps.size() - last]++;
        last = rx.received_tlps.size();
      end
      pass_dllps(tx, rx);
    end
    for (int k = 1; k <= 4; k++)
      if (seen[k] == 0) begin
        $display("FAIL: no Ack covering %0d TLPs in 400", k); errors++;
      end
    expect_eq("ack sizes: never 0 or more than 4", seen[0], 0);
  endfunction

  // ---------------------------------------------------------------- random lossy traffic

  int delivered_total = 0, replays_total = 0, dups_total = 0, proto_total = 0, bad_dllp_total = 0,
      corrupt_tlp_total = 0, drop_tlp_total = 0, timeouts_total = 0;

  function automatic void lossy_traffic(int start, int steps);
    dll_transmitter_with_replay tx = new(seq_t'(start));
    dll_receiver_with_nak       rx = new(seq_t'(start));
    int sent[$];
    int payload = 0, illegal = 0, corrupt_dllp = 0, r, q;
    pcie_tlp  t;
    pcie_dllp d;
    for (int step = 0; step < steps; step++) begin
      r = $urandom_range(0, 99);
      if (r < 35) begin
        if (tx.retry_buffer.size() < 16) begin
          t = new(payload);
          tx.send_tlp(t);
          sent.push_back(payload++);
        end
      end else if (r < 65) begin
        if (tx.tx_tlps.size() > 0) begin
          t = tx.tx_tlps.pop_front();
          q = $urandom_range(0, 99);
          if (q < 3) begin t.crc_ok = 0; corrupt_tlp_total++; end
          if (q >= 3 && q < 5) drop_tlp_total++;
          else rx.receive_tlp(t);
        end
      end else if (r < 85) begin
        if (rx.tx_dllps.size() > 0) begin
          d = rx.tx_dllps.pop_front();
          q = $urandom_range(0, 99);
          if (q < 3) begin d.crc_ok = 0; corrupt_dllp++; end
          else if (q < 5) continue;
          else if (q < 7) begin d.seq = tx.ackd_seq + 12'd2048; illegal++; end
          tx.receive_dllp(d);
        end
      end else if (r < 92) begin
        rx.flush_ack();
      end else if (tx.tx_tlps.size() == 0 && rx.tx_dllps.size() == 0 && tx.retry_buffer.size() > 0) begin
        tx.on_replay_timeout();
        timeouts_total++;
      end
      if (!bookkeeping_ok(tx, rx, sent)) begin
        $display("FAIL: bookkeeping at step %0d (start %0d)", step, start);
        errors++;
        return;
      end
    end
    for (int k = 0; k < 200 && tx.retry_buffer.size() > 0; k++) begin
      while (tx.tx_tlps.size() > 0) rx.receive_tlp(tx.tx_tlps.pop_front());
      rx.flush_ack();
      while (rx.tx_dllps.size() > 0) tx.receive_dllp(rx.tx_dllps.pop_front());
      if (tx.retry_buffer.size() > 0) tx.on_replay_timeout();
    end
    expect_eq($sformatf("lossy (start %0d): retry buffer drained", start), tx.retry_buffer.size(), 0);
    expect_eq($sformatf("lossy (start %0d): every TLP delivered", start), rx.received_tlps.size(), sent.size());
    expect_eq($sformatf("lossy (start %0d): protocol errors = illegal DLLPs", start), tx.protocol_error_count, illegal);
    expect_eq($sformatf("lossy (start %0d): bad DLLPs = corrupt DLLPs", start), tx.bad_dllp_count, corrupt_dllp);
    delivered_total += rx.received_tlps.size();
    replays_total   += tx.replay_count;
    dups_total      += rx.duplicate_count;
    proto_total     += tx.protocol_error_count;
    bad_dllp_total  += tx.bad_dllp_count;
  endfunction

  // Delivered TLPs are the sent ones in order; the retry buffer is clean and consecutive.
  function automatic bit bookkeeping_ok(dll_transmitter_with_replay tx, dll_receiver_with_nak rx, ref int sent[$]);
    foreach (rx.received_tlps[i])
      if (rx.received_tlps[i].payload != sent[i]) return 0;
    foreach (tx.retry_buffer[i])
      if (!tx.retry_buffer[i].crc_ok || tx.retry_buffer[i].is_replay ||
          tx.retry_buffer[i].seq != seq_t'(tx.ackd_seq + 1 + i)) return 0;
    if (tx.retry_buffer.size() != int'(seq_t'(tx.next_transmit_seq - tx.ackd_seq - 1))) return 0;
    return 1;
  endfunction

  initial begin
    int starts[4] = '{0, 4000, 4090, 2047};
    example_1();
    example_2();
    example_3();
    example_4();
    example_5();
    illegal_dllps();
    duplicate_window();
    clean_copy();
    ack_sizes();
    foreach (starts[i]) lossy_traffic(starts[i], 25000);
    if (delivered_total < 8192 || replays_total < 20 || dups_total < 20 || proto_total < 20 ||
        bad_dllp_total < 20 || corrupt_tlp_total < 20 || drop_tlp_total < 20 || timeouts_total < 20) begin
      $display("FAIL: too little coverage: delivered %0d replays %0d dups %0d proto %0d bad dllp %0d corrupt %0d dropped %0d timeouts %0d",
               delivered_total, replays_total, dups_total, proto_total, bad_dllp_total, corrupt_tlp_total,
               drop_tlp_total, timeouts_total);
      errors++;
    end
    if (errors == 0)
      $display("PASS: %0d checks, five examples, %0d TLPs delivered in order over lossy links (%0d replays, %0d duplicates, %0d protocol errors)",
               checks, delivered_total, replays_total, dups_total, proto_total);
    else
      $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
