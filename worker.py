import json
import os
import requests
import shutil

from flask import Flask, abort, request, jsonify, Response
from PIL import Image

app = Flask(__name__)
app.config["DEBUG"] = True

def download_image(url):
	response = requests.get(url, stream=True)
	with open('temporary.jpeg', 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)
	del response
	return 'temporary.jpeg'

def resize(filepath):
	image = Image.open(filepath)
	image.thumbnail((100,100))
	new_url = "thumbnail.jpg"
	image.save(new_url)
	os.remove(filepath)
	return new_url

def main():
	response = requests.get(request.json['url'], stream=True)
	if response.status_code == 404:
		error_message = json.dumps({'Message': 'Photo not found.'})
		abort(Response(error_message, 404))
	# Download image.
	local_url = download_image(request.json['url'])
	resized_url = resize(local_url)
	return jsonify({'url': resized_url}, 201)


