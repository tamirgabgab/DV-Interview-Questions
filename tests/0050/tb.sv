// Question 0050: the page's ooo_scoreboard on the scenarios of part b (the same kinds of
// errors as the Python reference on the page), and on random legal streams (no error)
// and streams with one injected bug (at least one error of the right kind).
module tb;
  //@page class ooo_scoreboard

  int errors = 0;

  typedef struct { longint t; string op; int id; int data; } ev_t;

  function automatic void play(ev_t ev[$], longint timeout, ref string out[$]);
    ooo_scoreboard sb = new(timeout);
    foreach (ev[k]) begin
      sb.check_timeouts(ev[k].t);
      case (ev[k].op)
        "req":   sb.on_request(ev[k].id, ev[k].data, ev[k].t);
        "rsp":   sb.on_response(ev[k].id, ev[k].data, ev[k].t);
        "reset": sb.on_reset();
        default: sb.final_check();
      endcase
    end
    out = sb.errors;
  endfunction

  function automatic ev_t e(longint t, string op, int id = 0, int data = 0);
    ev_t x;
    x.t = t; x.op = op; x.id = id; x.data = data;
    return x;
  endfunction

  function automatic bit has(string errs[$], string word);
    foreach (errs[k]) if (errs[k].substr(0, word.len() - 1) == word) return 1;
    return 0;
  endfunction

  task automatic expect_scenario(string name, ev_t ev[$], string word);
    string out[$];
    play(ev, 8, out);
    if (word == "" ? out.size() != 0 : !has(out, word)) begin
      errors++; $display("%s: %0d errors, wanted %s", name, out.size(), word == "" ? "none" : word);
      foreach (out[k]) $display("  %s", out[k]);
    end
  endtask

  // a legal random stream: requests and responses interleaved, each ID in its own order
  function automatic void legal(int n, int ids, ref ev_t ev[$]);
    int pend[int][$];
    int sent = 0, nxt = 100, busy[$], i;
    longint t = 0;
    ev = {};
    while (1) begin
      busy = {};
      for (int j = 0; j < ids; j++) if (pend.exists(j) && pend[j].size() > 0) busy.push_back(j);
      if (sent >= n && busy.size() == 0) break;
      if (sent < n && (busy.size() == 0 || $urandom_range(99) < 55)) begin
        i = $urandom_range(ids - 1);
        ev.push_back(e(t, "req", i, nxt)); pend[i].push_back(nxt); nxt++; sent++;
      end else begin
        i = busy[$urandom_range(busy.size() - 1)];
        ev.push_back(e(t, "rsp", i, pend[i].pop_front()));
      end
      t++;
    end
    ev.push_back(e(t, "end"));
  endfunction

  initial begin
    ev_t ev[$], bad[$];
    string out[$];
    int k, j;
    expect_scenario("legal interleave", '{e(0, "req", 0, 10), e(1, "req", 1, 20), e(2, "req", 0, 11), e(3, "rsp", 1, 20), e(4, "rsp", 0, 10), e(5, "rsp", 0, 11), e(6, "end")}, "");
    expect_scenario("swap in an ID", '{e(0, "req", 0, 10), e(1, "req", 0, 11), e(2, "rsp", 0, 11), e(3, "rsp", 0, 10), e(4, "end")}, "mismatch");
    expect_scenario("bad data", '{e(0, "req", 0, 10), e(1, "req", 1, 20), e(2, "rsp", 1, 21), e(3, "rsp", 0, 10), e(4, "end")}, "mismatch");
    expect_scenario("missing", '{e(0, "req", 0, 10), e(1, "req", 1, 20), e(2, "rsp", 1, 20), e(3, "end")}, "missing");
    expect_scenario("duplicate", '{e(0, "req", 0, 10), e(1, "rsp", 0, 10), e(2, "rsp", 0, 10), e(3, "end")}, "unexpected");
    expect_scenario("late", '{e(0, "req", 0, 10), e(12, "rsp", 0, 10), e(13, "end")}, "timeout");
    expect_scenario("reset, then new", '{e(0, "req", 0, 10), e(1, "req", 1, 20), e(2, "reset"), e(3, "req", 1, 21), e(4, "rsp", 1, 21), e(5, "end")}, "");
    expect_scenario("stale after reset", '{e(0, "req", 0, 10), e(1, "reset"), e(2, "rsp", 0, 10), e(3, "end")}, "unexpected");
    void'($urandom(50));
    for (int r = 0; r < 300; r++) begin
      legal($urandom_range(1, 40), $urandom_range(1, 5), ev);
      play(ev, 100000, out);
      if (out.size() != 0) begin errors++; $display("legal stream %0d: %s", r, out[0]); end
      // one corrupted response: the data of a random response
      bad = ev;
      do k = $urandom_range(bad.size() - 1); while (bad[k].op != "rsp" && bad.size() > 1);
      if (bad[k].op == "rsp") begin
        bad[k].data += 1000;
        play(bad, 100000, out);
        if (!has(out, "mismatch")) begin errors++; $display("bad data %0d not caught", r); end
        // one dropped response
        bad = ev; bad.delete(k);
        play(bad, 100000, out);
        if (!has(out, "missing")) begin errors++; $display("drop %0d not caught", r); end
        // one duplicated response
        bad = ev; bad.insert(k + 1, ev[k]);
        play(bad, 100000, out);
        if (!has(out, "unexpected")) begin errors++; $display("dup %0d not caught", r); end
        // the next response of the same ID swapped with this one
        for (j = k + 1; j < ev.size(); j++) if (ev[j].op == "rsp" && ev[j].id == ev[k].id) break;
        if (j < ev.size()) begin
          bad = ev; bad[k].data = ev[j].data; bad[j].data = ev[k].data;
          play(bad, 100000, out);
          if (!has(out, "mismatch")) begin errors++; $display("swap %0d not caught", r); end
        end
      end
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
