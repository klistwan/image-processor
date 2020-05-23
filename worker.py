import json
import os
import requests
import shutil

from flask import Flask, abort, request, jsonify, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from PIL import Image

from models import Thumbnail

engine = create_engine('sqlite:///image_processor.db', echo=True)

def _download_image(url):
	try:
		response = requests.get(url, stream=True, timeout=(2, 5))
	except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
		return None
	with open('temporary.jpeg', 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)
	del response
	return 'temporary.jpeg'

def _create_thumbnail(filepath):
	image = Image.open(filepath)
	image.thumbnail((100,100))
	new_url = "thumbnail.jpg"
	image.save(new_url)
	os.remove(filepath)
	return new_url

def generate_thumbnail(id, url):
	# Query the DB to get this thumbnail request.
	Session = sessionmaker(bind=engine)
	session = Session()
	result = session.query(Thumbnail).get(id)

	# Try to download the image.
	local_url = _download_image(url)
	if local_url:
		# If successful, resize.
		resized_url = _create_thumbnail(local_url)
		result.resized_url = resized_url
	else:
		# If not, mark this request as failed.
		result.status = 'failed'

	session.commit()
	#return jsonify(result)
