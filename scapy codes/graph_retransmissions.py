from scapy.all import rdpcap, TCP
import matplotlib.pyplot as plt

def get_cumulative_errors(filename):
    print(f"Reading {filename}...")
    pkts = rdpcap(filename)
    start = float(pkts[0].time)
    
    seen_seqs = set()
    error_timeline = []
    total_errors = 0
    
    # Check for duplicate sequence numbers every second
    for i in range(30):
        # Find packets in this specific second
        second_pkts = [p for p in pkts if p.haslayer(TCP) and int(float(p.time) - start) == i]
        
        for p in second_pkts:
            seq = p[TCP].seq
            if seq in seen_seqs:
                total_errors += 1 # Found a duplicate/retransmission!
            else:
                seen_seqs.add(seq)
                
        error_timeline.append(total_errors)
        
    return error_timeline

norm_err = get_cumulative_errors("normal traffic.pcapng")
med_err = get_cumulative_errors("medium traffic.pcapng")
high_err = get_cumulative_errors("high traffic.pcapng")

plt.figure(figsize=(10, 5))
plt.plot(range(30), norm_err, label="Normal Traffic", color="green", linewidth=2.5)
plt.plot(range(30), med_err, label="Medium Traffic", color="orange", linewidth=2.5)
plt.plot(range(30), high_err, label="High Traffic", color="red", linewidth=2.5)

plt.title("CN Network Health: Cumulative TCP Retransmissions Over Time")
plt.xlabel("Time (Seconds)")
plt.ylabel("Total Dropped/Retransmitted Packets")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)

plt.savefig("Triple_Line_Retransmissions.png")
print("Saved!")