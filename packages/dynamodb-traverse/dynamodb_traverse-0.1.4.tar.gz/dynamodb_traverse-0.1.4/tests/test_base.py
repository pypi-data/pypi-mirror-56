import unittest

from dynamodb_traverse.base import Base


class TestBaseObject(unittest.TestCase):
    def test_log_file_generation(self):
        obj = Base()
        obj.info('test msg')
