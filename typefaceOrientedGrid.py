# --------------------------------
# --------------------------------
# Typeface oriented grid generator
# --------------------------------

from drawBot import _drawBotDrawingTool as db

FROM_MM_TO_PT = 2.834627813


def modularCut(maxWidth, columns) -> float:
    for layout_width in reversed(range(int(maxWidth))):
        columnWidth = (layout_width - line_height * (columns - 1)) / columns
        if (columnWidth > 0) and (columnWidth % line_height == 0):
            return columnWidth
    raise StopIteration


# ---------
# ---------
# Variables
# ---------
line_height = 12  # pt

# Margins
margin_external = line_height * 3
margin_internal = line_height * 3

margin_superior = line_height * 4
margin_inferior = line_height * 5

# Starting sheet dimensions
sheet_width, sheet_height = 210 * 2 * FROM_MM_TO_PT, 297 * FROM_MM_TO_PT

# Single page columns number
columns_number = 2

# ------------
# ------------
# Instructions
# ------------
if __name__ == "__main__":
    db.size(1500, 1500)

    db.stroke(0)
    db.fill(255)

    # Margins
    db.translate(50, 50)

    # Drawing sheet
    db.rect(0, 0, sheet_width, sheet_height)

    # calc modular layout and column
    column_width = modularCut(
        sheet_width / 2 - (margin_external + margin_internal), columns_number
    )
    layout_width = column_width * columns_number + line_height * (columns_number - 1)
    layout_height = modularCut(sheet_height - (margin_superior + margin_inferior), 1)

    # calc modular page dimensions
    page_width = (layout_width + margin_external + margin_internal) * 2
    page_height = layout_height + margin_inferior + margin_superior

    # bleed calc
    bleed_external = (sheet_width - page_width) / 2
    bleed_vertical = (sheet_height - page_height) / 2

    # moving canvas origin point
    db.translate(bleed_external, bleed_vertical)  # type: ignore

    # drawing page rect
    db.rect(0, 0, page_width, page_height)

    # drawing pages folding line
    db.line((page_width / 2, 0), (page_width / 2, page_height))

    # left layout
    db.rect(margin_external, margin_inferior, layout_width, layout_height)

    # right layout
    db.rect(
        page_width / 2 + margin_internal, margin_inferior, layout_width, layout_height
    )

    # baseline grid
    db.translate(0, margin_inferior)
    baselines = int((page_height - margin_inferior - margin_superior) / line_height)
    print(f"Baselines: {baselines}")
    for i in range(baselines):
        quota = i * line_height
        db.line(
            (margin_external, quota), (margin_external + layout_width, quota)
        )  # left
        db.line(
            (page_width / 2 + margin_internal, quota),
            (page_width / 2 + margin_internal + layout_width, quota),
        )  # right

    # left columns
    db.translate(margin_external, 0)
    db.fill(1, 1, 1, 0.8)  # type: ignore
    for i in range(columns_number):
        ascissa = i * column_width + line_height * (i - 1) + line_height
        db.rect(ascissa, 0, column_width, layout_height)

    # right columns
    db.translate(layout_width + margin_internal * 2, 0)  # type: ignore
    for i in range(columns_number):
        ascissa = i * column_width + line_height * (i - 1) + line_height
        db.rect(ascissa, 0, column_width, layout_height)

    # Printing output for indesign new document panel
    print(f"Width: {int(page_width / 2.0)} pt")
    print(f"Height: {page_height} pt")
    print()
    print(f"Margin internal: {margin_internal} pt")
    print(f"Margin external: {margin_external} pt")
    print(f"Margin superior: {margin_superior} pt")
    print(f"Margin inferior: {margin_inferior} pt")
    print()
    print("Bleed internal: 0 pt")
    print(f"Bleed external: {bleed_external} pt")
    print(f"Bleed superior: {bleed_vertical} pt")
    print(f"Bleed inferior: {bleed_vertical} pt")
