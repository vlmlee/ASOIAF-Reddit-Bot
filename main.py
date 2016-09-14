import praw
import re
import json
import spell
from time import sleep
from collections import deque
from prawoauth2 import PrawOAuth2Mini

#####################
### USER SETTINGS ###
#####################

import settings # Edit settings.py to set up your own bots.

###################
### BOT ACTIONS ###
###################

def check_if_named_weapon(c):
	oauth_helper.refresh()
	text = c.body.lower()
	tokens = str(text).split()
	words = filter_to_only_candidate_words(tokens)
	for word in words:
		check_if_misspelled(c, word)

def check_if_misspelled(c, word):
	for key, value in common_misspellings.items():
		# Does a quick check to see if the first letters of the word and key are the same
		if word[0] == key[0]:
			# If the word is in the array of common misspellings, we can skip the spell checker
			# and automatically reply with the correction and description.
			if word in value:
				reply_with_correct_spelling(c, word, key) # key allows us to grab the description
			else:
				# If the word isn't in the array, we do a spell check. If the spell check comes
				# back with the same word, the word was not misspelled. If it is a different word,
				# we check and see if it is in the common misspellings array. If the misspelling
				# is too obscure, we ignore it.
				correct_word = spell.correction(word)
				if (correct_word != word) and (correct_word in value):
					reply_with_correct_spelling(c, word, key)

def reply_with_correct_spelling(c, word, key):
	# Steps to take:
	# 1. Get misspelled word
	# 2. Tell user that it has been corrected
	# 3. Reply with description

	correction = "Did you mean *" + key + "* instead of *" + word + "*? \n\n\n"
	description = "A little bit of detail about that weapon: \n\n\n >" + weapons[key]
	footer = "\n\n*****\n\n ^(/r/ASOIAF_Named_Weapons: I'm a speller checker bot!)"
	c.reply(correction + description + footer)

###############
### HELPERS ###
###############

def filter_to_only_candidate_words(tokens):
	# heuristically filter the words
	letters = ("b", "d", "h", "i", "l", "n", "o", "r", "t", "v", "w")
	return [word for word in tokens if type(word) == str and word.startswith(letters) and len(word) > 2 and len(word) < 12]

def handle_rate_limit(func, *args, **kwargs):
	while True:
		try:
			func(*args, **kwargs)
			break
		except praw.errors.RateLimitExceeded as error:
			print error.sleep_time
			sleep(error.sleep_time)

def unit_tests():
	assert type(weapons) is dict
	assert 'brightroar' in weapons
	assert 'blackfire' not in weapons
	assert len(weapons) == 15
	assert settings.user_agent == ("ASOIAF Named Weapons Spell Checker v0.3")
	assert settings.app_key != ''
	assert settings.app_secret != ''
	assert filter_to_only_candidate_words(["one", "two", 1, "again", "wooly"]) == ["one", "two", "wooly"]
	return

############
### MAIN ###
############

if __name__ == '__main__':
	cache = deque(maxlen=200)
	reddit_client = praw.Reddit(user_agent = settings.user_agent)
	oauth_helper = PrawOAuth2Mini(reddit_client, 
								  app_key=settings.app_key,
                                  app_secret=settings.app_secret,
                                  access_token=settings.access_token,
                                  refresh_token=settings.refresh_token,
                                  scopes=settings.scopes)

	with open('docs/named_weapons.json') as file:
		content = json.load(file)
		weapons, common_misspellings = content["named weapons"], content["common misspellings"]

	while True:
		try:
			for c in reddit_client.get_comments("ASOIAF_Named_Weapons", limit=100):
				if c.id in cache:
					continue
				cache.append(c.id)
				handle_rate_limit(check_if_named_weapon, c)
			sleep(30)
		except praw.errors.OAuthInvalidToken:
			oauth_helper.refresh()