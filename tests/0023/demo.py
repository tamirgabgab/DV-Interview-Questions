# Change the seed, the writes and the reads and press Run
model = UnalignedEndpointModel(random.Random(7))      # a fixed seed: the same run every time
model.process_write(MemWriteReq(0x10000, bytes(i & 0xFF for i in range(512))))
# an aligned read (one cut possible, at 0x10080) and an unaligned one (cuts at 0x10080, 0x10100)
model.process_read(MemReadReq(0x10000, 256, 0x0200, 0x15))
model.process_read(MemReadReq(0x10020, 256, 0x0300, 0x22))
while model.pending_reads:
    model.tick()
    cpl = model.get_next_completion()
    if cpl is not None:
        print(f"cycle {model.current_cycle:2}: CPL RID=0x{cpl.requester_id:04X} TAG=0x{cpl.tag:02X} "
              f"ADDR=0x{cpl.start_address:X} SIZE={len(cpl.data):3} BC={cpl.byte_count:3} "
              f"data[0]=0x{cpl.data[0]:02X}")
