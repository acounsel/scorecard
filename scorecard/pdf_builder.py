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

s3_url = 'https://scorecard-static.s3-us-west-1.amazonaws.com/'
url_loc = 'media/public/'
file_url = s3_url + url_loc

reportlab.rl_config.TTFSearchPath.append(
    'https://s3.console.aws.amazon.com/s3/object/scorecard-static/media/public/')
# pdfmetrics.registerFont(TTFont("Fjalla-One", "FjallaOne-Regular.ttf"))

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
        self.drawRightString(260 * mm, (0.4 * inch),
                             "%d" % (self._pageNumber))
def export_pdf(overview):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=commitments.pdf'
        
    image = '{}Accountability+Counsel_Logo_Color+(2).png'.format(
        file_url)

    #Create all different font styles
    styles = getSampleStyleSheet()
    header_style = styles.add(ParagraphStyle(name='header_style',
                              fontFamily='Montserrat',
                              fontSize=11,
                              textColor=colors.HexColor('#FFFFFF')))
    styleBH = ParagraphStyle('header_style', parent=styles['header_style'])
    styleBH.alignment = TA_CENTER
    category_style = styles.add(ParagraphStyle(name='category_style',
                              fontFamily='Fjalla-One',
                              fontSize=20,
                              leftIndent=13,
                              textColor=colors.HexColor('#FFFFFF')))
    style_category = ParagraphStyle('category_style', parent=styles['category_style'])
    styles.add(ParagraphStyle(name='Breadpointlist_style',
                              fontFamily='Montserrat',
                              fontSize=10,
                              leading=12,
                              wordWrap='LTR',
                              ))
    styleN = ParagraphStyle('bps', parent=styles['Breadpointlist_style'])
    styles.add(ParagraphStyle(name='Title_style',
                              fontFamily='Fjalla-One',
                              fontSize=30,
                              textColor=colors.HexColor("#1ca4bc")))
    title_style = ParagraphStyle('title_style', parent=styles['Title_style'])
    styles.add(ParagraphStyle(name='subitle1_style',
                              fontFamily='Fjalla-One',
                              fontSize=12))
    subtitle1_style = ParagraphStyle('subitle1_style', parent=styles['subitle1_style'])
    styles.add(ParagraphStyle(name='subitle2_style',
                              fontFamily='Fjalla-One',
                              fontSize=11))
    subtitle2_style = ParagraphStyle('subitle2_style', parent=styles['subitle2_style'])


    # Create PDF
    pdf = SimpleDocTemplate(response, showBoundary=0, leftMargin=0.9 * cm, 
        rightMargin=0.9*cm, topMargin=2.5*cm, bottomMargin=1*cm, pagesize=landscape(letter))

    # Create header with titles and legend
    story = []
    story.append(Paragraph("<strong>{}</strong>".format(overview.name),title_style))
    story.append(Spacer(1,.30*inch))
    story.append(Paragraph("<strong>{}</strong>".format(overview.subtitle),subtitle1_style))
    story.append(Spacer(1,.18*inch))
    story.append(Paragraph("<strong>Status of Commitments as of May 2020</strong>",subtitle2_style))
    im = Image('{}graphics.jpg'.format(file_url), width=360, height=41.076)
    im.hAlign = 'RIGHT'
    story.append(im)
        
    total_data =[]
    counter = 2
    #create header row
    row_data = []
    for header_text in ('#', 'Commitment', 'About the Commitment',
        'Status of Commitment', 'Original Timeline', '2019 Status',
        '2020 Status'):
        row_data.append(
            Paragraph(
                '''<b>{}</b>'''.format(header_text), styleBH
            )
        )
    total_data.append(row_data)
    table = Table(total_data, colWidths=[30, 81, 174, 290, 60, 47, 47], rowHeights=[60])
    styling = [
        ('BACKGROUND', (0, 0), (-1, 0), '#70747c'),
        ("GRID", (0, 0), (-1, -1), 0.2*mm, '#a0a0a4'),
        ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('HALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]
    style = TableStyle(styling)
    table.setStyle(style)
    story.append(table)
    total_data = []
    # Use bools to track the first instance of the category
    category_bools = {
        'Pasture': False,
        'Water': False,
        'Monitoring': False,
        'Individual Compensation': False,
        'Animal Husbandry Development': False,
        'Collective Compensation': False,
        'Undai River diversion': False,
    }
    #iterate through data
    for commitment in overview.commitment_set.all():
        row_data = []
        #Input the category row
        new_category = False
        for key, value in category_bools.items():
            if key == commitment.category.name and value == False:
                category_bools[key] = True
                new_category = True
        if new_category:
            if counter > 2:
                table = Table(total_data, colWidths=[30, 81, 174, 290, 60, 47, 47])
                styling = [
                    ("GRID", (0, 0), (-1, -1), 0.2*mm, '#a0a0a4'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('HALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
                ]
                style = TableStyle(styling)
                table.setStyle(style)
                story.append(table)
                total_data = []
                row_data = []
            diversion_check = commitment.category.name
            diversion_check = diversion_check.replace("diversion", "Diversion")
            row_data.append(Paragraph(diversion_check, style_category))
            for i in range(0, 6):
                row_data.append(Paragraph("", style_category))
            total_data.append(row_data)
            table = Table(total_data, colWidths=[30, 81, 174, 290, 60, 47, 47], rowHeights=[35])
            #[35, 95, 145, 300, 60, 45, 45]
            styling = [
                ("GRID", (0, 0), (-1, -1), 0.2*mm, '#a0a0a4'),
                ('SPAN', (0, 0), (6, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BACKGROUND', (0, 0), (-1, 0), '#007D8A'),
            ]
            style = TableStyle(styling)
            table.setStyle(style)
            story.append(table)
            total_data = []
            counter += 1
        row_data = []
        order = Paragraph(str(commitment.order_num) + commitment.order_letter, styleN)
        commit = commitment.name
        commit = commit.replace("ОТ", "OT")
        if "href" in commit:
            commit = commit.replace("\">", "\" color=\"#2171c7\"><u>")
            commit = commit.replace("</a>", "</u></a>")
        commitment_name = platypus.Paragraph(commit, styleN)
        about_commitment = platypus.Paragraph(commitment.description, styleN)
        status = commitment.get_status().description
        status = status.replace('</p><p>', '<br />\n <br />\n')
        status = status.replace("</p> <p>", '<br />\n <br />\n')
        status = status.replace("ОТ", "OT")
        if "href" in status:
            status = status.replace(" http://ot.mn/reports/</a> for English", "English</a>")
            status = status.replace("http://ot.mn/тайлан</a> for Mongolian", "Mongolian</a>")
            status = status.replace("\">", "\" color=\"#2171c7\"><u>")
            status = status.replace("</a>", "</u></a>")
        status_commitment = platypus.Paragraph(status, styleN)
        timeline = Paragraph(commitment.original_timeline, styleN)
        statuses = commitment.status_set.order_by('date')[:2]
        icon_url = 'https://scorecard-static.s3-us-west-1.amazonaws.com/media/public/'
        status_displays = []
        icon_statuses = ('not_started', 'delayed', 'in_progress', 'completed')
        for status in statuses:
            print(status.status)
            if status.status in icon_statuses:
                display_status = Image(
                    "{0}{1}.jpg".format(
                        icon_url,
                        status.status, 
                        width=25, height=25
                    )
                )
            else:
                display_status = Paragraph(
                    status.get_status_display(), styleN)
            status_displays.append(display_status)
        row_data.append(order)
        row_data.append(commitment_name)
        row_data.append(about_commitment)
        row_data.append(status_commitment)
        row_data.append(timeline)
        row_data.append(status_displays[0])
        row_data.append(status_displays[1])
        total_data.append(row_data)
    table = Table(total_data, colWidths=[30, 81, 174, 290, 60, 47, 47])
    styling = [
        ("GRID", (0, 0), (-1, -1), 0.2 * mm, '#a0a0a4'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('HALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 6), (-1, 7), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]
    style = TableStyle(styling)
    table.setStyle(style)
    story.append(table)

    #Build PDF with logo header and page numbers
    pdf.build(story, onFirstPage=_header, onLaterPages=_header,
                  canvasmaker=PageNumbers)

    return response


