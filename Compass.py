#!/usr/bin/env python3
'A module to provide a Compass class'

import unittest

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

if __name__ == '__main__':
    pass
