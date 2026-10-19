module tb;
  //@page typedef bit [7:0] credit_t
  //@page class egress_credit_model
  //@page class egress_sync_model

  localparam hop_id_t HOP = 3;
  int errors = 0, checks = 0;

  function automatic void expect_eq(string what, int got, int want);
    checks++;
    if (got !== want) begin
      $display("FAIL: %s: got %0d, expected %0d", what, got, want);
      errors++;
    end
  endfunction

  // (PCC, PCL, PCR, PCA, occupancy) against the expected tuple
  function automatic void expect_state(string what, egress_sync_model eg, ingress_sync_model ing,
                                       int pcc, int pcl, int pcr, int pca, int occ);
    expect_eq({what, ": PCC"}, eg.pcc, pcc);
    expect_eq({what, ": PCL"}, eg.pcl, pcl);
    expect_eq({what, ": PCR"}, ing.pcr, pcr);
    expect_eq({what, ": PCA"}, ing.pca, pca);
    expect_eq({what, ": occupancy"}, ing.rx_occupancy, occ);
  endfunction

  function automatic void grant(egress_sync_model eg, ingress_sync_model ing);
    eg.consume_credit_grant(ing.build_credit_grant());
  endfunction

  function automatic void send(egress_sync_model eg, ingress_sync_model ing, bit accepted, int id);
    tunneled_packet pkt = new(HOP, id);
    eg.on_packet_transmitted();
    ing.on_packet_received(pkt, accepted);
  endfunction

  // ---------------------------------------------------------------- the six examples

  function automatic void example_a();
    egress_sync_model  eg  = new(HOP);
    ingress_sync_model ing = new(HOP, 5);
    expect_state("A setup", eg, ing, 0, 0, 0, 5, 0);
    expect_eq("A: no credit before the grant", eg.can_transmit(), 0);
    grant(eg, ing);
    expect_state("A grant", eg, ing, 0, 5, 0, 5, 0);
    for (int n = 1; n <= 3; n++) begin
      send(eg, ing, 1, n);
      expect_state($sformatf("A packet %0d", n), eg, ing, n, 5, n, 5, n);
    end
    ing.on_packet_dequeued();
    expect_state("A dequeue 1", eg, ing, 3, 5, 3, 6, 2);
    ing.on_packet_dequeued();
    expect_state("A dequeue 2", eg, ing, 3, 5, 3, 7, 1);
    grant(eg, ing);
    expect_state("A grant 7", eg, ing, 3, 7, 3, 7, 1);
    expect_eq("A: four credits left", forward_distance(eg.pcc, eg.pcl), 4);
    for (int n = 4; n <= 7; n++) begin
      expect_eq("A: may transmit", eg.can_transmit(), 1);
      send(eg, ing, 1, n);
    end
    expect_state("A full", eg, ing, 7, 7, 7, 7, 5);
    expect_eq("A: exhausted", eg.can_transmit(), 0);
  endfunction

  function automatic void example_b();
    egress_sync_model  eg  = new(HOP);
    ingress_sync_model ing = new(HOP, 5);
    credit_sync_packet sync;
    grant(eg, ing);
    send(eg, ing, 1, 1);
    expect_state("B packet 1", eg, ing, 1, 5, 1, 5, 1);
    send(eg, ing, 0, 2);                     // transmitted, lost before the Ingress
    expect_state("B packet 2 lost", eg, ing, 2, 5, 1, 5, 1);
    send(eg, ing, 1, 3);
    expect_state("B packet 3", eg, ing, 3, 5, 2, 5, 2);
    sync = eg.build_credit_sync();
    expect_eq("B: sync carries PCC", sync.pcc, 3);
    ing.consume_credit_sync(sync);
    expect_state("B sync", eg, ing, 3, 5, 3, 6, 2);
    ing.on_packet_dequeued();
    ing.on_packet_dequeued();
    expect_state("B dequeues", eg, ing, 3, 5, 3, 8, 0);
    expect_eq("B: grant carries 8", ing.build_credit_grant().credits, 8);
    grant(eg, ing);
    expect_state("B grant 8", eg, ing, 3, 8, 3, 8, 0);
    expect_eq("B: five credits", forward_distance(eg.pcc, eg.pcl), 5);
  endfunction

  function automatic void example_c();
    egress_sync_model   eg = new(HOP);
    credit_grant_packet g  = new();
    eg.pcc = 9; eg.pcl = 10;
    expect_eq("C: one credit", eg.can_transmit(), 1);
    eg.on_packet_transmitted();
    expect_eq("C: PCC", eg.pcc, 10);
    expect_eq("C: exhausted", eg.can_transmit(), 0);
    g.hop_id = HOP; g.credits = 13;
    eg.consume_credit_grant(g);
    for (int n = 0; n < 3; n++) begin
      expect_eq("C: may transmit", eg.can_transmit(), 1);
      eg.on_packet_transmitted();
    end
    expect_eq("C: exhausted again", eg.can_transmit(), 0);
  endfunction

  function automatic void example_d();
    egress_sync_model   eg = new(HOP);
    credit_grant_packet g  = new();
    int expected[4] = '{255, 0, 1, 2};
    eg.pcc = 251; eg.pcl = 254;
    for (int n = 0; n < 3; n++) begin
      expect_eq("D: may transmit", eg.can_transmit(), 1);
      eg.on_packet_transmitted();
    end
    expect_eq("D: stop at 254", eg.pcc, 254);
    expect_eq("D: exhausted", eg.can_transmit(), 0);
    g.hop_id = HOP; g.credits = 2;
    eg.consume_credit_grant(g);
    expect_eq("D: PCL", eg.pcl, 2);
    foreach (expected[i]) begin
      expect_eq("D: may transmit across the wrap", eg.can_transmit(), 1);
      eg.on_packet_transmitted();
      expect_eq("D: PCC sequence", eg.pcc, expected[i]);
    end
    expect_eq("D: exhausted at 2", eg.can_transmit(), 0);
  endfunction

  function automatic void example_e();
    ingress_sync_model ing  = new(HOP, 10);
    credit_sync_packet sync = new();
    ing.pca = 254; ing.pcr = 253;
    sync.hop_id = HOP; sync.pcc = 1;
    ing.consume_credit_sync(sync);
    expect_eq("E: PCA", ing.pca, 2);
    expect_eq("E: PCR", ing.pcr, 1);
  endfunction

  function automatic void example_f();
    ingress_sync_model ing = new(HOP, 20);
    ing.pcr = 12; ing.pca = 20; ing.rx_occupancy = 3;
    ing.on_packet_dequeued();
    expect_eq("F: PCR", ing.pcr, 12);
    expect_eq("F: PCA", ing.pca, 21);
    expect_eq("F: occupancy", ing.rx_occupancy, 2);
    ing.on_packet_dequeued();
    ing.on_packet_dequeued();
    expect_eq("F: PCR unchanged", ing.pcr, 12);
    expect_eq("F: PCA", ing.pca, 23);
    expect_eq("F: grant carries 23", ing.build_credit_grant().credits, 23);
  endfunction

  // ---------------------------------------------------------------- the transmit rule, every pair

  function automatic void transmit_rule();
    egress_sync_model eg = new(HOP);
    int s, bad = 0;
    bit spec;
    for (int pcc = 0; pcc < 256; pcc++)
      for (int pcl = 0; pcl < 256; pcl++) begin
        eg.pcc = credit_t'(pcc); eg.pcl = credit_t'(pcl);
        s = pcl - pcc;
        spec = ((s > 0) && (s < 128)) || ((s < 0) && (pcc - pcl > 128));
        if (eg.can_transmit() != spec) bad++;
        if (forward_distance(credit_t'(pcc), credit_t'(pcl)) != ((s + 256) % 256)) bad++;
      end
    expect_eq("transmit rule mismatches over 65536 pairs", bad, 0);
  endfunction

  // ---------------------------------------------------------------- random lossy traffic

  int transmitted_total = 0, lost_total = 0;

  // Plain integers next to the modulo counters: transmitted, received, dequeued, lost,
  // and how many of the losses a Credit Sync has already handed back.
  function automatic void random_traffic(int credits, int steps, int loss_percent);
    egress_sync_model  eg  = new(HOP);
    ingress_sync_model ing = new(HOP, credits);
    int T = 0, R = 0, D = 0, L = 0, credited = 0;
    bit                 to_device_is_sync[$];
    credit_t            to_device_pcc[$];
    int                 to_device_id[$];
    credit_t            to_host[$];
    int r;

    for (int step = 0; step <= steps; step++) begin
      // One event kind per step; a kind that is not possible now is skipped. The last round
      // drains everything.
      r = (step < steps) ? $urandom_range(0, 99) : 100;
      if (r < 30) begin
        if (eg.can_transmit()) begin
          eg.on_packet_transmitted();
          T++;
          to_device_is_sync.push_back(0); to_device_pcc.push_back(0); to_device_id.push_back(T);
        end
      end else if (r < 65) begin
        if (to_device_is_sync.size() > 0)
          deliver_one(ing, to_device_is_sync, to_device_pcc, to_device_id, loss_percent, R, L, credited);
      end else if (r < 80) begin
        if (ing.rx_occupancy > 0) begin
          ing.on_packet_dequeued();
          D++;
        end
      end else if (r < 87) begin
        to_host.push_back(ing.build_credit_grant().credits);
      end else if (r < 95) begin
        if (to_host.size() > 0) begin
          credit_grant_packet g = new();
          g.hop_id = HOP; g.credits = to_host.pop_front();
          eg.consume_credit_grant(g);
        end
      end else if (r < 100) begin
        credit_sync_packet s = eg.build_credit_sync();
        to_device_is_sync.push_back(1); to_device_pcc.push_back(s.pcc); to_device_id.push_back(0);
      end else begin
        while (to_device_is_sync.size() > 0)
          deliver_one(ing, to_device_is_sync, to_device_pcc, to_device_id, loss_percent, R, L, credited);
        while (ing.rx_occupancy > 0) begin
          ing.on_packet_dequeued();
          D++;
        end
        ing.consume_credit_sync(eg.build_credit_sync());
        credited = L;
        grant(eg, ing);
        expect_eq($sformatf("credits = free slots after sync and grant (%0d credits)", credits),
                  forward_distance(eg.pcc, eg.pcl), credits);
      end
      if (eg.pcc != credit_t'(T) || ing.pcr != credit_t'(R + credited) ||
          ing.pca != credit_t'(credits + D + credited) || ing.rx_occupancy != R - D || R - D > credits) begin
        $display("FAIL: bookkeeping at step %0d (credits %0d): T=%0d R=%0d D=%0d L=%0d credited=%0d; PCC=%0d PCR=%0d PCA=%0d occ=%0d",
                 step, credits, T, R, D, L, credited, eg.pcc, ing.pcr, ing.pca, ing.rx_occupancy);
        errors++;
        return;
      end
    end
    transmitted_total += T;
    lost_total += L;
  endfunction

  function automatic void deliver_one(ingress_sync_model ing, ref bit is_sync[$], ref credit_t pcc[$],
                                      ref int id[$], input int loss_percent, ref int R, ref int L, ref int credited);
    bit      s = is_sync.pop_front();
    credit_t c = pcc.pop_front();
    int      i = id.pop_front();
    if (s) begin
      credit_sync_packet sync = new();
      sync.hop_id = HOP; sync.pcc = c;
      ing.consume_credit_sync(sync);
      credited = L;                              // every earlier packet arrived or was lost
    end else if ($urandom_range(0, 99) < loss_percent) begin
      L++;
    end else begin
      tunneled_packet pkt = new(HOP, i);
      ing.on_packet_received(pkt, 1);
      R++;
    end
  endfunction

  initial begin
    int sizes[6] = '{1, 2, 5, 16, 64, 127};
    example_a();
    example_b();
    example_c();
    example_d();
    example_e();
    example_f();
    transmit_rule();
    foreach (sizes[i]) begin
      random_traffic(sizes[i], 6000, 6);
      random_traffic(sizes[i], 6000, 0);
    end
    if (transmitted_total < 4000 || lost_total < 100) begin
      $display("FAIL: too little traffic: %0d packets, %0d lost", transmitted_total, lost_total);
      errors++;
    end
    if (errors == 0)
      $display("PASS: %0d checks, six examples, 65536 rule pairs, %0d packets through lossy links (%0d lost)",
               checks, transmitted_total, lost_total);
    else
      $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
