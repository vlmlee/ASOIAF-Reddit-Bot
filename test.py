import unittest
from main import mispelled, correct_spelling, check_if_named_weapon

class RedditBotTestCase(unittest.TestCase):
	"""Tests for ASOIAF Named Weapons Spell Checker Bot"""
	def test_letter_filter(self):
		self.assertFalse(mispelled({body: 'anchor'}))
		self.assertFalse(mispelled({body: 'carrot'}))
		self.assertFalse(mispelled({body: 'zoo'}))

	def test_length_filter(self):
		self.assertFalse(mispelled('to'))
		self.assertFalse(mispelled('supercalifragilisticexpialidocious'))
		self.assertTrue('widow')

	def test_is_named_weapon(self):
		self.assertFalse(check_if_named_weapon('blede'))
		self.assertFalse(check_if_named_weapon('blackfyre'))

if __name__ == "__main__":
	unittest.main()