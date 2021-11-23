from datetime import datetime
import unittest

from data_structures.youtube import YouTubeChannel


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
