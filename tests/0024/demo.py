# One Path from the HOST (Egress) to the DEVICE (Ingress) with 5 credits; packet 2 is lost
HOP = 3
egress, ingress = EgressSyncModel(HOP), IngressSyncModel(HOP, 5)

def show(event):
    credits = forward_distance(egress.pcc, egress.pcl)
    print(f"{event:<30} PCC={egress.pcc:3} PCL={egress.pcl:3} | PCR={ingress.pcr:3} PCA={ingress.pca:3} "
          f"buffer={ingress.rx_occupancy}/{ingress.buffer_size} | credits={credits}")

show("path setup")
egress.consume_credit_grant(ingress.build_credit_grant()); show("Credit Grant")
for n, accepted in ((1, True), (2, False), (3, True)):      # change the flags: which packets arrive
    egress.on_packet_transmitted()
    ingress.on_packet_received(TunneledPacket(HOP, n), accepted)
    show(f"packet {n} {'accepted' if accepted else 'DROPPED'}")
for _ in range(2):
    ingress.on_packet_dequeued(); show("dequeue")
egress.consume_credit_grant(ingress.build_credit_grant()); show("Credit Grant (a credit leaked)")
ingress.consume_credit_sync(egress.build_credit_sync()); show("Credit Sync")
egress.consume_credit_grant(ingress.build_credit_grant()); show("Credit Grant (repaired)")
