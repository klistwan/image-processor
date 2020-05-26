import json
import os
import unittest
from unittest.mock import patch

from PIL import Image

import api
import worker

class APITestCase(unittest.TestCase):
	def setUp(self):
		self.image_url = "https://www.fullstackpython.com/img/logos/flask.jpg"

	def test_get_invalid_thumbnail(self):
		fake_tid = 123456789
		response = api.app.test_client().get(f"/v1/thumbnails?id={fake_tid}")
		self.assertEqual(response.status_code, 404)
		json_response = json.loads(response.data)
		self.assertEqual(json_response['status'], 404)
		self.assertEqual(json_response['message'], f"Thumbnail {fake_tid} not found")

	def test_add_thumbnail_request(self):
		response = api.app.test_client().post(
			'/v1/thumbnails',
			data=json.dumps({'url': self.image_url}),
			content_type='application/json',
		)
		self.assertEqual(response.status_code, 201)
		data = json.loads(response.get_data(as_text=True))
		self.assertEqual(data['status'], 'queued')
		self.assertEqual(data['url'], self.image_url)

	@patch('api.redis_conn.get')
	def test_valid_thumbnail(self, mock_redis_get):
		real_id = '12345'
		mock_redis_get.return_value = json.dumps({'id': real_id, 'url': self.image_url})
		response = api.app.test_client().get(f"/v1/thumbnails?id={real_id}")
		json_response = json.loads(response.data)
		self.assertEqual(json_response['url'], self.image_url)


class WorkerTestCase(unittest.TestCase):
	def setUp(self):
		self.image_url = "https://www.fullstackpython.com/img/logos/flask.jpg"
		self.real_id = "96b725d0-14f5-48b7-b8b1-2182219fbf06"

	def test_resize(self):
		# TODO: Turn this integration-like unit test into a proper deterministic unit test mocking HTTP calls.
		generator = worker.ThumbnailGenerator(**{'id': self.real_id, 'url': self.image_url, 'status': 'queued'})
		generator.download_image()
		generator.resize()
		self.assertEqual(generator.status, 'completed')
		with Image.open(generator.local_url()) as img:
			self.assertTrue(100 in img.size)
		os.remove(generator.local_url())

	def test_invalid_resize(self):
		generator = worker.ThumbnailGenerator(**{'url': "http://notawebsite.ca/fake.jpg", 'status': 'queued'})
		generator.download_image()
		self.assertEqual(generator.status, 'failed')



if __name__ == '__main__':
	unittest.main()