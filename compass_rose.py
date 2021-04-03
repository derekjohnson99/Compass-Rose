# coding: utf-8
'''
A program to draw a PDF of a compass card showing all 32 points of a compass
'''
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, portrait
from Compass import Compass

class DrawCompass():
    "Draw a full compass cards with all 32 points"

    def __init__(self):
        self.compass = Compass()
        self.pdf = Canvas("compass_rose.pdf", pagesize=portrait(A4))
        width, _ = portrait(A4)
        self.half_page_width = width / 2.0
        self.inner_radius = self.half_page_width - 2.5 * cm
        self.outer_radius = self.half_page_width - 1.0 * cm

    def draw_closed_path(self, points, colour='black'):
        "Helper method to draw a closed path"
        self.pdf.setFillColor(colour)
        pdf_path = self.pdf.beginPath()
        pdf_path.moveTo(*points[0])
        for pnt in points[1:]:
            pdf_path.lineTo(*pnt)
        pdf_path.close()
        self.pdf.drawPath(pdf_path, fill=1)

    def draw_arrows(self):
        "Draw large two-colour arrows for the major compass points"
        cardinals = [pt for pt in self.compass if self.compass.is_cardinal(pt)]
        ordinals = [pt for pt in self.compass if self.compass.is_ordinal(pt)]
        length = self.inner_radius
        width = 1.0 * cm

        for point in ordinals + cardinals:
            self.pdf.rotate(-self.compass.angle(point))
            self.draw_closed_path([(0, 0), (0, length), (-width, width)], 'white')
            self.draw_closed_path([(0, 0), (0, length), (width, width)], 'black')
            self.pdf.rotate(self.compass.angle(point))

    def draw_points(self):
        "Draw each point of the compass"
        self.pdf.setLineWidth(0.25)
        arrow_point = self.inner_radius - 0.015 * cm
        arrow_head = self.inner_radius - 0.75 * cm
        arrow_width = 0.1 * cm
        text_offset = self.inner_radius + 0.25 * cm
        line_base = 0.1 * cm
        line_length = self.inner_radius

        for point in self.compass:
            self.pdf.rotate(-self.compass.angle(point))

            self.pdf.line(0, line_base, 0, line_length)

            if self.compass.is_cardinal(point):
                self.pdf.setFont("Times-Bold", 24)
            elif self.compass.is_ordinal(point):
                self.pdf.setFont("Times-Bold", 18)
            elif self.compass.is_half_wind(point):
                self.pdf.setFont("Times-Roman", 12)
                self.draw_closed_path([(0, arrow_point),
                                       (arrow_width, arrow_head),
                                       (-arrow_width, arrow_head)])
            else:
                self.pdf.setFont("Times-Roman", 8)

            self.pdf.drawCentredString(0, text_offset, f"{self.compass.abbreviate(point)}")

            self.pdf.rotate(self.compass.angle(point))

    def draw_degrees(self):
        "Draw the 360 degrees as ticks, with every ten degrees showing the value"
        for deg in range(360):
            self.pdf.rotate(-deg)
            if deg % 10 == 0:
                self.pdf.setLineWidth(1.0)
                self.pdf.drawCentredString(0, self.outer_radius - 0.5 * cm, f"{deg:2d}°")
            else:
                self.pdf.setLineWidth(0.25)
            self.pdf.line(0, self.outer_radius - 0.2 * cm, 0, self.outer_radius)
            self.pdf.rotate(deg)

    def draw_circles(self):
        "Draw the circles surrounding the compass"
        self.pdf.setLineWidth(0.5)
        self.pdf.circle(0, 0, self.inner_radius)
        self.pdf.circle(0, 0, self.outer_radius - 0.2 * cm)
        self.pdf.circle(0, 0, self.outer_radius)

    def draw_compass_card(self):
        "Main method to draw a full compass card"

        self.pdf.saveState()
        self.pdf.translate(self.half_page_width, self.half_page_width)

        self.draw_points()
        self.draw_degrees()
        self.draw_circles()
        self.draw_arrows()

        self.pdf.restoreState()

        self.pdf.showPage()
        self.pdf.save()

def main():
    "main function"
    pic = DrawCompass()
    pic.draw_compass_card()

if __name__ == '__main__':
    main()
