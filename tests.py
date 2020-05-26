import json
import unittest
from unittest.mock import patch

from api import app

class APITestCase(unittest.TestCase):
	def setUp(self):
		self.image_url = "https://www.fullstackpython.com/img/logos/flask.jpg"
	def test_get_invalid_thumbnail(self):
		fake_tid = 1
		response = app.test_client().get(f"/v1/thumbnails?id={fake_tid}")
		self.assertEqual(response.status_code, 404)
		json_response = json.loads(response.data)
		self.assertEqual(json_response['status'], 404)
		self.assertEqual(json_response['message'], f"Thumbnail {fake_tid} not found")

	def test_add_thumbnail_request(self):
		response = app.test_client().post(
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
		mock_redis_get.return_value = {'id': real_id, 'url': self.image_url}
		response = app.test_client().get(f"/v1/thumbnails?id={real_id}")
		json_response = json.loads(response.data)
		self.assertEqual(json_response['url'], self.image_url)


if __name__ == '__main__':
	unittest.main()