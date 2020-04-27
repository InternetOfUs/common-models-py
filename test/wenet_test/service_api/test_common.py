from __future__ import absolute_import, annotations

from datetime import datetime
from unittest import TestCase

from wenet.service_api.common import Date, UserLanguage


class TestDate(TestCase):

    def test_repr(self):
        date = Date(
            year=2020,
            month=1,
            day=1
        )

        to_repr = date.to_repr()
        from_repr = Date.from_repr(to_repr)
        self.assertIsInstance(from_repr, Date)
        self.assertEqual(date, from_repr)
        self.assertEqual(datetime(year=2020, month=1, day=1), date.date_dt)

    def test_repr2(self):
        date = Date(
            year=2020,
            month=1,
            day=None
        )

        to_repr = date.to_repr()
        from_repr = Date.from_repr(to_repr)
        self.assertIsInstance(from_repr, Date)
        self.assertEqual(date, from_repr)
        self.assertIsNone(date.date_dt)

    def test_equal(self):
        date = Date(
            year=2020,
            month=1,
            day=None
        )
        date1 = Date(
            year=2020,
            month=1,
            day=None
        )
        date2 = Date(
            year=2020,
            month=None,
            day=None
        )
        date3 = Date(
            year=2020,
            month=1,
            day=1
        )
        date4 = Date(
            year=2020,
            month=1,
            day=1
        )
        self.assertEqual(date, date1)
        self.assertNotEqual(date, date2)
        self.assertNotEqual(date, date3)
        self.assertEqual(date3, date4)


class TestUserLanguage(TestCase):

    def test_repr(self):
        user_language = UserLanguage("ita", "C2", "it")
        to_repr = user_language.to_repr()
        from_repr = UserLanguage.from_repr(to_repr)

        self.assertIsInstance(from_repr, UserLanguage)
        self.assertEqual(user_language, from_repr)

    def test_check_iso_language(self):
        user_language_repr = {
            "name": "ita",
            "level": "C2",
            "code": "it"
        }

        self.assertEqual(user_language_repr, UserLanguage.from_repr(user_language_repr).to_repr())

    def test_check_iso_language2(self):
        user_language_repr = {
            "name": "ita",
            "level": "C2",
            "code": "ad"
        }

        self.assertRaises(
            ValueError,
            UserLanguage.from_repr,
            user_language_repr
        )
