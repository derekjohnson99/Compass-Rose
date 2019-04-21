# coding: utf-8
import math
from collections import OrderedDict
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, portrait, landscape
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

def draw_arrow(pdf, angle, length):
    w = 1.0
    pdf.rotate(-angle)
    pdf.setFillColor('black')
    p = pdf.beginPath()
    p.moveTo(0, 0)
    p.lineTo(0, length)
    p.lineTo(w * cm, w * cm)
    p.close()
    pdf.drawPath(p, fill=1)
    pdf.setFillColor('white')
    p = pdf.beginPath()
    p.moveTo(0, 0)
    p.lineTo(0, length)
    p.lineTo(-w * cm, w * cm)
    p.close()
    pdf.drawPath(p, fill=1)
    pdf.setFillColor('black')
    pdf.rotate(angle)

def draw_compass_card():

    compass = Compass()
    pdf = Canvas("CompassRose.pdf", pagesize=portrait(A4))

    width, height = portrait(A4)
    x_centre = width / 2.0

    pdf.saveState()
    pdf.translate(x_centre, x_centre)

    inner_radius = x_centre - 2.5 * cm

    pdf.setLineWidth(0.5)
    [pdf.circle(0, 0, r) for r in [x_centre - 1 * cm, x_centre - 1.2 * cm,  inner_radius]]

    pdf.setLineWidth(0.25)

    for point in compass:
        pdf.rotate(-compass.angle(point))

        pdf.line(0, 1 * cm, 0, inner_radius)

        if compass.is_cardinal(point):
            pdf.setFont("Times-Bold", 24)
        elif compass.is_ordinal(point):
            pdf.setFont("Times-Bold", 18)
        elif compass.is_half_wind(point):
            pdf.setFont("Times-Roman", 12)
            p = pdf.beginPath()
            p.moveTo(0, inner_radius - 0.015 * cm)
            p.lineTo(0.1 * cm, inner_radius - 0.75 * cm)
            p.lineTo(-0.1 * cm, inner_radius - 0.75 * cm)
            p.close()
            pdf.drawPath(p, fill=1)
        else:
            pdf.setFont("Times-Roman", 8)

        pdf.drawCentredString(0, x_centre - 2.25 * cm, "{}".format(compass.abbreviate(point)))

        pdf.rotate(compass.angle(point))

    cardinals = [pt for pt in compass if compass.is_cardinal(pt)]
    ordinals = [pt for pt in compass if compass.is_ordinal(pt)]

    for point in ordinals + cardinals:
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
    draw_compass_card()
