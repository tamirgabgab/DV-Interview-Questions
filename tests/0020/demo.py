# Change the address, the length, MPS and RCB and press Run
for addr, length, mps, rcb in [(0x1010, 256, 256, 64), (0x1010, 256, 128, 64), (0x1000, 256, 128, 64)]:
    splits = completion_splits(addr, length, mps, rcb)
    print(f"addr=0x{addr:X} len={length} MPS={mps} RCB={rcb}: {len(splits)} splits")
    for s in splits:
        print("   ", s)
