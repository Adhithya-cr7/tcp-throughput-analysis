from scapy.all import rdpcap, TCP, IP
import matplotlib.pyplot as plt

def get_tcp_efficiency(filename):
    print(f"Reading {filename}...")
    pkts = rdpcap(filename)
    start = float(pkts[0].time)
    
    total_bytes = {}
    payload_bytes = {}

    for p in pkts:
        if p.haslayer(TCP) and p.haslayer(IP):
            t = int(float(p.time) - start)
            
            t_len = len(p)
            total_bytes[t] = total_bytes.get(t, 0) + t_len
            
            # TCP Payload = Total Length - IP Header - TCP Header
            ip_header_len = p[IP].ihl * 4
            tcp_header_len = p[TCP].dataofs * 4
            payload = t_len - (ip_header_len + tcp_header_len + 14) # 14 is Ethernet header
            
            # Ensure no negative numbers from weird packets
            payload = max(0, payload) 
            payload_bytes[t] = payload_bytes.get(t, 0) + payload

    efficiency_ratio = []
    for i in range(30):
        if total_bytes.get(i, 0) > 0:
            ratio = (payload_bytes.get(i, 0) / total_bytes[i]) * 100
            efficiency_ratio.append(ratio)
        else:
            efficiency_ratio.append(0)
            
    return efficiency_ratio

norm_eff = get_tcp_efficiency("normal traffic.pcapng")
med_eff = get_tcp_efficiency("medium traffic.pcapng")
high_eff = get_tcp_efficiency("high traffic.pcapng")

plt.figure(figsize=(10, 5))
plt.plot(range(30), norm_eff, label="Normal Load", color="green", linewidth=2)
plt.plot(range(30), med_eff, label="Medium Load", color="orange", linewidth=2)
plt.plot(range(30), high_eff, label="High Load (Congested)", color="red", linewidth=2)

plt.title("CN Protocol Overhead: TCP Payload Efficiency (%)")
plt.xlabel("Time (Seconds)")
plt.ylabel("Usable Application Data (%)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)

plt.savefig("Triple_TCP_Efficiency.png")
print("Saved Efficiency Graph!")