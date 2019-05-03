# coding: utf-8
import unittest

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

    def __iter__(self):
        'Iterates through all the points in the compass.'
        return iter(self.points)

    def is_cardinal(self, point):
        'Returns true if point is North, East, West or South, false otherwise.'
        return self.index(point) % 8 == 0

    def is_ordinal(self, point):
        'Returns true if point is Northeast, Southeast, Southwest or Northwest, false otherwise.'
        return self.index(point) % 4 == 0 and not self.is_cardinal(point)

    def is_half_wind(self, point):
        'Returns true if the point bisects the angle between the principle winds.'
        return self.index(point) % 2 == 0 and not self.is_cardinal(point) and not self.is_ordinal(point)

    def abbreviate(self, point):
        'Abbreviate the given compass point.'
        abbrev = point.lower()
        abbrev = abbrev.replace('north', 'N')
        abbrev = abbrev.replace('east', 'E')
        abbrev = abbrev.replace('south', 'S')
        abbrev = abbrev.replace('west', 'W')
        abbrev = abbrev.replace('-', '')
        return abbrev

    def get_point(self, abbreviated_point):
        'Returns the full name of the abbreviated point.'
        expansions = { 'N': 'North', 'E': 'East', 'S': 'South', 'W': 'West', 'b': ' by ' }
        point = ""
        for letter in abbreviated_point:
            point += expansions[letter]
        return point.capitalize()

    def angle(self, point):
        'Returns the angle of the given point in degrees.'
        assert point in self.points
        return 360.0 / len(self.points) * self.index(point)

    def index(self, point):
        'Returns the list index of the given point.'
        assert point in self.points
        return self.points.index(point)

class testCompass(unittest.TestCase):

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

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, portrait, landscape

class DrawCompass():

    def __init__(self):
        self.compass = Compass()
        self.pdf = Canvas("CanvasRose.pdf", pagesize=portrait(A4))
        width, height = portrait(A4)
        self.compass_radius = width / 2.0
        self.radii = [self.compass_radius - n * cm for n in [2.5, 1.2, 1.0]]

    def draw_arrow(self, angle):
        w = 1.0
        self.pdf.rotate(-angle)
        self.pdf.setFillColor('black')
        p = self.pdf.beginPath()
        p.moveTo(0, 0)
        p.lineTo(0, self.radii[0])
        p.lineTo(w * cm, w * cm)
        p.close()
        self.pdf.drawPath(p, fill=1)
        self.pdf.setFillColor('white')
        p = self.pdf.beginPath()
        p.moveTo(0, 0)
        p.lineTo(0, self.radii[0])
        p.lineTo(-w * cm, w * cm)
        p.close()
        self.pdf.drawPath(p, fill=1)
        self.pdf.setFillColor('black')
        self.pdf.rotate(angle)

    def draw_points(self):
        self.pdf.setLineWidth(0.25)

        for point in self.compass:
            self.pdf.rotate(-self.compass.angle(point))

            self.pdf.line(0, 1 * cm, 0, self.radii[0])

            if self.compass.is_cardinal(point):
                self.pdf.setFont("Times-Bold", 24)
            elif self.compass.is_ordinal(point):
                self.pdf.setFont("Times-Bold", 18)
            elif self.compass.is_half_wind(point):
                self.pdf.setFont("Times-Roman", 12)
                p = self.pdf.beginPath()
                p.moveTo(0, self.radii[0] - 0.015 * cm)
                p.lineTo(0.1 * cm, self.radii[0] - 0.75 * cm)
                p.lineTo(-0.1 * cm, self.radii[0] - 0.75 * cm)
                p.close()
                self.pdf.drawPath(p, fill=1)
            else:
                self.pdf.setFont("Times-Roman", 8)

            self.pdf.drawCentredString(0, self.radii[2] - 1.25 * cm, "{}".format(self.compass.abbreviate(point)))

            self.pdf.rotate(self.compass.angle(point))

    def draw_degrees(self):
        for deg in range(360):
            self.pdf.rotate(-deg)
            if deg % 10 == 0:
                self.pdf.setLineWidth(1.0)
                self.pdf.drawCentredString(0, self.radii[2] - 0.5 * cm, "{:2d}°".format(deg))
            else:
                self.pdf.setLineWidth(0.25)
            self.pdf.line(0, self.radii[1], 0, self.radii[2])
            self.pdf.rotate(deg)

    def draw_circles(self):
        self.pdf.setLineWidth(0.5)
        [self.pdf.circle(0, 0, r) for r in self.radii]


    def draw_compass_card(self):

        self.pdf.saveState()
        self.pdf.translate(self.compass_radius, self.compass_radius)

        self.draw_points()
        self.draw_degrees()
        self.draw_circles()

        cardinals = [pt for pt in self.compass if self.compass.is_cardinal(pt)]
        ordinals = [pt for pt in self.compass if self.compass.is_ordinal(pt)]

        for point in ordinals + cardinals:
            self.draw_arrow(self.compass.angle(point))

        self.pdf.restoreState()

        self.pdf.showPage()
        self.pdf.save()

if __name__ == '__main__':
    pic = DrawCompass()
    pic.draw_compass_card()
