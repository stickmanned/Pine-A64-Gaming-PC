# Pine A64 Gaming PC

<table align="center">
  <tr>
    <td align="center"><b>Fusion 360 render</b></td>
    <td align="center"><b>Another angle</b></td>
    <td align="center"><b>Finished build</b></td>
  </tr>
  <tr>
    <td><img src="./Photos/cad_final_render_fan_angle.png" alt="Fusion 360 render of the enclosure from the fan side" width="260" /></td>
    <td><img src="./Photos/cad_final_render_button_angle.png" alt="Fusion 360 render of the enclosure from the power button side" width="260" /></td>
    <td><img src="./Photos/finished_case_fan_spinning.jpeg" alt="Finished Pine A64 computer with its fan spinning" width="260" /></td>
  </tr>
</table>

I turned an old Pine A64 single-board computer into a small [Moonlight](https://moonlight-stream.org/) game-streaming client. It runs DietPi, connects to my main gaming PC over Ethernet, and lives in a case that I designed and 3D printed. I also added a Noctua fan, copper heatsinks, and a real power button.

The idea started before Hack Club Horizons. I won the Pine A64 for placing second at the Equinox hackathon in Vancouver, but for a while it stayed in its original display case and collected dust. At the time, I was streaming games out of my room because my main PC made the room too hot. I realized I did not need another complete computer beside me just to receive a Moonlight stream. The Pine A64 already had Gigabit Ethernet and enough CPU power to at least try.

I later made it a [Hack Club Horizons](https://guides.horizons.hackclub.com/) project because I wanted to attend the hackathon, but the project itself was self-directed. This was a solo build.

- [Demo video: Roblox and BeamNG.drive streamed through Moonlight](https://photos.app.goo.gl/yZgWkz5E3pNsgPrR7)
- [Build log with 24 hourly entries](./Devlog.md)
- [Build session recordings](https://drive.google.com/drive/folders/1OZEimO6eNiohD2dQr07wJ2Tfkh4ZQb1m?usp=sharing)
- [Bill of materials](./Pine%20A64%20PC%20Bill%20of%20Materials.csv)
- [Project tracker](https://docs.google.com/spreadsheets/d/1We2MmTOR3fEgsacE6zURNgYWdwFos29sACSzlIPlyxY/edit?usp=sharing)

## How well it works

The finished computer is playable at about 20-30 FPS at 720p. That is not enough for a competitive game, but it works for slower story games. I was honestly surprised that a board this old could do it.

I experimented with hardware video decoding and left some of those settings in the tracked configuration, but I ran into video problems and the finished setup still relies mainly on CPU decoding. The Pine A64's video hardware and drivers are the main limit, not its Ethernet connection.

After power-on, the board performs its normal checks and then opens Moonlight automatically. On my build this takes about 10 seconds. The physical button can start or shut down the board without cutting power in the middle of a write to the microSD card.

## Why I kept working on it

This was my first real single-board computer project. I had used microcontrollers before, but I had never installed Linux without a desktop, worked directly with DRM/KMS, or tried to remove everything that was wasting performance on a low-end CPU.

The first successful desktop boot took more than six hours of troubleshooting. I was lying on the floor with my laptop in one hand and the Pine A64 connected to a monitor beside me. Most attempts ended in a black screen. When the desktop finally appeared, I jumped up because I had spent the whole day reading documentation, watching setup videos, changing files, and remotely connecting to the board whenever the display stopped working.

The random crashes turned out to be caused by a cheap microSD card. Replacing it fixed the problem. If I started again, checking the storage and other basic hardware would be my first step instead of my last.

The case caused a different kind of problem. My first fan mount had four pillars, which made it impossible to slide the Noctua fan into place. I tried three, then removed another one. The final two-pillar arrangement was the simplest fix and let me screw the fan in properly.

Putting the finished unit together was my favourite part. I had already spent about a dozen hours on the board and operating system, another five or six hours on the case and power button, and roughly two hours assembling everything. Closing the case made all of that work feel real.

## Repository contents

```text
├── CAD/                  Fusion 360, STL, and 3MF enclosure files
├── firmware-config/      DietPi boot, udev, and Moonlight autostart files
├── Hardware/             Wiring schematic
├── Photos/               CAD screenshots and build photos
├── Devlog.md             Hour-by-hour build notes
└── Pine A64 PC Bill of Materials.csv
```

## Hardware

| Part | What I used it for |
|---|---|
| Pine A64 2GB Rev B | The ARM64 computer running DietPi and Moonlight |
| Noctua NF-A6x25 FLX, 12V | Active cooling |
| MT3608 boost converter | Raises a 5V supply branch to 12V for the fan |
| Copper heatsinks | Extra cooling for the board |
| Cherry MX-compatible momentary switch | External power and shutdown button |
| M3 screws and threaded inserts | Fan and case mounting |
| Custom printed case | Holds the board, fan, wiring, and switch |
| Custom KeyV2 keycap | Fits the power-button opening and has a power symbol |

Prices, quantities, and source links are in the [bill of materials](./Pine%20A64%20PC%20Bill%20of%20Materials.csv).

## Wiring

There are two voltages in this build. The Pine A64 only receives 5V. The MT3608 raises a separate branch to 12V, and that output goes only to the Noctua fan.

I used a regulated 5V supply rated for at least 2A. The board can be powered through microUSB or through the Euler header's DC input pins: pin 2 or 4 for 5V, with pin 6 or 9 for ground. The MT3608 input is connected to the 5V supply in parallel so its fan current does not pass through the Pine A64.

[Open the complete wiring schematic](./Hardware/wiring-schematic.pdf).

```text
5V power supply
  ├── Pine A64 power input
  └── MT3608 IN+ and IN-

MT3608, adjusted to 12.0V before connecting the fan
  └── Noctua red wire to OUT+, black wire to OUT-
      Yellow tachometer wire disconnected and insulated

Momentary power switch
  └── EXP pin 5 (Pwr/Stb Sw) to EXP pin 6 (GND)
```

The switch is not wired in series with the main power input. Pressing it signals the board to start or shut down normally, which lowers the chance of corrupting the microSD card.

I did not design a custom PCB for this project. The electronics use point-to-point wiring between the Pine A64, boost converter, fan, and switch, so there are no Gerbers or KiCad files. The schematic is the hardware reference for this part of the build.

## Case files and print settings

The `CAD` folder contains:

- `P64-CASE.f3z`: editable Fusion 360 archive
- `P64-case-top-v1.4.1.stl` and `P64-case-bottom.stl`: case exports for slicing
- `P64-case-top-v1.4.1.3mf`: the print project used for the top shell
- `power-button-keycap-v3.stl`: the final keycap, made with [KeyV2](https://github.com/rsheldiii/keyv2) in OpenSCAD

These are the settings I used:

| Part | Printer | Material | Layer height | Infill | Supports |
|---|---|---|---:|---:|---|
| Top shell | Snapmaker U1 | Black Bambu PLA Basic | 0.20 mm | 10% gyroid | Normal/snug with Bambu Support for PLA |
| Bottom shell | Anycubic Kobra X | Wood JAYO PLA+ | 0.16 mm | 15% gyroid | None |
| Power keycap | Either printer | PLA | 0.12-0.20 mm | 20% | None |

The final top-shell file includes the fan-mount changes I made after the fit tests. More details are in [Hour 24 of the devlog](./Devlog.md#hour-24-finalized-cad-renders-print-settings--assembly-instructions).

## Software setup

The exact files from my DietPi setup are in [firmware-config](./firmware-config). The installer backs up the existing files, adds `video=HDMI-A-1:1920x1080@60` to the boot environment, installs the udev rule for DRM and input access, and appends the Moonlight launch block to the DietPi user's `.bashrc`. Limiting the HDMI mode before Linux starts kept the Allwinner A64 DRM/KMS stack from using up the CMA memory pool during initialization.

### 1. Flash DietPi

Download a [DietPi](https://dietpi.com/) image for the Allwinner A64 and write it to a reliable microSD card with a tool such as [BalenaEtcher](https://etcher.balena.io/). Complete the first-run setup over SSH. I also learned to connect my USB keyboard and mouse before turning on the board because hot-plugging them caused brownout resets during setup.

I would strongly recommend starting with a known-good card. A bad one cost me hours because the resulting crashes looked like an operating-system problem.

### 2. Prepare Moonlight

Install `moonlight-qt` and pair it with the host gaming PC:

```bash
moonlight pair <HOSTNAME_OR_IP>
```

I removed XFCE and LightDM so Moonlight could use the direct DRM/KMS path without a full desktop running behind it:

```bash
sudo systemctl mask lightdm
sudo apt purge 'xfce4*' 'lightdm*' -y
sudo apt autoremove -y
sudo systemctl set-default multi-user.target
```

### 3. Apply the tracked configuration

Copy this repository to the Pine A64, then run:

```bash
cd firmware-config
chmod +x install.sh
sudo ./install.sh
```

The script creates backups before changing `/boot/dietpiEnv.txt`, `/home/dietpi/.bashrc`, or `/etc/udev/rules.d/99-kms.rules`. After it finishes, replace `<HOSTNAME_OR_IP>` in `/home/dietpi/.bashrc` with the address of the gaming PC.

I used `modetest` to check that the DRM device and Allwinner display engine were detected before trying Moonlight:

```bash
modetest
```

The tracked launch block requests 1080p/60 FPS and enables the hardware-decoder flag because those were settings I tested. My final reliable result was closer to 720p at 20-30 FPS with mostly CPU decoding, so lower the stream resolution and frame rate if the board cannot keep up.

Reboot when the configuration is ready:

```bash
sudo reboot
```

On the main TTY, Moonlight should launch after the display and input devices finish initializing. SSH sessions do not trigger the autostart block.

## Assembly

1. Install the copper heatsinks before putting the board into the case.
2. Print the top, bottom, and power-button keycap from the files in `CAD`.
3. Mount the Noctua fan using the two usable screw pillars, with its airflow aimed at the heatsinks.
4. With the fan still disconnected, power the MT3608 input and adjust its output to exactly 12.0V using a multimeter.
5. Disconnect power. Wire the fan to the MT3608 output and the switch to EXP pins 5 and 6.
6. Add strain relief and keep the wires away from the fan blades.
7. Seat the Pine A64 in the bottom shell, close the case, and install the four bottom M3 screws.
8. Connect HDMI, Ethernet, and any USB input devices. Power it on and check the fan, button, DietPi boot, and Moonlight stream.

The [devlog safety checklist](./Devlog.md#hour-23-ship-ready-wiring-schematic--electrical-safety-review) has the longer version I used before the first full power test.

<table align="center">
  <tr>
    <td><img src="./Photos/final_assembly_fan_and_board.jpeg" alt="Noctua fan and Pine A64 before the case was closed" width="240" /><br/><sub>Fan and board</sub></td>
    <td><img src="./Photos/cable_management_hot_glue.jpeg" alt="Wiring secured inside the case" width="240" /><br/><sub>Cable management</sub></td>
    <td><img src="./Photos/moonlight_streaming_verified.jpeg" alt="Moonlight streaming on the completed computer" width="240" /><br/><sub>Streaming test</sub></td>
  </tr>
</table>

## Safety

- Never connect the MT3608's 12V output to the Pine A64. The board is 5V only.
- Measure the boost converter output before attaching the fan.
- Insulate the fan's unused yellow tachometer wire.
- Only connect the momentary switch across EXP pins 5 and 6. Do not put it in the main 5V line.
- Unplug the power supply before soldering or changing the wiring.
- Let the soldering iron and hot glue gun cool before handling them.
- This build has no lithium battery and no mains voltage inside the case.

## What I learned

I can now install and configure DietPi on a single-board computer, work through a headless Linux setup, change startup scripts, and strip away a desktop environment when it is slowing down the only program I need. I also learned to verify old-board documentation instead of trusting the first search result. Some AI-assisted search answers hallucinated details about this board and sent me toward more errors, so I started double-checking them against documentation and actual tests.

Most importantly, the Pine A64 has a purpose again. I could have bought a newer streaming box, but that would have missed the point. I wanted to see how much useful work I could still get out of hardware I already owned.

## AI use

I used AI-assisted search and writing tools during this project. They helped me find possible troubleshooting directions, organize some early plans, and clean up parts of the devlog and repository text. They were not always correct, especially with this older board, so I checked suggestions against documentation and tested them myself.

I did all of the CAD work, soldering, wiring, assembly, Linux setup, and physical debugging. The observations in this README, including the failed SD card, six-hour display problem, case iterations, boot time, and final streaming performance, come from my own build.

## License

See [LICENSE](./LICENSE).
