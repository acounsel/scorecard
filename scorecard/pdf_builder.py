import csv
import reportlab

from django.conf import settings
from django.http import HttpResponse

from reportlab import platypus
from reportlab.platypus import Paragraph, KeepTogether, Frame, KeepInFrame
from reportlab.platypus import Spacer, Image, Table, TableStyle, SimpleDocTemplate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import landscape, letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, StyleSheet1
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.units import mm, inch, cm

from .task import pdf_creator

s3_url = 'https://scorecard-static.s3-us-west-1.amazonaws.com/'
url_loc = 'media/public/'
file_url = s3_url + url_loc
col_widths = [30, 81, 174, 290, 60, 47, 47]

table_styles = {
    'header': [
        ("GRID", (0, 0), (-1, -1), 0.2*mm, '#a0a0a4'),
        ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('HALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), '#70747c'),
    ],
    'body': [
        ("GRID", (0, 0), (-1, -1), 0.2 * mm, '#a0a0a4'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('HALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 6), (-1, 7), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ],
    'category': [
        ("GRID", (0, 0), (-1, -1), 0.2*mm, '#a0a0a4'),
        ('SPAN', (0, 0), (6, 0)),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, 0), '#007D8A'),
    ],
    'category2': [
        ("GRID", (0, 0), (-1, -1), 0.2*mm, '#a0a0a4'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('HALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ]
}
# reportlab.rl_config.TTFSearchPath.append(
#     'https://scorecard-static.s3-us-west-1.amazonaws.com/media/public/'
# )
reportlab.rl_config.TTFSearchPath.append(str(settings.BASE_DIR))

pdfmetrics.registerFont(TTFont("Fjalla-One", "FjallaOne-Regular.ttf"))
pdfmetrics.registerFont(TTFont("NotoSansMongolian", "NotoSansMongolian-Regular.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))

def _header(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Header
    header_url = 'Accountability+Counsel_Logo_Color+(2).png'
    header = Image('{0}{1}'.format(
        file_url, header_url), width=112.3, height=29)
    header.hAlign = 'RIGHT'

    w, h = header.wrap(doc.width, doc.topMargin)
    header.drawOn(canvas, w + 530, doc.height + doc.topMargin - h)

    # Release the canvas
    canvas.restoreState()


class PageNumbers(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.setFont("Helvetica", 12)
        self.drawRightString(
            260 * mm, (0.4 * inch),
            str(self._pageNumber)
        )

def get_field(obj, field, language):
    return getattr(obj, '{}_{}'.format(field, language))

def export_pdf(ov_id, language='en'):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=commitments.pdf'
    pdf = pdf_creator.delay(ov_id, language, response)
    return response

def create_pdf(overview, language, response):
    image = '{}Accountability+Counsel_Logo_Color+(2).png'.format(
        file_url)
    styles = get_styles()
    # Create PDF
    pdf = SimpleDocTemplate(response, showBoundary=0, 
        leftMargin=0.9 * cm, rightMargin=0.9*cm, topMargin=2.5*cm, 
        bottomMargin=1*cm, pagesize=landscape(letter))

    # Create header with titles and legend
    story = create_header(overview, language, 
        styles['title_style'], styles['subtitle1_style'], 
        styles['subtitle2_style']) 
    counter = 2
    #create header row
    table = get_table_header(
        language, styles['header_style'])
    story = set_table(table, table_styles['header'], story)
    total_data = []
    category_bools = get_category_bools()
    #iterate through data
    for commitment in overview.commitment_set \
    .select_related('category').prefetch_related('status_set'):
        #Input the category row
        category_bools, new = category_header_check(
            commitment, category_bools)
        if new: 
            total_data, story = add_category_header(counter, 
                commitment, total_data, story, language, 
                styles['category_style'])
            counter += 1
        row_data = get_commitment_row(commitment, language, 
            styles['Breadpointlist_style'])
        total_data.append(row_data)
    table = Table(total_data, colWidths=col_widths)
    story = set_table(table, table_styles['body'], story)
    #Build PDF with logo header and page numbers
    pdf.build(story, onFirstPage=_header, onLaterPages=_header,
                  canvasmaker=PageNumbers)
    return pdf

def get_styles():
    #Create all different font styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='header_style',
        fontName='DejaVuSans',
        fontSize=11,
        textColor=colors.HexColor('#FFFFFF')))
    styles['header_style'].alignment = TA_CENTER
    styles.add(ParagraphStyle(
        name='category_style',
        fontName='DejaVuSans',
        fontSize=20,
        leftIndent=13,
        textColor=colors.HexColor('#FFFFFF')))
    styles.add(ParagraphStyle(
        name='Breadpointlist_style',
        fontName='DejaVuSans',
        fontSize=7,
        leading=12,
        wordWrap='LTR',))
    styles.add(ParagraphStyle(
        name='title_style',
        fontName='DejaVuSans',
        fontSize=30,
        textColor=colors.HexColor("#1ca4bc")))
    styles.add(ParagraphStyle(
        name='subtitle1_style',
        fontName='DejaVuSans',
        fontSize=12))
    styles.add(ParagraphStyle(
        name='subtitle2_style',
        fontName='DejaVuSans',
        fontSize=11))
    return styles

def create_header(overview, language, title_style, style1, style2):
    story = []
    story.append(Paragraph("<strong>{}</strong>".format(
        get_field(overview, 'name', language)), 
        title_style)
    )
    story.append(Spacer(1,.30*inch))
    story.append(Paragraph("<strong>{}</strong>".format(
        get_field(overview, 'subtitle', language)), style1))
    story.append(Spacer(1,.18*inch))
    if language == 'mn':
        h3 = "<strong>Үүрэг Амлалтын Хэрэгжилтийн Байдал 2020</strong>"
        img = Image('{}status_key.jpg'.format(file_url), width=480, height=41.076)
    else:
        h3 = "<strong>Status of Commitments as of May 2020</strong>"
        img = Image('{}graphics.jpg'.format(file_url), width=360, height=41.076)
    story.append(Paragraph(h3, style2))
    img.hAlign = 'RIGHT'
    story.append(img)
    return story

def set_table(table, styling, story):
    style = TableStyle(styling)
    table.setStyle(style)
    story.append(table)
    return story

def get_table_header(language, style):
    row_data = get_title_data(language, style)
    table = Table(row_data, 
        colWidths=col_widths, 
        rowHeights=[60]
    )
    return table

def get_title_data(language, style):
    row_data = []
    if language == 'mn':
        headers = ('#', 'Үүрэг Амлалтууд', 
            'нэ Үүрэг Амлалтын Тухай', 'Үүрэг Амлалтын Хэрэгжилтийн Байдал',
            'Анх Товлосон Хугацаа', '2019', '2020'
        )
    else:
        headers = ('#', 'Commitment', 'About the Commitment',
        'Status of Commitment', 'Original Timeline', '2019 Status',
        '2020 Status')
    for header_text in headers:
        row_data.append(
            Paragraph(
                '''<b>{}</b>'''.format(header_text), style
            )
        )
    return [row_data,]

def get_category_bools():
    return {
        'Pasture': False,
        'Water': False,
        'Monitoring': False,
        'Individual Compensation': False,
        'Animal Husbandry Development': False,
        'Collective Compensation': False,
        'Undai River Diversion': False,
    }

def category_header_check(commitment, category_bools):
    # Use bools to track the first instance of the category
    new_category = False
    for key, value in category_bools.items():
        if key == commitment.category.name and value == False:
            category_bools[key] = True
            new_category = True
    if new_category:
        return category_bools, True
    return category_bools, False

def add_category_header(counter, commitment, total_data, 
    story, language, style):
    if counter > 2:
        table = Table(total_data, colWidths=col_widths)
        story = set_table(table, table_styles['category2'], story)
        total_data = []
    row_data = []
    row_data.append(Paragraph(
        get_field(commitment.category, 'name', language), 
        style))
    for i in range(0, 6):
        row_data.append(Paragraph("", style))
    total_data.append(row_data)
    table = Table(total_data, colWidths=col_widths, 
        rowHeights=[35])
    story = set_table(table, table_styles['category'], story)
    total_data = []
    return total_data, story

def get_commitment_row(commitment, language, style):
    order = Paragraph(
        str(commitment.order_num) + commitment.order_letter,
        style)
    name = get_commitment_name(commitment, language, style)
    description = platypus.Paragraph(
        get_field(commitment, 'description', language), style)
    status = get_commitment_status(commitment, language, style)
    timeline = Paragraph(
        get_field(commitment, 'original_timeline', language), 
        style
    )
    statuses = commitment.status_set.order_by('date')[:2]
    row_data = [order, name, description, status, timeline]
    row_data.extend(get_status_displays(statuses, style))
    return row_data

def get_commitment_name(commitment, language, style):
    name = get_field(commitment, 'name', language)
    if "href" in name:
        name = name.replace("\">", "\" color=\"#2171c7\"><u>")
        name = name.replace("</a>", "</u></a>")
    return platypus.Paragraph(name, style)

def get_commitment_status(commitment, language, style):
    status = get_field(commitment.get_status(), 'description', 
        language)
    status = clean_status(status)
    return platypus.Paragraph(status, style)

def clean_status(status):
    if status:
        status = status.replace('</p><p>', '<br />\n <br />\n')
        status = status.replace("</p> <p>", '<br />\n <br />\n')
        status = status.replace("ОТ", "OT")
        if "href" in status:
            status = status.replace(" http://ot.mn/reports/</a> for English", 
                "English</a>")
            status = status.replace("http://ot.mn/тайлан</a> for Mongolian", 
                "Mongolian</a>")
            status = status.replace("\">", "\" color=\"#2171c7\"><u>")
            status = status.replace("</a>", "</u></a>")
        return status
    else:
        return ''

def get_status_displays(statuses, style):
    status_displays = []
    icon_statuses = ('not_started', 'delayed', 
        'in_progress', 'completed')
    for status in statuses:
        if status.status in icon_statuses:
            display_status = Image(
                "{0}{1}.jpg".format(
                    file_url,
                    status.status),
                width=25, height=25
            )
        else:
            display_status = Paragraph(
                status.get_status_display(), style)
        status_displays.append(display_status)
    if len(status_displays) < 2:
        status_displays.append('')
    return status_displays
    return ['','']
