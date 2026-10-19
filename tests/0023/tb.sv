module tb;
  //@page typedef byte unsigned block_t
  //@page class endpoint_ref_model;
  //@page class unaligned_endpoint_model

  // One open read as the checker sees it: where the next completion must start, how many
  // bytes are left, the memory at request time, and when the request arrived.
  class open_read;
    bit [63:0]    start, next_addr;
    int           left, req_cycle;
    byte unsigned snap[];
    int           sizes[$];
  endclass

  byte unsigned shadow[bit [63:0]];     // independent memory at byte resolution
  open_read     opens[int];             // key: {requester_id, tag}
  int           errors = 0, completions = 0, interleaved = 0, last_key = -1;
  bit           seen_one = 0, seen_two = 0, seen_three = 0, seen_unaligned_start = 0;

  function automatic void do_write(endpoint_ref_model m, bit [63:0] addr, int len);
    mem_write_req w = new(addr, len);
    foreach (w.data[i]) begin
      w.data[i] = byte'($urandom);
      shadow[addr + i] = w.data[i];
    end
    m.process_write(w);
  endfunction

  function automatic void do_read(endpoint_ref_model m, bit [63:0] addr, int len, bit [15:0] rid, bit [9:0] tag);
    mem_read_req r = new();
    open_read    o = new();
    int          key = {rid, tag};
    r.address = addr; r.length_bytes = len; r.requester_id = rid; r.tag = tag;
    if (opens.exists(key)) begin
      $display("FAIL: tag %0h reused while open", key);
      errors++;
    end
    o.start = addr; o.next_addr = addr; o.left = len; o.req_cycle = m.current_cycle;
    o.snap = new[len];
    foreach (o.snap[i]) o.snap[i] = shadow.exists(addr + i) ? shadow[addr + i] : 8'h00;
    opens[key] = o;
    m.process_read(r);
  endfunction

  function automatic void check(completion c, int cycle);
    int key = {c.requester_id, c.tag};
    open_read o;
    if (!opens.exists(key)) begin
      $display("FAIL: completion for unknown read %0h", key); errors++; return;
    end
    o = opens[key];
    if (c.start_address != o.next_addr) begin
      $display("FAIL: read %0h: completion at 0x%0h, expected 0x%0h", key, c.start_address, o.next_addr); errors++;
    end
    if (c.byte_count != o.left) begin
      $display("FAIL: read %0h: byte count %0d, expected %0d", key, c.byte_count, o.left); errors++;
    end
    if (c.data.size() == 0 || c.data.size() > MPS) begin
      $display("FAIL: read %0h: payload of %0d bytes", key, c.data.size()); errors++;
    end
    if (c.start_address != o.start && c.start_address % RCB != 0) begin
      $display("FAIL: read %0h: cut at 0x%0h is not on an RCB boundary", key, c.start_address); errors++;
    end
    if (cycle <= o.req_cycle) begin
      $display("FAIL: read %0h: completion in the request cycle", key); errors++;
    end
    foreach (c.data[j])
      if (c.start_address - o.start + j < o.snap.size() &&
          c.data[j] != o.snap[c.start_address - o.start + j]) begin
        $display("FAIL: read %0h: data[%0d] = %0h, expected %0h", key, j, c.data[j], o.snap[c.start_address - o.start + j]);
        errors++;
        break;
      end
    if (o.sizes.size() > 0 && last_key != -1 && last_key != key) interleaved++;
    last_key = key;
    o.sizes.push_back(c.data.size());
    o.next_addr += c.data.size();
    o.left      -= c.data.size();
    completions++;
    if (o.left == 0) begin
      if (o.sizes.size() == 1) seen_one = 1;
      if (o.sizes.size() == 2) seen_two = 1;
      if (o.sizes.size() == 3) seen_three = 1;
      if (o.start % RCB != 0) seen_unaligned_start = 1;
      opens.delete(key);
    end
  endfunction

  // Random traffic for `steps` cycles, then drain; aligned traffic uses the aligned model.
  function automatic void phase(endpoint_ref_model m, bit aligned, int steps);
    bit [63:0] addr;
    int        len, tag = 0;
    completion c;
    shadow.delete();                    // a fresh model starts from an empty memory
    last_key = -1;
    for (int s = 0; s < steps; s++) begin
      m.tick();
      if ($urandom_range(0, 9) < 4) begin
        addr = aligned ? 64'h10000 + $urandom_range(0, 7) * RCB : 64'h10000 + $urandom_range(0, 1023);
        len  = aligned ? ($urandom_range(0, 1) ? RCB : 2 * RCB) : $urandom_range(1, MRRS);
        do_write(m, addr, len);
      end
      if ($urandom_range(0, 9) < 4 && tag < 1000) begin
        addr = aligned ? 64'h10000 + $urandom_range(0, 7) * RCB : 64'h10000 + $urandom_range(0, 1023);
        len  = aligned ? ($urandom_range(0, 1) ? RCB : 2 * RCB) : $urandom_range(1, MRRS);
        do_read(m, addr, len, 16'h0200 + $urandom_range(0, 1), 10'(tag++));
      end
      c = m.get_next_completion();
      if (c != null) check(c, m.current_cycle);
    end
    for (int s = 0; s < 2000 && m.pending_reads.size() > 0; s++) begin
      m.tick();
      c = m.get_next_completion();
      if (c != null) check(c, m.current_cycle);
    end
    if (m.pending_reads.size() > 0 || opens.size() > 0) begin
      $display("FAIL: %0d reads never finished", opens.size()); errors++;
      opens.delete();
    end
  endfunction

  // The page's examples: every legal split shows up, and only legal splits.
  function automatic void examples();
    bit seen_a[2], seen_b[4];
    for (int trial = 0; trial < 200; trial++) begin
      endpoint_ref_model      a = new();
      unaligned_endpoint_model b = new();
      mem_write_req w = new(64'h10000, 512);
      mem_read_req  r = new();
      completion    c;
      int sizes[$], bcs[$];
      foreach (w.data[i]) w.data[i] = byte'(i);
      a.process_write(w);
      b.process_write(w);
      // part a: 256 bytes from 0x10000
      r.address = 64'h10000; r.length_bytes = 256; r.requester_id = 16'h0200; r.tag = 10'h15;
      a.process_read(r);
      sizes.delete(); bcs.delete();
      while (a.pending_reads.size() > 0) begin
        a.tick(); c = a.get_next_completion();
        if (c != null) begin sizes.push_back(c.data.size()); bcs.push_back(c.byte_count); end
      end
      if (sizes.size() == 1 && sizes[0] == 256 && bcs[0] == 256) seen_a[0] = 1;
      else if (sizes.size() == 2 && sizes[0] == 128 && sizes[1] == 128 && bcs[0] == 256 && bcs[1] == 128) seen_a[1] = 1;
      else begin $display("FAIL: part a split %p", sizes); errors++; end
      // part b: 256 bytes from 0x10020
      r = new(); r.address = 64'h10020; r.length_bytes = 256; r.requester_id = 16'h0300; r.tag = 10'h22;
      b.process_read(r);
      sizes.delete(); bcs.delete();
      while (b.pending_reads.size() > 0) begin
        b.tick(); c = b.get_next_completion();
        if (c != null) begin
          sizes.push_back(c.data.size()); bcs.push_back(c.byte_count);
          if (c.data[0] != byte'(c.start_address - 64'h10000)) begin
            $display("FAIL: part b data at 0x%0h is %0h", c.start_address, c.data[0]); errors++;
          end
        end
      end
      if (sizes.size() == 1 && sizes[0] == 256) seen_b[0] = 1;
      else if (sizes.size() == 2 && sizes[0] == 96 && sizes[1] == 160 && bcs[1] == 160) seen_b[1] = 1;
      else if (sizes.size() == 2 && sizes[0] == 224 && sizes[1] == 32 && bcs[1] == 32) seen_b[2] = 1;
      else if (sizes.size() == 3 && sizes[0] == 96 && sizes[1] == 128 && sizes[2] == 32 &&
               bcs[0] == 256 && bcs[1] == 160 && bcs[2] == 32) seen_b[3] = 1;
      else begin $display("FAIL: part b split %p with byte counts %p", sizes, bcs); errors++; end
    end
    if (!(seen_a[0] && seen_a[1])) begin $display("FAIL: part a did not show both answers"); errors++; end
    foreach (seen_b[i]) if (!seen_b[i]) begin $display("FAIL: part b split %0d never produced", i); errors++; end
  endfunction

  initial begin
    endpoint_ref_model       aligned_model = new();
    unaligned_endpoint_model unaligned_model = new();
    phase(aligned_model, 1, 400);
    if (!(seen_one && seen_two)) begin $display("FAIL: aligned traffic did not show both shapes"); errors++; end
    phase(unaligned_model, 0, 600);
    if (!(seen_three && seen_unaligned_start)) begin $display("FAIL: unaligned traffic too tame"); errors++; end
    if (interleaved < 20) begin $display("FAIL: only %0d interleavings", interleaved); errors++; end
    examples();
    if (errors == 0)
      $display("PASS: %0d completions checked, %0d interleavings, both examples covered", completions, interleaved);
    else
      $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
