from scapy.all import rdpcap
import matplotlib.pyplot as plt
import numpy as np

def get_basic_throughput_stats(filename):
    print(f"Reading {filename}...")
    pkts = rdpcap(filename)
    start = float(pkts[0].time)
    bins = {}
    
    # Group packets into 1-second chunks
    for p in pkts:
        t = int(float(p.time) - start)
        bins[t] = bins.get(t, 0) + len(p)
        
    # Calculate Mbps for the first 30 seconds
    mbps_list = [bins.get(i, 0) * 8 / 1e6 for i in range(30)]
    
    # Calculate the two basic stats
    avg_throughput = sum(mbps_list) / len(mbps_list)
    max_throughput = max(mbps_list)
    
    return avg_throughput, max_throughput

# 1. Extract the stats from your 3 files
n_avg, n_max = get_basic_throughput_stats("normal traffic.pcapng")
m_avg, m_max = get_basic_throughput_stats("medium traffic.pcapng")
h_avg, h_max = get_basic_throughput_stats("high traffic.pcapng")

# 2. Setup the Bar Graph formatting
labels = ['Normal Traffic', 'Medium Traffic', 'High Traffic']
avg_data = [n_avg, m_avg, h_avg]
max_data = [n_max, m_max, h_max]

x = np.arange(len(labels))  # The x-axis locations for the groups
width = 0.35  # The width of the bars

# 3. Draw the graph
fig, ax = plt.subplots(figsize=(9, 6))

# Plot the two sets of bars side-by-side
bar1 = ax.bar(x - width/2, avg_data, width, label='Average Throughput', color='#2ca02c') # Green
bar2 = ax.bar(x + width/2, max_data, width, label='Max Peak Throughput', color='#d62728') # Red

# Add labels, title, and formatting
ax.set_ylabel('Speed (Mbps)', fontsize=12, fontweight='bold')
ax.set_title('Basic Comparison: Average vs Peak Throughput', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=11)
ax.legend()

# Add a horizontal grid so it's easy to read the values
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Add the exact numbers on top of the bars for maximum points!
ax.bar_label(bar1, fmt='%.1f', padding=3)
ax.bar_label(bar2, fmt='%.1f', padding=3)

plt.tight_layout()
plt.savefig("Bar_Graph_Throughput_Comparison.png", dpi=300)
print("Bar Graph Saved successfully!")