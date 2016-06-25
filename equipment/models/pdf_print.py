import copy

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image

from inventory import settings


class PdfPrint:

    def __init__(self, buffer, pageSize):
        self.buffer = buffer
        # default format is A4
        if pageSize == 'A4':
            self.pageSize = A4
        elif pageSize == 'Letter':
            self.pageSize = letter
        self.width, self.height = self.pageSize

    def report(self, equipment_qrcode, equipment_inventory, equipment_serial):
        font_url = "%s/assets/css/dist/fonts/calibri.ttf" % settings.BASE_DIR
        pdfmetrics.registerFont(TTFont('Calibri', font_url))

        # set some characteristics for pdf document
        document = SimpleDocTemplate(
            self.buffer,
            rightMargin=72,
            leftMargin=72,
            topMargin=30,
            bottomMargin=72,
            pagesize=self.pageSize,)
        styles = getSampleStyleSheet()

        title_text = copy.copy(styles['Title'])
        title_text.fontName = 'Calibri'
        title_text.fontSize = 22

        body_text = copy.copy(styles['Normal'])
        body_text.alignment = 1
        body_text.fontSize = 16
        body_text.fontName = 'Calibri'

        # create document
        data = [
            Image(equipment_qrcode),
            Paragraph('Инв. {0}'.format(str(equipment_inventory)), title_text),
            Paragraph('S/N{0}'.format(equipment_serial), body_text)
        ]
        document.build(data)
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf