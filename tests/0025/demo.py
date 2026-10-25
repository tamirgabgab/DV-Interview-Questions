# RC transmitter and EP receiver from Sequence Number 4094; the link damages TLP 4095 and
# then the first Ack. Change the thresholds, the damaged packets or the order and press Run.
rc, ep = TransmitterWithReplay(4094), ReceiverWithNak(4094, random.Random(5))
ep.ack_threshold = 3                             # the first Ack only after the gap is closed

def show(event):
    retry = ", ".join(str(t.seq) for t in rc.retry_buffer) or "-"
    print(f"{event:<34} NTS={rc.next_transmit_seq:4} ACKD={rc.ackd_seq:4} retry=[{retry:<14}] | "
          f"NRS={ep.next_rcv_seq:4} pending={ep.accepted_since_ack}/{ep.ack_threshold} NAK_SCHEDULED={int(ep.nak_scheduled)}")

def deliver_tlp(corrupt=False):
    tlp = rc.tx_tlps.pop(0)
    if corrupt:
        tlp.crc_ok = False                       # the link, not the model, damages the wire copy
    ep.receive_tlp(tlp)
    show(f"TLP {tlp.seq}{' replay' if tlp.is_replay else ''}{' BAD LCRC' if corrupt else ''} -> EP")

def deliver_dllp(corrupt=False):
    dllp = ep.tx_dllps.pop(0)
    if corrupt:
        dllp.crc_ok = False
    rc.receive_dllp(dllp)
    show(f"{dllp.kind.name} {dllp.seq}{' BAD CRC' if corrupt else ''} -> RC")

show("start")
for payload in (0xA0, 0xA1, 0xA2, 0xA3):
    rc.send_tlp(Tlp(payload))
show("RC sent 4094, 4095, 0, 1")
deliver_tlp()                                    # 4094 accepted
deliver_tlp(corrupt=True)                        # 4095 damaged: Nak 4094
deliver_tlp(); deliver_tlp()                     # 0 and 1: future, discarded quietly
deliver_dllp()                                   # Nak 4094: purge 4094, replay 4095 0 1
while rc.tx_tlps:
    deliver_tlp()
ep.flush_ack(); show("flush_ack")
if ep.tx_dllps:
    deliver_dllp(corrupt=True)                   # the Ack is damaged: nothing changes at the RC
rc.on_replay_timeout(); show("replay timer")
while rc.tx_tlps:
    deliver_tlp()                                # duplicates: each answered with the same Ack
while ep.tx_dllps:
    deliver_dllp()
