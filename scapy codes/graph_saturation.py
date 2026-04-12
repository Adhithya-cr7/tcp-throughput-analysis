from scapy.all import rdpcap
import matplotlib.pyplot as plt

def get_average_delay_line(filename):
    print(f"Reading {filename}...")
    pkts = rdpcap(filename)
    start = float(pkts[0].time)
    
    delay_sums = {}
    packet_counts = {}
    
    for i in range(1, len(pkts)):
        t = int(float(pkts[i].time) - start)
        delay = float(pkts[i].time - pkts[i-1].time) # Time since last packet
        
        delay_sums[t] = delay_sums.get(t, 0) + delay
        packet_counts[t] = packet_counts.get(t, 0) + 1
        
    avg_delay_timeline = []
    for i in range(30):
        if packet_counts.get(i, 0) > 0:
            avg_delay_timeline.append(delay_sums[i] / packet_counts[i])
        else:
            avg_delay_timeline.append(0)
            
    return avg_delay_timeline

norm_delay = get_average_delay_line("normal traffic.pcapng")
med_delay = get_average_delay_line("medium traffic.pcapng")
high_delay = get_average_delay_line("high traffic.pcapng")

plt.figure(figsize=(10, 5))
plt.plot(range(30), norm_delay, label="Normal (Sparse Traffic)", color="green", linewidth=2)
plt.plot(range(30), med_delay, label="Medium (Moderate Traffic)", color="orange", linewidth=2)
plt.plot(range(30), high_delay, label="High (Saturated Link)", color="red", linewidth=2)

plt.title("CN Link Saturation: Average Packet Delay Over Time")
plt.xlabel("Time (Seconds)")
plt.ylabel("Average Delay Between Packets (Seconds)")
# Using a log scale on the Y-axis makes this look incredibly professional
plt.yscale("log") 
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)

plt.savefig("Triple_Line_Saturation.png")
print("Saved!")