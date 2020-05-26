import json
import os
import requests
import shutil

from flask import Flask, request, jsonify
from redis import Redis
from PIL import Image

from app import app
import settings

redis_conn = Redis(host=os.environ['REDIS_HOST'], port=6379)
FLASK_HOST_AND_PORT = os.environ['FLASK_RUN_HOST'] + ":" + os.environ['FLASK_PORT']


class ThumbnailGenerator():
	def __init__(self, **entries):
		self.__dict__.update(entries)

	def local_url(self):
		return f"{settings.STATIC_FOLDER}/{self.id}.jpeg"

	def download_image(self):
		try:
			response = requests.get(self.url, stream=True, timeout=(2, 5))
		except Exception as e:
			self.status = 'failed'
			self.error_message = e.__str__()
			return False
		with open(self.local_url(), 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		del response
		return True

	def resize(self):
		if self.status == 'failed':
			return
		image = Image.open(self.local_url())
		image.thumbnail((100,100))
		image.save(self.local_url())
		self.resized_url = f"{FLASK_HOST_AND_PORT}/{self.local_url()}"
		self.status = 'completed'
		return True

def generate_thumbnail(tid):
	thumbnail = json.loads(redis_conn.get(tid))
	generator = ThumbnailGenerator(**thumbnail)
	generator.download_image()
	generator.resize()
	redis_conn.set(tid, json.dumps(generator.__dict__))
