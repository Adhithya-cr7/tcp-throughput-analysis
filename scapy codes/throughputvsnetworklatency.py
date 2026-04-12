from scapy.all import rdpcap
import matplotlib.pyplot as plt

def get_throughput_vs_latency(filename):
    print(f"Reading {filename}...")
    pkts = rdpcap(filename)
    start = float(pkts[0].time)
    
    throughput_bytes = {}
    latency_sums = {}
    packet_counts = {}

    # Calculate both metrics for every 1-second interval
    for i in range(1, len(pkts)):
        p = pkts[i]
        t = int(float(p.time) - start)
        delay = float(p.time - pkts[i-1].time) * 1000 # ms
        
        throughput_bytes[t] = throughput_bytes.get(t, 0) + len(p)
        latency_sums[t] = latency_sums.get(t, 0) + delay
        packet_counts[t] = packet_counts.get(t, 0) + 1

    mbps = []
    avg_lat = []
    for i in range(30): # First 30 seconds
        mbps.append(throughput_bytes.get(i, 0) * 8 / 1e6)
        if packet_counts.get(i, 0) > 0:
            avg_lat.append(latency_sums.get(i, 0) / packet_counts[i])
        else:
            avg_lat.append(0)
            
    return mbps, avg_lat

# Extract data for all 3 files
n_mbps, n_lat = get_throughput_vs_latency("normal traffic.pcapng")
m_mbps, m_lat = get_throughput_vs_latency("medium traffic.pcapng")
h_mbps, h_lat = get_throughput_vs_latency("high traffic.pcapng")

plt.figure(figsize=(10, 6))

# Plot all three as scattered dots to show the correlation
plt.scatter(n_mbps, n_lat, label="Normal", color="green", alpha=0.7, s=50)
plt.scatter(m_mbps, m_lat, label="Medium", color="orange", alpha=0.7, s=50)
plt.scatter(h_mbps, h_lat, label="High", color="red", alpha=0.7, s=50)

plt.title("Correlation: Throughput vs. Network Latency")
plt.xlabel("Throughput Speed (Mbps)")
plt.ylabel("Average Latency/Delay (ms)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)

plt.savefig("Triple_Correlation_Throughput_vs_Latency.png")
print("Saved!")