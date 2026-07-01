#!/usr/bin/env python3

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Hardware" / "wiring-schematic.pdf"


def box(c, x, y, w, h, title, lines, fill):
    c.setStrokeColor(colors.HexColor("#222222"))
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, 8, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#111111"))
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 12, y + h - 22, title)
    c.setFont("Helvetica", 9)
    text_y = y + h - 40
    for line in lines:
        c.drawString(x + 12, text_y, line)
        text_y -= 13


def line(c, x1, y1, x2, y2, color, width=3, label=None, label_dx=0, label_dy=0):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)
    if label:
        c.setFillColor(colors.HexColor("#f8fafc"))
        c.setFont("Helvetica-Bold", 8)
        c.drawString((x1 + x2) / 2 + label_dx, (y1 + y2) / 2 + label_dy, label)


def make_pdf():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=landscape(letter))
    page_w, page_h = landscape(letter)

    c.setTitle("Pine A64 Gaming PC Wiring Schematic")

    c.setFillColor(colors.HexColor("#0f172a"))
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(36, page_h - 46, "Pine A64 Gaming PC - Wiring Schematic")

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#dbeafe"))
    c.drawString(
        36,
        page_h - 65,
        "Exported reviewer schematic matching README.md. No custom PCB; point-to-point low-voltage wiring only.",
    )

    rail_red = colors.HexColor("#dc2626")
    rail_black = colors.HexColor("#94a3b8")
    rail_orange = colors.HexColor("#f97316")
    signal_blue = colors.HexColor("#2563eb")

    psu = (50, 305, 145, 86)
    pine = (470, 305, 245, 130)
    mt = (280, 150, 190, 110)
    fan = (565, 155, 150, 90)
    switch = (515, 455, 150, 68)

    box(
        c,
        *psu,
        "5 V PSU",
        ["Regulated 5.0 V DC", "Recommended: 2 A or more", "Feeds board and MT3608 input"],
        colors.HexColor("#e0f2fe"),
    )
    box(
        c,
        *pine,
        "Pine A64 board",
        [
            "5 V input: microUSB",
            "or Euler pin 2/4 to GND pin 6/9",
            "EXP pin 5: Pwr/Stb Sw",
            "EXP pin 6: GND",
            "Board never receives 12 V",
        ],
        colors.HexColor("#dcfce7"),
    )
    box(
        c,
        *mt,
        "MT3608 boost converter",
        [
            "IN+ / IN- from 5 V PSU rail",
            "Adjust OUT before fan is connected",
            "Target output: 12.0 V DC",
        ],
        colors.HexColor("#fef9c3"),
    )
    box(
        c,
        *fan,
        "Noctua fan",
        ["NF-A6x25 FLX", "Red: +12 V", "Black: GND", "Yellow tach: insulated"],
        colors.HexColor("#ffedd5"),
    )
    box(
        c,
        *switch,
        "Power key switch",
        ["Momentary normally-open", "Shorts EXP pin 5 to pin 6", "Not in series with 5 V rail"],
        colors.HexColor("#dbeafe"),
    )

    # 5 V rail split.
    line(c, 195, 360, 470, 360, rail_red, label="5 V+", label_dy=7)
    line(c, 195, 330, 470, 330, rail_black, label="GND", label_dy=-13)
    line(c, 195, 345, 280, 215, rail_red, label="5 V+ to IN+", label_dx=-18, label_dy=15)
    line(c, 195, 320, 280, 185, rail_black, label="GND to IN-", label_dx=-12, label_dy=-18)

    # Boosted fan rail.
    line(c, 470, 210, 565, 210, rail_orange, label="12.0 V OUT+", label_dy=8)
    line(c, 470, 185, 565, 185, rail_black, label="OUT- / GND", label_dy=-13)

    # Switch signal pair.
    line(c, 590, 455, 590, 435, signal_blue, width=2)
    line(c, 590, 435, 590, 435, signal_blue, width=2)
    line(c, 590, 435, 610, 435, signal_blue, width=2)
    line(c, 610, 435, 610, 415, signal_blue, width=2)
    line(c, 630, 455, 630, 415, rail_black, width=2)

    # Callouts.
    c.setFillColor(colors.HexColor("#ffffff"))
    c.roundRect(36, 36, page_w - 72, 85, 8, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#111111"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(52, 96, "Pre-power checklist")
    c.setFont("Helvetica", 9)
    checklist = [
        "1. Verify PSU is about 5.0 V DC.",
        "2. Verify MT3608 input polarity before power.",
        "3. Adjust MT3608 OUT+/OUT- to 12.0 V before connecting the fan.",
        "4. Connect fan red to OUT+, black to OUT-, and insulate the yellow tach wire.",
        "5. Verify the key switch only shorts EXP pin 5 to EXP pin 6 when pressed.",
        "6. Confirm no 12 V conductor can touch any Pine A64 header or board input.",
    ]
    x = 52
    y = 78
    for item in checklist[:3]:
        c.drawString(x, y, item)
        y -= 14
    x = 380
    y = 78
    for item in checklist[3:]:
        c.drawString(x, y, item)
        y -= 14

    c.setFillColor(colors.HexColor("#fef2f2"))
    c.roundRect(50, 430, 300, 52, 8, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#991b1b"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(66, 463, "Golden rule")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(66, 446, "5 V powers the Pine A64. 12 V powers only the fan.")

    c.setFillColor(colors.HexColor("#dbeafe"))
    c.setFont("Helvetica", 8)
    c.drawRightString(page_w - 36, 18, "Source: README.md wiring section and Devlog Hour 23")

    c.showPage()
    c.save()


if __name__ == "__main__":
    make_pdf()
    print(OUT)
