module tb;
  //@page class room_c
  //@page function automatic box_list_t cycle_from

  int errors = 0;

  function automatic void shuffle_notes(output notes_t notes);
    int perm[$];
    perm.delete();                     // start from an empty queue on every call
    for (int b = 1; b <= N; b++) perm.push_back(b);
    perm.shuffle();
    notes[0] = 0;
    for (int b = 1; b <= N; b++) notes[b] = perm[b - 1];
  endfunction

  // One full game with the checks of the page: one swap at most, everybody finds the note
  function automatic void check_game(notes_t notes);
    room_c room = new(notes);
    helper(room);
    if (room.swaps_left < MAX_SWAPS - 1) errors++;
    for (int me = 1; me <= N; me++)
      if (!find_my_note(room, me)) errors++;
    if (!play(notes)) errors++;
  endfunction

  // A random arrangement with one cycle of length `long_len` (the rest are fixed points)
  function automatic void with_long_cycle(int long_len, output notes_t notes);
    int boxes[$];
    boxes.delete();
    for (int b = 1; b <= N; b++) begin
      boxes.push_back(b);
      notes[b] = b;
    end
    notes[0] = 0;
    boxes.shuffle();
    for (int i = 0; i < long_len; i++) notes[boxes[i]] = boxes[(i + 1) % long_len];
  endfunction

  initial begin
    notes_t    notes, after;
    room_c     room;
    box_list_t cycle;
    int        wins = 0;
    bit        all_found;

    // The example on the page: a cycle of 11 splits into 6 and 5 by swapping boxes 1 and 9
    notes = '{0, 7, 11, 15, 16, 13, 2, 12, 14, 4, 5, 6, 3, 1, 8, 9, 10};
    if (cycle_from(notes, 1).size() != 11) errors++;
    room = new(notes);
    helper(room);
    room.look_all(after);
    if (after[1] != 4 || after[9] != 7) errors++;
    if (cycle_from(after, 1).size() != 6 || cycle_from(after, 7).size() != 5) errors++;
    check_game(notes);

    for (int len = 1; len <= N; len++)
      repeat (50) begin
        with_long_cycle(len, notes);
        check_game(notes);
      end

    repeat (20000) begin
      shuffle_notes(notes);
      check_game(notes);
    end

    // Without person 0 about one third of the arrangements win
    repeat (20000) begin
      all_found = 1;                 // a declaration initializer here would run only once (static)
      shuffle_notes(notes);
      room = new(notes);
      for (int me = 1; me <= N; me++)
        if (!find_my_note(room, me)) all_found = 0;
      wins += all_found;
    end
    if (wins < 6400 || wins > 7100) errors++;

    if (errors == 0) $display("PASS (without helper: %0d / 20000 win)", wins);
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
