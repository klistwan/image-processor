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
		filetype = self.url.split('.')[-1]
		return f"{settings.STATIC_FOLDER}/{self.id}.{filetype}"

	def download_image(self):
		try:
			response = requests.get(self.url, stream=True, timeout=(2, 5))
		except Exception as e:
			self.status = 'failed'
			self.error_message = e.__str__()
			return
		with open(self.local_url(), 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		del response

	def resize(self):
		# Fail error if image failed to download.
		if self.status == 'failed':
			return
		# TODO: Add error handling if image can't be opened.
		image = Image.open(self.local_url())
		# TODO: Decide what to do if submitted images are smaller than 100px by 100px.
		# TODO: Remove hard-coded sizes and make resize configurable.
		image.thumbnail((100,100))
		# TODO: Add error handling if saving image fails.
		image.save(self.local_url())
		self.resized_url = f"{FLASK_HOST_AND_PORT}/{self.local_url()}"
		self.status = 'completed'

def generate_thumbnail(tid):
	# TODO: Elminate this Redis call at the API level by submitting a job with the serialized request.
	thumbnail = json.loads(redis_conn.get(tid))
	generator = ThumbnailGenerator(**thumbnail)
	generator.download_image()
	generator.resize()
	redis_conn.set(tid, json.dumps(generator.__dict__))
