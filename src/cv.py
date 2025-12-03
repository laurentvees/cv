from reportlab.platypus import SimpleDocTemplate, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import json

from styles import get_styles
from layout import (
    info_table, p, space, ps, bs, experience_block, expertise_block, make_footer, personal_block
)

def build_cv(path: str, show_grid=True, redacted=False):
    with open("src/cv.json") as file:
        CV = json.load(file)

    styles = get_styles()
    footer = make_footer(CV["footer"], styles["Footer"])
    story = []

    ## Page 1

    story.append(p(CV["name"], styles["Name"]))
    story.append(p(CV["title"], styles["JobTitle"]))
    story.append(space(8))

    info = info_table(CV["basics"], styles, show_grid=show_grid, redacted=redacted)
    story.append(info)
    # story.append(space(12))

    story.append(p("Executive Summary", styles["Page1Section"]))
    story.extend(ps(CV["summary"], styles["Body"]))

    story.append(p("Core Strengths", styles["Page1Section"]))
    story.extend(bs(CV["strengths"], styles["Body"]))

    story.append(p("Expertise", styles["Page1Section"]))
    story.append(expertise_block(CV["expertise"], styles))

    story.append(p("Key Achievements", styles["Page1Section"]))
    story.extend(bs(CV["achievements"], styles["Body"]))

    story.append(PageBreak())

    ## Page 2

    story.extend(experience_block(CV["experiences"][0], styles, wide=True))
    story.append(space(12))
    story.extend(experience_block(CV["experiences"][1], styles, wide=True))
    story.append(space(12))
    story.extend(experience_block(CV["experiences"][2], styles, wide=True))
    story.append(space(12))
    story.extend(experience_block(CV["experiences"][3], styles, wide=True))

    story.append(PageBreak())

    ## Page 3

    story.extend(experience_block(CV["experiences"][4], styles))
    story.append(space(6))
    story.extend(experience_block(CV["experiences"][5], styles))
    story.append(space(6))
    story.extend(experience_block(CV["experiences"][6], styles))

    story.append(p("Personal Projects", styles["OtherSection"]))
    story.extend(personal_block(CV["personal_projects"], styles))
    story.append(p("Volunteering", styles["OtherSection"]))
    story.extend(personal_block(CV["volunteering"], styles))
    story.append(p("Interests", styles["OtherSection"]))
    story.append(p(CV["interests"], styles["Body"]))

    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm,
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--redacted", default=False)
    args = parser.parse_args()

    redacted = args.redacted
    if redacted:
        out_file = "CV Laurent Van Eesbeeck - Redacted.pdf"
    else:
        out_file = "CV Laurent Van Eesbeeck.pdf"

    build_cv(out_file, show_grid=False, redacted=redacted)

