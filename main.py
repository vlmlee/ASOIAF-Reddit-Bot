import praw
import re
import json
import spell
from time import sleep
from collections import deque

# User settings
# import settings

def check_if_misspelled(c):
	text = c.body.lower()
	tokens = text.split()

	# heuristically filter the words
	letters = ("b", "d", "h", "i", "l", "n", "o", "r", "t", "v", "w")
	words_to_spellcheck = [word for word in tokens if word.startswith(letters) and len(word) > 2 and len(word) < 12]

	for item in words_to_spellcheck:
		if check_if_named_weapon(item):
			correct_spelling(c, check_if_named_weapon(item), respond=True)

def check_if_named_weapon(word):
	corrected_word = correction(word) # correction() comes from spell.py
	correction_and_descrip = []
	if (corrected_word != word):
		# the candidate word is a slight misspelling
		if corrected_word in weapons: # check if the misspelled word matches any of the weapons
			return correction_and_descrip.extend([word, corrected_word, weapons[corrected_word]])
		else:
			return False
	else:
		# the word is spelled correctly
		return False

def correct_spelling(c, correction_and_descrip, respond=False):
	# get misspelled word
	# tell user that it has been corrected
	# reply with description

	if respond: 
		head = "Hi, it looks like you misspelled " + correction_and_descrip[0] + ".\n"
		correction = "The correct spelling is " + correction_and_descrip[1] + ".\n"
		description = "A little bit of detail about that weapon: \n\n >" + correction_and_descrip[2]
		c.reply(head + correction + description)

def unit_tests():
	assert type(weapons) is dict
	assert 'brightroar' in weapons
	assert 'blackfire' not in weapons
	assert len(weapons) == 15
	# assert user_agent == ("ASOIAF Named Weapons Spell Checker Bot v0.1")
	# assert REDDIT_USERNAME != ''
	# assert REDDIT_PASS != ''
	return 'Unit tests passed'

if __name__ == '__main__':
	cache = deque(maxlen=200)
	# r = praw.Reddit(user_agent = user_agent)
	# r.login(REDDIT_USERNAME, REDDIT_PASS)

	with open('named_weapons.json') as file:
		content = json.load(file)
		weapons, misspellings = content["named weapons"], content["misspellings"]

	print unit_tests()

	# while True:
	# 	for c in praw.helpers.comment_stream(r, "asoiaf"):
	# 		if c.id in cache:
	# 			continue
	# 		cache.append(c.id)
	# 		check_if_misspelled(c):
	# 	sleep(30)