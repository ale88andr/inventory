from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image


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
        # font_bold_url = "%s/plan/font-bold.ttf" % settings.BASE_DIR
        # pdfmetrics.registerFont(TTFont('MegaFontBold', font_bold_url))

        # set some characteristics for pdf document
        document = SimpleDocTemplate(
            self.buffer,
            rightMargin=72,
            leftMargin=72,
            topMargin=30,
            bottomMargin=72,
            pagesize=self.pageSize,)
        styles = getSampleStyleSheet()
        # styles.add(ParagraphStyle(name='default', alignment=CA_CENTER, fontSize=13, spaceAfter=8, fontName='Calibry'))

        # create document
        data = [
            Image(equipment_qrcode),
            Paragraph(str(equipment_inventory), styles['Title']),
            Paragraph('S/N{0}'.format(equipment_serial), styles['BodyText'])
        ]
        document.build(data)
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf