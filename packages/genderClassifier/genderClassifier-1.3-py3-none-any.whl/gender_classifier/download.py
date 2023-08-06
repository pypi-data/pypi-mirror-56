# SWAMI KARUPPASWAMI THUNNAI

import requests

def latest_model():
	r = requests.get("https://github.com/VISWESWARAN1998/gender_classifier/releases/download/1.0/gender_v2.h5", stream=True)
	with open("gender_v2.h5", "wb") as file:
		count = 1
		for i in r.iter_content(chunk_size=1024):
			print("Downloading model's chunk {} of 132444".format(count))
			count += 1
			file.write(i)
