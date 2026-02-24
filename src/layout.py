import re
from datetime import datetime, UTC
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from typing import Union
from styles import url_color


# Text primitives
def bold(text: str):
    return f"<b>{text}</b>"


def italic(text: str):
    return f"<i>{text}</i>"


def url(text: str, link: Union[str, None] = None):
    if not link:
        link = text
    return f"<a href='{link}' color='{url_color}'>{text}</a>"


def parse_markup(s: str):
    patterns = [
        (r"\*\*(.+?)\*\*", lambda m: bold(m.group(1))),
        (r"__(.+?)__", lambda m: italic(m.group(1))),
        (r"\[(.+?)\]\((.+?)\)", lambda m: url(m.group(1), m.group(2))),
    ]

    changed = True
    while changed:
        changed = False
        for pattern, repl in patterns:
            new_s = re.sub(pattern, repl, s)
            if new_s != s:
                changed = True
                s = new_s
    return s


# ReportLab primitives
def space(h):
    return Spacer(1, h)


def p(text, style, bullet=None):
    return Paragraph(parse_markup(text), style, bulletText=bullet)


def b(text, style):
    return p(text, style, bullet="•")


def ps(texts: list[str], style):
    return [p(text, style) for text in texts]


def bs(texts: list[str], style, top_space=0, bottom_space=0):
    ts = space(top_space)
    items = [b(item, style) for item in texts]
    bs = space(bottom_space)
    return [ts, *items, bs]


def base_table(data, col_widths=None, top_padding=0, show_grid=False):
    t = Table(data, colWidths=col_widths, hAlign="LEFT")
    style_cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), top_padding),
        ("TOPPADDING", (0, 0), (-1, 0), 0),  # ignore padding on 1st row
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]
    if show_grid:
        style_cmds.append(("GRID", (0, 0), (-1, -1), 0.25, colors.black))
    t.setStyle(TableStyle(style_cmds))
    return t


# CV primitives
def make_footer(footer_text: str, style):
    left_style = style.clone('footer_left')
    left_style.alignment = TA_LEFT

    mid_style = style.clone('footer_mid')
    mid_style.alignment = TA_CENTER

    right_style = style.clone('footer_right')
    right_style.alignment = TA_RIGHT

    timestamp = datetime.now(UTC).strftime("%d %B %Y")

    def footer(canvas, doc):
        canvas.saveState()

        left_p = p(f"Page {doc.page}", left_style)
        mid_p = p(footer_text, mid_style)
        right_p = p(f"CV Version — {timestamp}", right_style)

        data = [[left_p, mid_p, right_p]]

        table = Table(
            data,
            colWidths=[3*cm, 10*cm, 4*cm]
        )

        table.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ]
            )
        )

        w, h = table.wrap(doc.width, doc.bottomMargin)
        table.drawOn(canvas, doc.leftMargin, h + 0.25 * cm)

        canvas.restoreState()

    return footer


def info_table(info, styles, show_grid=False, redacted=False):
    def lang_table(d):
        rows = [[p(k, styles["Body"]), p(v, styles["Body"])] for k, v in d.items()]
        return base_table(rows, [2.5 * cm, 2 * cm], show_grid=show_grid)

    def side_table(d, col_widths, redacted=False):
        rows = []
        for label, value in d.items():
            if label == "Languages":
                rows.append([p(label, styles["BodyBold"]), lang_table(value)])
            else:
                if redacted:
                    rows.append(
                        [p(label, styles["BodyBold"]), p("", styles["Body"])]
                    )
                else:
                    rows.append(
                        [p(label, styles["BodyBold"]), p(value, styles["Body"])]
                    )
        return base_table(rows, col_widths, top_padding=6, show_grid=show_grid)

    left = side_table(info["left"], [2.5 * cm, 4.5 * cm], redacted=redacted)
    right = side_table(info["right"], [2.5 * cm, 7 * cm])

    if redacted:
        note = p(info["redacted_note"], styles["Body"])
        left = base_table(
            [[left], [note]],
            show_grid=show_grid,
            top_padding=6,
        )

    info = base_table([[left, right]], [8 * cm, 8 * cm], show_grid=show_grid)

    return info

# def expertise_block(data, styles):
    # out = []
    # for category, items in data.items():
    #     header = p(category, styles["BodyBold"])
    #     line = ", ".join(items)
    #     out.append(header)
    #     out.append(p(line, styles["Body"]))
    # return out
def expertise_block(data, styles, n_cols=2):
    categories = list(data.items())
    rows = [[] for _ in range(n_cols)]

    for i, (category, lines) in enumerate(categories):
        col = i % n_cols
        header = p(category, styles["BodyBold"])
        lines = [p(line, styles["Body"]) for line in lines]
        rows[col].append(header)
        rows[col].extend(lines)
        rows[col].append(space(4))

    table = Table(
        [rows],
        colWidths=[8*cm, 8*cm],
        hAlign="LEFT"
    )
    table.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))

    return table

def experience_block(experience, styles, wide=False, show_grid=False):
    title = f"{experience['company']} —  {experience['role']}"
    if 'department' in experience:
        title = f"{title} ({experience['department']})"

    header = base_table(
        [
            [
                p( title, styles["ExperienceHeader"]),
                p(experience["dates"], styles["ExperienceHeader"]),
            ]
        ],
        col_widths=[13.25*cm, 4 * cm], show_grid=show_grid
    )

    meta_items = []
    for label, value in experience.get("meta", {}).items():
        if isinstance(value, list):
            v = ", ".join(value)
        else:
            v = value
        meta_items.append(f"**{label}**&nbsp;&nbsp;{v}")

    meta_line = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join(meta_items)
    meta = p(meta_line, styles["Body"])

    context_block = ps(experience.get("context", []), styles["Body"])

    tasks_block = bs(
        experience.get("tasks", []), styles["Body"], top_space=2, bottom_space=6
    )

    out = []
    out.append(header)
    out.append(space(3))
    if wide:
        out.append(space(3))
    out.append(meta)
    if wide:
        out.append(space(3))
    out.append(p("Context", styles["ExperienceSection"]))
    out.extend(context_block)
    out.append(p("Tasks & Responsibilities", styles["ExperienceSection"]))
    out.extend(tasks_block)

    return out

def personal_block(data, styles):
    out = []
    for item in data:
        out.append(p(f"{item['title']} ({item['dates']})", styles["ExperienceSection"]))
        out.append(p(item["summary"], styles["Body"]))
    return out
