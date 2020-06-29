# coding: utf-8
'''
A program to draw a PDF of a compass card showing all 32 points of a compass
'''
import unittest
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, portrait

class Compass():
    '''
    A class to encapusalte all the points in a compass, including
    their names and angles.
    '''

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

    def __iter__(self):
        'Iterates through all the points in the compass.'
        return iter(self.points)

    def is_cardinal(self, point):
        'Returns true if point is North, East, West or South (aka "basic wind"), false otherwise.'
        return self.index(point) % 8 == 0

    def is_ordinal(self, point):
        'Returns true if point is Northeast, Southeast, Southwest or Northwest, false otherwise.'
        return self.index(point) % 4 == 0 and not self.is_cardinal(point)

    def is_principal_wind(self, point):
        'Returns true if point is one of cardinal or ordinal points'
        return self.is_cardinal(point) or self.is_ordinal(point)

    def is_half_wind(self, point):
        'Returns true if the point bisects the angle between the principal winds.'
        return self.index(point) % 2 == 0 and not self.is_principal_wind(point)

    @staticmethod
    def abbreviate(point):
        'Abbreviate the given compass point.'
        abbrev = point.lower()
        abbrev = abbrev.replace('north', 'N')
        abbrev = abbrev.replace('east', 'E')
        abbrev = abbrev.replace('south', 'S')
        abbrev = abbrev.replace('west', 'W')
        abbrev = abbrev.replace('-', '')
        return abbrev

    def angle(self, point):
        'Returns the angle of the given point in degrees.'
        assert point in self.points
        return 360.0 / len(self.points) * self.index(point)

    def index(self, point):
        'Returns the list index of the given point.'
        assert point in self.points
        return self.points.index(point)

class TestCompass(unittest.TestCase):
    "Test the Compass class"

    def setUp(self):
        self.compass = Compass()

    def test_cardinals(self):
        'The compass class can correctly identify cardinal points'
        self.assertTrue(self.compass.is_cardinal('North'))
        self.assertFalse(self.compass.is_cardinal('Northwest'))

    def test_ordinals(self):
        'The compass class can correctly identify ordinal points'
        self.assertTrue(self.compass.is_ordinal('Northwest'))
        self.assertFalse(self.compass.is_ordinal('North'))
        self.assertFalse(self.compass.is_ordinal('Southwest by west'))

    def test_abbreviations(self):
        'The compass class can abbreviate points correctly'
        # A selection of test points and their expected abbreviations
        test_points = [
            ("North-northwest", "NNW"),
            ("East by south", "E by S"),
            ("Northeast", "NE"),
            (self.compass.points[1], "N by E"),
        ]

        for (point, expected_abbreviation) in test_points:
            with self.subTest(point):
                self.assertEqual(self.compass.abbreviate(point), expected_abbreviation)

    def test_angle(self):
        'Points are at correct angle'
        # A selection of points, and their expected angle on the compass
        test_points = [
            ("North", 0.0),
            ("South", 180.0),
            ("North-northeast", 22.5),
            ("West", 270.0),
            ("Northwest", 315.0),
            ("North by west", 360.0 - 11.25),
        ]

        for (point, expected_angle) in test_points:
            with self.subTest(point):
                self.assertEqual(self.compass.angle(point), expected_angle)

class DrawCompass():
    "Draw a full compass cards with all 32 points"

    def __init__(self):
        self.compass = Compass()
        self.pdf = Canvas("compass_rose.pdf", pagesize=portrait(A4))
        width, height = portrait(A4)
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
                self.draw_closed_path([(0, arrow_point), (arrow_width, arrow_head), (-arrow_width, arrow_head)])
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

if __name__ == '__main__':
    PIC = DrawCompass()
    PIC.draw_compass_card()
