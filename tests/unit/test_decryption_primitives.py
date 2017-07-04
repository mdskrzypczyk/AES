import unittest
from aes.aes_lib import ibyte_sub, ishift_row, imix_column

class TestDecryptionPrimitives(unittest.TestCase):
	def test_inverse_byte_sub(self):
		data = [99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118]
		res = ibyte_sub(data)
		assert res == range(16)

	def test_inverse_shift_row(self):
		data = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
		res = ishift_row(data)
		assert res == range(16)

	def test_inverse_mix_columns(self):
		data = [2, 7, 0, 5, 6, 3, 4, 1, 10, 15, 8, 13, 14, 11, 12, 9]
		res = imix_column(data)
		assert res == range(16)