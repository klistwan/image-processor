import os

from flask import Flask, abort, request, jsonify, Response
from PIL import Image
from json import dumps

app = Flask(__name__)
app.config["DEBUG"] = True


def resize(filepath):
	image = Image.open(filepath)
	image.thumbnail((100,100))
	new_url = "thumbnail.jpg"
	image.save(new_url)
	return new_url


@app.route('/resize', methods=['POST'])
def home():
	if not request.json or not 'url' in request.json:
		abort(400)
	if not os.path.exists(request.json['url']):
		error_message = dumps({'Message': 'Photo not found.'})
		abort(Response(error_message, 404))
	resized_url = resize(request.json['url'])
	return jsonify({'url': resized_url}, 201)


app.run()