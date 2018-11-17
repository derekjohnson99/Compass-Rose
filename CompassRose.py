import math
from collections import OrderedDict
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, portrait, landscape

class Compass():

    def __init__(self):
        self.points = [
            'North',
            'North by east',
            'North-northeast',
            'Northeast by north',
            'Northeast',
            'Northeast by east',
            'East-northeast',
            'East by north',
            'East',
            'East by south',
            'East-southeast',
            'Southeast by east',
            'Southeast',
            'Southeast by south',
            'South-southeast',
            'South by east',
            'South',
            'South by west',
            'South-southwest',
            'Southwest by south',
            'Southwest',
            'Southwest by west',
            'West-southwest',
            'West by south',
            'West',
            'West by north',
            'West-northwest',
            'Northwest by west',
            'Northwest',
            'Northwest by north',
            'North-northwest',
            'North by west'
        ]

    def is_cardinal(self, point):
        'Returns true if point is North, East, West or South, false otherwise'
        return self.points.index(point) % 8 == 0

    def is_ordinal(self, point):
        'Returns true if point is Northeast, Southeast, Southwest or Northwest, false otherwise'
        return self.points.index(point) % 4 == 0 and not self.is_cardinal(point)

    def is_half_wind(self, point):
        return self.points.index(point) % 2 == 0 and not self.is_cardinal(point) and not self.is_ordinal(point)

    def abbreviate(self, point):
        "Abbreviate the given compass point"
        pnt = point.lower()
        translation_table = dict.fromkeys(map(ord, ' -'))
        # Remove spaces and hyphens
        pnt = pnt.translate(dict.fromkeys(map(ord, ' -'), None))
        abbrev = ""
        trans = { 'north': 'N', 'east': 'E', 'south': 'S', 'west': 'W', 'by': 'b' }
        while len(pnt):
            for p in trans.keys():
                if pnt.startswith(p):
                    abbrev += trans[p]
                    pnt = pnt[len(p):]
        return abbrev

    def get_point(self, abbreviated_point):
        expansions = { 'N': 'North', 'E': 'East', 'S': 'South', 'W': 'West', 'b': ' by ' }
        point = ""
        for letter in abbreviated_point:
            point += expansions[letter]
        return point.capitalize()

    def angle(self, point):
        assert point in self.points
        return 360.0 / len(self.points) * self.points.index(point)

    def index(self, point):
        assert point in self.points
        return self.points.index(point)

    def test_compass(self):
        assert(self.is_cardinal('North'))
        assert(not self.is_cardinal('Northwest'))
        assert(self.is_ordinal('Northwest'))
        assert(not self.is_ordinal('North'))

def draw_arrow(pdf, angle, length):
    pdf.rotate(-angle)
    pdf.setFillColor('black')
    p = pdf.beginPath()
    p.moveTo(0, 0)
    p.lineTo(0, length)
    p.lineTo(1 * cm, 1 * cm)
    p.close()
    pdf.drawPath(p, fill=1)
    pdf.setFillColor('white')
    p = pdf.beginPath()
    p.moveTo(0, 0)
    p.lineTo(0, length)
    p.lineTo(-1 * cm, 1 * cm)
    p.close()
    pdf.drawPath(p, fill=1)
    pdf.setFillColor('black')
    pdf.rotate(angle)

def draw_compass_card(compass):
    
    pdf = Canvas("CompassRose.pdf", pagesize=portrait(A4))

    width, height = portrait(A4)
    x_centre = width / 2.0

    pdf.saveState()
    pdf.translate(x_centre, x_centre)

    inner_radius = x_centre - 2.5 * cm

    pdf.setLineWidth(0.5)
    [pdf.circle(0, 0, r) for r in [x_centre - 1 * cm, x_centre - 1.2 * cm,  inner_radius]]

    pdf.setLineWidth(0.25)

    for point in compass.points:
        pdf.rotate(-compass.angle(point))

        pdf.line(0, 1 * cm, 0, inner_radius)

        if compass.is_cardinal(point):
            pdf.setFont("Times-Roman", 24)
        elif compass.is_ordinal(point):
            pdf.setFont("Times-Roman", 18)
        elif compass.is_half_wind(point):
            pdf.setFont("Times-Roman", 12)
            p = pdf.beginPath()
            p.moveTo(0, inner_radius)
            p.lineTo(0.1 * cm, inner_radius - 0.75 * cm)
            p.lineTo(-0.1 * cm, inner_radius - 0.75 * cm)
            p.close()
            pdf.drawPath(p, fill=1)
        else:
            pdf.setFont("Times-Roman", 8)

        pdf.drawCentredString(0, x_centre - 2.25 * cm, "{}".format(compass.abbreviate(point)))
            
        pdf.rotate(compass.angle(point))

    cardinals = [pt for pt in compass.points if compass.is_cardinal(pt)]
    ordinals = [pt for pt in compass.points if compass.is_ordinal(pt)]

    for point in ordinals:
        draw_arrow(pdf, compass.angle(point), inner_radius)

    for point in cardinals:
        draw_arrow(pdf, compass.angle(point), inner_radius)

    for deg in range(360):
        pdf.rotate(-deg)
        if deg % 10 == 0:
            pdf.setLineWidth(1.0)
            pdf.drawCentredString(0, x_centre - 1.5 * cm, "{:2d}°".format(deg))
        else:
            pdf.setLineWidth(0.25)
        pdf.line(0, x_centre - 1 * cm, 0, x_centre - 1.2 * cm)
        pdf.rotate(deg)

    pdf.restoreState()

    pdf.showPage()
    pdf.save()

if __name__ == '__main__':
    compass = Compass()
    compass.test_compass()

    draw_compass_card(compass)
