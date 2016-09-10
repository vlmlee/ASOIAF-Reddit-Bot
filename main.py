import praw
import re
import json
import spell
from time import sleep
from collections import deque

# User settings
import settings

def mispelled(c):
	text = c.body.lower()
	tokens = text.split()
	letters = ("b", "d", "h", "i", "l", "n", "o", "r", "t", "v", "w")
	words_to_spellcheck = [word for word in tokens if word.startswith(letters) and len(word) > 2 and len(word) < 12]

	for item in words_to_spellcheck:
		if check_if_named_weapon(item):
			return True

def check_if_named_weapon(word):
	if not correction(word):
		# if word is spelled correctly
		return False
	else
		# if word is a slight mispelling
		if condition: # check if the mispelled word matches any of the weapons
			return True

def correct_spelling(c, verbose=True, respond=False):
	# find corrected word
	# tell user that it has been corrected
	# reply with description
	correction = "Returning the corrected word and description"

	if verbose:
		print c.body.encode('UTF-8')
		print "\n\n~~~~"
		print fixed.encode('UTF-8')

	if respond: 
		head = "Hi, I'm testing this bot!"
		c.reply(head + correction)


if __name__ == '__main__':
	cache = deque(maxlen=200)
	r = praw.Reddit(user_agent = user_agent)
	r.login(REDDIT_USERNAME, REDDIT_PASS)

	with open('named_weapons.json') as file:
		weapons, mispellings = json.load(file)["named weapons"], json.load(file)["mispellings"]

	while True:
		for c in praw.helpers.comment_stream(r, "asoiaf"):
			if c.id in cache:
				continue
			cache.append(c.id)
			if mispelled(c):
				correct_spelling(c, respond=True)
		sleep(30)