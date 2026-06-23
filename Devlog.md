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
