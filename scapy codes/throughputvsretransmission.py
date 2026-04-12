from scapy.all import rdpcap, TCP
import matplotlib.pyplot as plt

def get_throughput_vs_errors(filename):
    print(f"Reading {filename}...")
    pkts = rdpcap(filename)
    start = float(pkts[0].time)
    
    throughput_bytes = {}
    error_counts = {}
    
    seen_seqs = set() # To track duplicate/retransmitted packets

    for p in pkts:
        if p.haslayer(TCP):
            t = int(float(p.time) - start)
            throughput_bytes[t] = throughput_bytes.get(t, 0) + len(p)
            
            # Very basic retransmission detection via sequence numbers
            seq = p[TCP].seq
            if seq in seen_seqs:
                error_counts[t] = error_counts.get(t, 0) + 1
            else:
                seen_seqs.add(seq)

    mbps = []
    errors = []
    for i in range(30):
        mbps.append(throughput_bytes.get(i, 0) * 8 / 1e6)
        errors.append(error_counts.get(i, 0))
            
    return mbps, errors

n_mbps, n_err = get_throughput_vs_errors("normal traffic.pcapng")
m_mbps, m_err = get_throughput_vs_errors("medium traffic.pcapng")
h_mbps, h_err = get_throughput_vs_errors("high traffic.pcapng")

plt.figure(figsize=(10, 6))
plt.scatter(n_mbps, n_err, label="Normal", color="green", alpha=0.7, s=50)
plt.scatter(m_mbps, m_err, label="Medium", color="orange", alpha=0.7, s=50)
plt.scatter(h_mbps, h_err, label="High", color="red", alpha=0.7, s=50)

plt.title("Correlation: Throughput vs. TCP Retransmissions")
plt.xlabel("Throughput Speed (Mbps)")
plt.ylabel("Retransmitted Packets per Second")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)

plt.savefig("Triple_Correlation_Throughput_vs_Errors.png")
print("Saved!")