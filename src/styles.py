from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("Lato", "fonts/Lato-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Lato-Bold", "fonts/Lato-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Lato-Italic", "fonts/Lato-Italic.ttf"))
pdfmetrics.registerFontFamily(
    "Lato",
    normal="Lato",
    bold="Lato-Bold",
    italic="Lato-Italic",
)

url_color = "royalblue"

def get_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="Name",
            parent=styles["Heading1"],
            fontName="Lato-Bold",
            fontSize=18,
            spaceBefore=0,
            spaceAfter=3,
        )
    )

    styles.add(
        ParagraphStyle(
            name="JobTitle",
            parent=styles["Heading2"],
            fontName="Lato-Bold",
            fontSize=13,
            spaceBefore=6,
            spaceAfter=12,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Page1Section",
            parent=styles["Heading2"],
            fontName="Lato-Bold",
            fontSize=12,
            leading=14,
            spaceBefore=18,
            spaceAfter=12,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["Normal"],
            fontName="Lato",
            fontSize=9,
            leading=11,
            spaceAfter=4,
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyBold",
            parent=styles["Body"],
            fontName="Lato-Bold",
        )
    )

    styles.add(ParagraphStyle(
        name="ExperienceHeader",
        parent=styles["Body"],
        fontName="Lato-Bold",
        fontSize=11,
        leading=13,
        spaceAfter=2,
    ))

    styles.add(ParagraphStyle(
        name="ExperienceMeta",
        parent=styles["Body"],
        fontName="Lato",
        fontSize=9,
        leading=10,
        spaceAfter=9,
    ))

    styles.add(ParagraphStyle(
        name="ExperienceSection",
        parent=styles["Body"],
        fontName="Lato-Bold",
        fontSize=9,
        leading=13,
        spaceBefore=6,
        spaceAfter=0,
    ))

    styles.add(ParagraphStyle(
        name="Footer",
        parent=styles["Body"],
        fontName="Lato",
        fontSize=7,
        textColor=colors.grey,
        spaceBefore=0,
        spaceAfter=0,
    ))

    styles.add(
        ParagraphStyle(
            name="OtherSection",
            parent=styles["Heading2"],
            fontName="Lato-Bold",
            fontSize=12,
            leading=14,
            spaceBefore=12,
            spaceAfter=6,
        )
    )

    return styles

