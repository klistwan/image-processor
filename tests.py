import json
import unittest

from api import app

class APITestCase(unittest.TestCase):
	def test_get_thumbnail(self):
		fake_tid = 1
		response = app.test_client().get(f"/v1/thumbnails?id={fake_tid}")
		self.assertEqual(response.status_code, 404)
		json_response = json.loads(response.data)
		self.assertEqual(json_response['status'], 404)
		self.assertEqual(json_response['message'], f"Thumbnail {fake_tid} not found")


if __name__ == '__main__':
	unittest.main()