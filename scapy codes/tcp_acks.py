from scapy.all import rdpcap, TCP
import matplotlib.pyplot as plt

def get_throughput_vs_acks(filename):
    print(f"Reading {filename}...")
    pkts = rdpcap(filename)
    start = float(pkts[0].time)
    
    throughput_bytes = {}
    pure_ack_counts = {}

    for p in pkts:
        if p.haslayer(TCP):
            t = int(float(p.time) - start)
            throughput_bytes[t] = throughput_bytes.get(t, 0) + len(p)
            
            # Count "Pure ACKs" (Packets with the ACK flag set, but ZERO payload)
            if 'A' in p[TCP].flags and len(p[TCP].payload) == 0:
                pure_ack_counts[t] = pure_ack_counts.get(t, 0) + 1

    mbps = []
    acks = []
    for i in range(30):
        mbps.append(throughput_bytes.get(i, 0) * 8 / 1e6)
        acks.append(pure_ack_counts.get(i, 0))
            
    return mbps, acks

n_mbps, n_acks = get_throughput_vs_acks("normal traffic.pcapng")
m_mbps, m_acks = get_throughput_vs_acks("medium traffic.pcapng")
h_mbps, h_acks = get_throughput_vs_acks("high traffic.pcapng")

plt.figure(figsize=(10, 6))
plt.scatter(n_mbps, n_acks, label="Normal Traffic", color="green", alpha=0.7, s=50)
plt.scatter(m_mbps, m_acks, label="Medium Traffic", color="orange", alpha=0.7, s=50)
plt.scatter(h_mbps, h_acks, label="High Traffic", color="red", alpha=0.7, s=50)

plt.title("CN Congestion Control: TCP Throughput vs. Pure ACK Storms")
plt.xlabel("TCP Throughput (Mbps)")
plt.ylabel("Pure ACKs Sent Per Second (Zero Data)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)

plt.savefig("Triple_TCP_ACK_Storm.png")
print("Saved ACK Storm Graph!")