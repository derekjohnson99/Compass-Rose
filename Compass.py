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
        self._point = None
        return self

    def __next__(self):
        'Provides the next point on the compass.'
        if self._point is None:
            self._point = 'North'
        elif self.index() + 1 < len(self.points):
            self._point = self.points[self.index() + 1]
        else:
            raise StopIteration
        return self

    def set(self, point):
        self._point = point

    def angle(self):
        'Returns the angle of the given point in degrees.'
        assert self._point in self.points
        return 360.0 / len(self.points) * self.index()

    def index(self):
        'Returns the list index of the given point.'
        assert self._point in self.points
        return self.points.index(self._point)

    def is_cardinal(self):
        'Returns true if point is North, East, West or South (aka "basic wind"), false otherwise.'
        return self.index() % 8 == 0

    def is_ordinal(self):
        'Returns true if point is Northeast, Southeast, Southwest or Northwest, false otherwise.'
        return self.index() % 4 == 0 and not self.is_cardinal()

    def is_principal_wind(self):
        'Returns true if point is one of cardinal or ordinal points'
        return self.is_cardinal() or self.is_ordinal()

    def is_half_wind(self):
        'Returns true if the point bisects the angle between the principal winds.'
        return self.index() % 2 == 0 and not self.is_principal_wind()

    def abbreviate(self):
        'Abbreviate the given compass point.'
        abbrev = self._point.lower()
        abbrev = abbrev.replace('north', 'N')
        abbrev = abbrev.replace('east', 'E')
        abbrev = abbrev.replace('south', 'S')
        abbrev = abbrev.replace('west', 'W')
        abbrev = abbrev.replace('-', '')
        return abbrev

class TestCompass(unittest.TestCase):
    "Test the Compass class"

    def setUp(self):
        self.compass = Compass()

    def test_cardinals(self):
        'The compass class can correctly identify cardinal points'
        self.compass.set('North')
        self.assertTrue(self.compass.is_cardinal())
        self.compass.set('Northwest')
        self.assertFalse(self.compass.is_cardinal())
        cardinals = [point for point in Compass() if point.is_cardinal()]
        self.assertEqual(len(cardinals), 4)

    def test_ordinals(self):
        'The compass class can correctly identify ordinal points'
        self.compass.set('Northwest')
        self.assertTrue(self.compass.is_ordinal())
        self.compass.set('North')
        self.assertFalse(self.compass.is_ordinal())
        self.compass.set('Southwest by west')
        self.assertFalse(self.compass.is_ordinal())
        ordinals = [point for point in Compass() if point.is_ordinal()]
        self.assertEqual(len(ordinals), 4)

    def test_principal_wind(self):
        'Test the is_principal_wind method'
        self.compass.set('Southwest')
        self.assertTrue(self.compass.is_principal_wind())
        self.compass.set('East')
        self.assertTrue(self.compass.is_principal_wind())
        self.compass.set('South-southwest')
        self.assertFalse(self.compass.is_principal_wind())
        self.compass.set('Northwest by west')
        self.assertFalse(self.compass.is_principal_wind())
        principal_winds = [point for point in Compass() if point.is_principal_wind()]
        self.assertEqual(len(principal_winds), 8)

    def test_half_wind(self):
        'Test the is_half_wind method'
        self.compass.set('Northeast')
        self.assertFalse(self.compass.is_half_wind())
        self.compass.set('West')
        self.assertFalse(self.compass.is_half_wind())
        self.compass.set('West-southwest')
        self.assertTrue(self.compass.is_half_wind())
        self.compass.set('Northwest by west')
        self.assertFalse(self.compass.is_half_wind())
        half_winds = [point for point in Compass() if point.is_half_wind()]
        self.assertEqual(len(half_winds), 8)

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
                self.compass.set(point)
                self.assertEqual(self.compass.abbreviate(), expected_abbreviation)

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
                self.compass.set(point)
                self.assertEqual(self.compass.angle(), expected_angle)

    def test_iterations(self):
        'Compass object will iterate through 32 points, then raise a StopIteration exception'
        point_count = 0
        it = iter(Compass())
        with self.assertRaises(StopIteration):
            while next(it):
                point_count += 1
        self.assertEqual(point_count, 32)

if __name__ == '__main__':
    pass
