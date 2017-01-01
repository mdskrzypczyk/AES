import unittest
from aes.aes_lib import byte_sub, shift_row, mix_column

data = range(16)

class TestEncryptionPrimitives(unittest.TestCase):
	def test_byte_sub(self):
		expected = [99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118]
		res = byte_sub(data)
		assert res == expected

	def test_shift_row(self):
		expected = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
		res = shift_row(data)
		assert res == expected

	def test_mix_column(self):
		expected = [2, 7, 0, 5, 6, 3, 4, 1, 10, 15, 8, 13, 14, 11, 12, 9]
		res = mix_column(data)
		assert res == expected
