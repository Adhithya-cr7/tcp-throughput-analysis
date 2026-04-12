from scapy.all import rdpcap, TCP
import matplotlib.pyplot as plt

def get_throughput_vs_window(filename):
    print(f"Reading {filename}...")
    pkts = rdpcap(filename)
    start = float(pkts[0].time)
    
    throughput_bytes = {}
    window_sums = {}
    tcp_counts = {}

    for p in pkts:
        if p.haslayer(TCP):
            t = int(float(p.time) - start)
            throughput_bytes[t] = throughput_bytes.get(t, 0) + len(p)
            window_sums[t] = window_sums.get(t, 0) + p[TCP].window
            tcp_counts[t] = tcp_counts.get(t, 0) + 1

    mbps = []
    avg_win = []
    for i in range(30):
        mbps.append(throughput_bytes.get(i, 0) * 8 / 1e6)
        if tcp_counts.get(i, 0) > 0:
            avg_win.append(window_sums.get(i, 0) / tcp_counts[i])
        else:
            avg_win.append(0)
            
    return mbps, avg_win

n_mbps, n_win = get_throughput_vs_window("normal traffic.pcapng")
m_mbps, m_win = get_throughput_vs_window("medium traffic.pcapng")
h_mbps, h_win = get_throughput_vs_window("high traffic.pcapng")

plt.figure(figsize=(10, 6))
plt.scatter(n_mbps, n_win, label="Normal", color="green", alpha=0.7, s=50)
plt.scatter(m_mbps, m_win, label="Medium", color="orange", alpha=0.7, s=50)
plt.scatter(h_mbps, h_win, label="High", color="red", alpha=0.7, s=50)

plt.title("Correlation: Throughput vs. TCP Receive Window")
plt.xlabel("Throughput Speed (Mbps)")
plt.ylabel("Average TCP Window Size (Bytes)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)

plt.savefig("Triple_Correlation_Throughput_vs_Window.png")
print("Saved!")