from scapy.all import rdpcap, TCP, UDP
import matplotlib.pyplot as plt

def get_throughput(filename):
    print(f"Reading {filename}...")
    pkts = rdpcap(filename)
    start = float(pkts[0].time)
    bins = {}
    for p in pkts:
        # TO FILTER FOR TCP ONLY, UNCOMMENT THE LINE BELOW:
        # if not p.haslayer(TCP): continue 
        
        t = int(float(p.time) - start)
        bins[t] = bins.get(t, 0) + len(p)
    return [bins.get(i, 0) * 8 / 1e6 for i in range(30)] # 30 seconds

norm = get_throughput("normal traffic.pcapng")
med = get_throughput("medium traffic.pcapng")
high = get_throughput("high traffic.pcapng")

plt.figure(figsize=(10, 5))
plt.fill_between(range(30), norm, color="green", alpha=0.5, label="Normal")
plt.fill_between(range(30), med, color="orange", alpha=0.5, label="Medium")
plt.fill_between(range(30), high, color="red", alpha=0.5, label="High")

plt.title("Triple Overlay: Throughput Area Chart")
plt.xlabel("Time (Seconds)")
plt.ylabel("Throughput (Mbps)")
plt.legend()
plt.savefig("Scapy_Area_Chart_All.png")
print("Saved Area Chart!")