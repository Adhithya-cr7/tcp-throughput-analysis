# TCP Throughput Analysis Under Volumetric Traffic Conditions

**Author:** Adithya Kumar Tummala  
**Registration Number:** 24BCE1588  
**Institution:** Vellore Institute of Technology (VIT), Chennai  

---

## 📌 Project Overview
This repository contains the source files, packet captures (PCAPs), and Python scripts used for a comprehensive Digital Assessment (DA) in Computer Networks. The project investigates the mechanics of TCP Throughput degradation and network bottlenecks in two main phases:

1. **Malware Baseline Analysis:** Analyzing a real-world malware PCAP to observe abnormal TCP behaviors, such as Zero Window crashes and artificial CWND limitations.
2. **Active Volumetric Load Testing:** Using `hping3` to programmatically generate Normal, Medium (`--fast`), and High (`--flood`) traffic against a target server, and analyzing the resulting PCAPs to visualize protocol collapse under stress.

## 🛠️ Tools & Technologies Used
* **Wireshark:** Deep Packet Inspection and native I/O Graphing.
* **Python 3 (Scapy):** Programmatic PCAP parsing and multi-file analysis.
* **Matplotlib:** Generating comparative overlay scatter plots and area charts.
* **hping3 & Ubuntu Linux:** Controlled volumetric traffic generation.

## 📂 Repository Structure
* `pcaps/`: Contains the raw `.pcapng` files captured during the Normal, Medium, and Flood traffic tests.
* `malware_baseline/`: Contains the baseline malware PCAP file used for the initial analysis.
  * ⚠️ **Security Note:** The malware PCAP archive is password-protected. **Password:** `infected_20250122`
* `scripts/`: Python Scapy scripts used to parse the PCAPs and generate the comparative overlay graphs.
* `graphs/`: High-resolution outputs of all the graphs rendered via Wireshark and Matplotlib.

## 🚀 How to Use
1. Clone this repository to your local machine:
   ```bash
   git clone [https://github.com/Adhithya-cr7/tcp-throughput-analysis.git](https://github.com/Adhithya-cr7/tcp-throughput-analysis.git)
