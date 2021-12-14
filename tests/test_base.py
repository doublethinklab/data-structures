from datetime import datetime
import json
from json import JSONDecodeError
import unittest

from data_structures.youtube import YouTubeChannel, YouTubeVideo


class TestBaseFunctionality(unittest.TestCase):

    def test_unpack(self):
        def f(**kwargs):
            for key, value in kwargs.items():
                print(f'{key}\t{value}')

        x = YouTubeChannel(
            id='123',
            title='test channel',
            created_at=datetime(2021, 11, 1))

        # we want to test that we can do this
        error = False
        try:
            f(**x)
        except:
            error = True
        self.assertFalse(error)

    def test_to_json_handles_datetime(self):
        channel = YouTubeChannel(
            id='1',
            title='1',
            created_at=datetime(2021, 11, 11, 12, 12, 12))
        error = False
        try:
            result = channel.to_json()
        except JSONDecodeError:
            error = True
        self.assertFalse(error)
        expected_date = '2021-11-11 12:12:12'
        self.assertIn(expected_date, result)

    def test_to_json_handles_recursive_call(self):
        channel = YouTubeVideo(
            id='1',
            channel_id='1',
            created_at=datetime(2021, 1, 1, 2, 2, 2),
            title='title1',
            description='description1',
            channel=YouTubeChannel(
                id='1',
                title='1',
                created_at=datetime(2021, 11, 11, 12, 12, 12)))
        error = False
        try:
            result = channel.to_json()
        except JSONDecodeError:
            error = True
        self.assertFalse(error)
        result = json.loads(result)
        expected = dict(
            id='1',
            channel_id='1',
            created_at='2021-01-01 02:02:02',
            title='title1',
            description='description1',
            duration=None,
            dimension=None,
            definition=None,
            projection=None,
            stats=None,
            channel=json.dumps(dict(
                id='1',
                title='1',
                created_at='2021-11-11 12:12:12',
                description=None,
                lang=None,
                country=None)))
        self.assertEqual(expected, result)
