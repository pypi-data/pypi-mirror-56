from pprint import pprint

import mptt
from django.test import TestCase
from django_tasker_geobase import geocoder, models


class TestGeocoder(TestCase):

    def test_not_found(self):
        geo_object = geocoder.geo(query="test_not_found test_not_found test_not_found")
        self.assertIsNone(geo_object)

    def test_address_apparment(self):
        geo_object = geocoder.geo(query="Новосибирск улица Мира, 61к1 кв.11")
        self.assertEqual(geo_object.zipcode, '630024')
        self.assertEqual(geo_object.ru, "11")
        self.assertEqual(geo_object.en, "11")
        self.assertEqual(geo_object.timezone, 'Asia/Novosibirsk')
        self.assertEqual(geo_object.longitude, 82.940462)
        self.assertEqual(geo_object.latitude, 54.959423)
        self.assertIsNone(geo_object.openweathermap)
        self.assertEqual(geo_object.type, 15)
        self.assertEqual(geo_object.get_type_display(), 'Apartment')

    def test_get_country(self):
        geo_object = geocoder.geo(query="Новосибирск улица Мира, 61к1 кв.11")
        geo_object = geo_object.get(geo_type=1)

        self.assertEqual(geo_object.ru, 'Россия')
        self.assertEqual(geo_object.en, 'Russia')
        self.assertEqual(geo_object.type, 1)
        self.assertEqual(geo_object.get_type_display(), 'Country')

    def test_get_province(self):
        geo_object = geocoder.geo(query="Новосибирск улица Мира, 61к1 кв.11")
        geo_object = geo_object.get(geo_type=2)
        self.assertEqual(geo_object.ru, 'Новосибирская область')
        self.assertEqual(geo_object.en, 'Novosibirsk Region')
        self.assertIsNone(geo_object.timezone)
        self.assertIsNone(geo_object.longitude)
        self.assertIsNone(geo_object.latitude)
        self.assertIsNone(geo_object.openweathermap)
        self.assertEqual(geo_object.type, 2)
        self.assertEqual(geo_object.get_type_display(), 'Province')

    def test_get_locality(self):
        geo_object = geocoder.geo(query="Новосибирск улица Мира, 61к1 кв.11")
        geo_object = geo_object.get(geo_type=4)
        self.assertEqual(geo_object.ru, 'Новосибирск')
        self.assertEqual(geo_object.en, 'Novosibirsk')
        self.assertEqual(geo_object.timezone, 'Asia/Novosibirsk')
        self.assertEqual(geo_object.longitude, 82.92043)
        self.assertEqual(geo_object.latitude, 55.030199)
        self.assertEqual(geo_object.openweathermap, 1496747)
        self.assertEqual(geo_object.type, 4)
        self.assertEqual(geo_object.get_type_display(), 'Locality')

    def test_get_street(self):
        geo_object = geocoder.geo(query="Новосибирск улица Мира, 61к1 кв.11")
        geo_object = geo_object.get(geo_type=6)

        self.assertEqual(geo_object.ru, 'улица Мира')
        self.assertEqual(geo_object.en, 'ulitsa Mira')
        self.assertEqual(geo_object.timezone, 'Asia/Novosibirsk')
        self.assertIsNone(geo_object.longitude)
        self.assertIsNone(geo_object.latitude)
        self.assertEqual(geo_object.type, 6)
        self.assertEqual(geo_object.get_type_display(), 'Street')

    def test_get_house(self):
        geo_object = geocoder.geo(query="Новосибирск улица Мира, 61к1 кв.11")
        geo_object = geo_object.get(geo_type=7)

        self.assertEqual(geo_object.ru, '61к1')
        self.assertEqual(geo_object.ru, '61к1')
        self.assertEqual(geo_object.timezone, 'Asia/Novosibirsk')
        self.assertEqual(geo_object.longitude, 82.940462)
        self.assertEqual(geo_object.latitude, 54.959423)
        self.assertEqual(geo_object.zipcode, '630024')
