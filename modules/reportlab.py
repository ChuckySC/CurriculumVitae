from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.units import inch
from reportlab.lib import colors


class ReportLabConfiguration:
    # Import fonts
    registerFont(TTFont('Inconsolata', 'static/assets/fonts/Inconsolata-Regular.ttf'))
    registerFont(TTFont('InconsolataBold', 'static/assets/fonts/Inconsolata-Bold.ttf'))
    registerFontFamily('Inconsolata', normal='Inconsolata', bold='InconsolataBold')
    
    # Set the page height and width
    HEIGHT = 11 * inch
    WIDTH = 8.5 * inch
    
    # Set styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Content', fontFamily='Inconsolata', fontSize=8, spaceAfter=.1*inch))
    
    def myPageWrapper(self, contact):
        """
            Draw the framework for the first page,
            pass in contact info as a dictionary
        """
        # template for static, non-flowables, on the first page
        # draws all of the contact information at the top of the page
        def myPage(canvas, doc):
            canvas.saveState()  # save the current state
            canvas.setFont('InconsolataBold', 16)  # set the font for the name
            canvas.drawString(
                .4 * inch, self.HEIGHT - (.4 * inch), contact['name']
            )  # draw the name on top left page 1
            canvas.setFont('Inconsolata', 8)  # sets the font for contact
            canvas.drawRightString(
                self.WIDTH - (.4 * inch), self.HEIGHT - (.4 * inch), contact['linkedin']
            )
            # canvas.drawRightString(
            #     self.WIDTH - (.4 * inch), self.HEIGHT - (.4 * inch), contact['github']
            # )
            canvas.line(
                .4 * inch, self.HEIGHT - (.47 * inch), self.WIDTH - (.4 * inch), self.HEIGHT - (.47 * inch)
            )
            canvas.drawString(
                .4 * inch, self.HEIGHT - (.6 * inch), contact['phone']
            )
            canvas.drawCentredString(
                self.WIDTH / 2.0, self.HEIGHT - (.6 * inch), contact['address']
            )
            canvas.drawRightString(
                self.WIDTH - (.4 * inch), self.HEIGHT - (.6 * inch), contact['email']
            )
            # restore the state to what it was when saved
            canvas.restoreState()
        return myPage

    def generate_print_pdf(self, data: list, contact: dict):
        pdfname = 'downloads/resume.pdf'
        doc = SimpleDocTemplate(
            pdfname,
            pagesize=letter,
            bottomMargin=.5 * inch,
            topMargin=.7 * inch,
            rightMargin=.4 * inch,
            leftMargin=.4 * inch
        )  # set the doc template
        style = self.styles["Normal"]  # set the style to normal
        story = []  # create a blank story to tell
        contentTable = Table(data, colWidths=[0.8 * inch, 6.9 * inch])
        tblStyle = TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('FONT', (0, 0), (-1, -1), 'Inconsolata'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT')
        ])
        contentTable.setStyle(tblStyle)
        story.append(contentTable)
        doc.build(story, onFirstPage=self.myPageWrapper(contact))
        return pdfname