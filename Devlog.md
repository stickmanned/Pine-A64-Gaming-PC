# Engineering Devlog: Pine A64 Gaming PC

Welcome to the engineering devlog for the Pine A64 Gaming PC project. This document serves as the repository for progress logs, design choices, component testing, and build records as we transform the Pine A64 single-board computer into a custom-cooled, custom-enclosed gaming PC.

Here is the spreadsheet which organizes the entire project:https://docs.google.com/spreadsheets/d/1We2MmTOR3fEgsacE6zURNgYWdwFos29sACSzlIPlyxY/edit?usp=sharing

---

## 🛠️ Hour 1: Project Teardown & Component Sourcing

* **Date:** June 22, 2026
* **Time Spent:** 1 Hour
* **Project Phase:** Stage 1 — Hardware Inspection & BOM Sourcing

### 📋 Activity Summary
Removed the pre-existing stock acrylic enclosure from the Pine A64 to expose the bare board. Finalized the engineered Bill of Materials (BOM) for the 12V active cooling system and ordered the MT3608 boost converter, copper heatsinks, and wiring hardware.

### 🔍 Engineering Notes
> [!NOTE]
> The original acrylic mounting hardware was kept and carefully stored. The thread pitches will be cross-referenced with planned M3 heat-set inserts to ensure compatibility during the custom enclosure design.

### 🖼️ Media & Sourcing Logs

#### 1. Bare-Board Teardown
Exposed Pine A64 board (Rev B, 2016-03-21) ready for thermal measurements and custom mount planning:
![Pine A64 Bare Board Teardown](./Photos/teardown_bare_board.jpg)

#### 2. Active Cooling Fan
A Noctua NF-A6x25 FLX 12V DC (0.96W, 0.08A) fan will be integrated to provide high-static-pressure, low-noise active cooling:
![Noctua 12V Fan](./Photos/noctua_fan.jpg)

#### 3. Sourced Bill of Materials (BOM)
Order placed for essential power management, thermal, and prototyping hardware:
![Amazon Sourcing Shopping Cart](./Photos/bom_sourcing_cart.png)

---

## 🛠️ Hour 2: Documentation Review & Pinout Architecture Analysis

* **Date:** June 22, 2026
* **Time Spent:** 1 Hour
* **Project Phase:** Stage 1 — Hardware Inspection & BOM Sourcing

### 📋 Activity Summary
Researched the Pine A64 hardware by watching unboxing tutorials and reviewing the official PINE64 documentation. Mapped out the exact pins needed for the custom cooling fan and the external power button.

### 🔍 Engineering Notes
* **Pi-2 Bus (40-pin header):** Found the power pins for the cooling system. Pins 2 and 4 provide 5V power, and Pin 6 is Ground (GND). These will connect to the MT3608 boost converter.
* **Euler Bus (34-pin header):** Found the hardware power switch pins. Pin 27 (PB2) and Pin 34 (GND) will connect to the external momentary tactile button.

### 🔗 Reference Links
* [PINE_A64 Wiki](https://wiki.pine64.org/wiki/PINE_A64)
* [Pine A64 Schematic & Pin Assignment PDF](https://files.pine64.org/doc/Pine%20A64%20Schematic/Pine%20A64%20Pin%20Assignment%20160119.pdf)
* [PINE64 official Schematics & Certifications Documentation](https://pine64.org/documentation/Pine_A64/Further_information/Schematics_and_certifications/)
* [Pine A64 Tutorial/Unboxing Reference 1](https://www.youtube.com/watch?v=4FUbQ5n3BIg)
* [Pine A64 Tutorial/Unboxing Reference 2](https://www.youtube.com/watch?v=FxGeloh80RQ)

---

## 🛠️ Hour 3: OS Selection, Flashing, & Initial Boot Diagnostics

* **Date:** June 24, 2026
* **Time Spent:** 1 Hour
* **Project Phase:** Stage 2 — OS Setup & Initial Diagnostic Testing

### 📋 Activity Summary
Selected DietPi as the core operating system to minimize background processing and maximize network stability for PC game streaming (Moonlight). Flashed the OS image using BalenaEtcher. Initiated the first boot sequence but encountered immediate HDMI display failures and random system halts.

### 🔍 Engineering Notes
* **Initial Boot Failures (Black Screen):** Diagnosed as potential voltage sags (brownouts) caused by peripheral power spikes.
* **USB Hotplug Brownouts:** Investigated by cold-plugging a keyboard before applying power to bypass capacitor draw spikes.
* **HDMI Handshake Failure:** Realized the HDMI handshake was failing due to resolution mismatches, requiring a pivot to a headless (SSH) configuration approach.


---

## 🛠️ Hour 4: Network Diagnostics, Subnet Sweeping, & Hardware Isolation

* **Date:** June 24, 2026
* **Time Spent:** 1 Hour
* **Project Phase:** Stage 2 — Headless Diagnostics & Hardware Isolation Testing

### 📋 Activity Summary
Attempted to establish a headless SSH connection to bypass the broken HDMI output. Upgraded the power delivery system to an Anker GaNPrime 100W brick to rule out amperage deficits. Performed advanced subnet sweeping to track down the board's IP address. Concluded with a bare-board isolation test.

### 🔍 Engineering Notes
* **Network Topology Issue:** Discovered the local OpenWrt router overrides the default `.local` mDNS protocol in favor of `.lan`. Wrote a custom bash loop to brute-force map the subnet:
  ```bash
  for ip in {1..254}; do ping -c 1 -W 50 192.168.1.$ip &> /dev/null & done; sleep 2; arp -a
  ```
* **MAC Address Analysis:** Successfully identified the board's dynamic IP (`192.168.1.250`) by analyzing the locally administered MAC address (`2:ba:3e:cd:49:25`) generated by DietPi.
* **Isolation Test & Power Delivery:** Despite the Anker 100W GaN upgrade, continuous pings showed 100% packet loss, indicating a recurring physical crash. Conducted a "Bare Board Isolation Test" (power only, no SD card). This proved that either the Micro-USB cable's electrical resistance is too high, or the MicroSD card itself is spiking power draw / physically corrupted, preventing the bootloader from executing.

