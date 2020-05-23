import json
import os
import requests
import shutil

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Thumbnail

from flask import Flask, abort, request, jsonify, Response
from PIL import Image

engine = create_engine('sqlite:///image_processor.db', echo=True)

def _download_image(url):
	response = requests.get(url, stream=True)
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
	# First, download the image from the given url.
	local_url = _download_image(url)
	# Next, resize the image and get its new URL.
	resized_url = _create_thumbnail(local_url)
	# Update the database.
	Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Thumbnail).get(id)
    result.resized_url = resized_url
    session.commit()
    return resized_url
