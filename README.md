## Workflow 
The Flask API application makes use of a Redis key-value store to store request information, and enqueues thumbnail generation requests via Redis Queue.

1. Client makes a POST request to generate a new thumbnail
2. The Flask API server stores the request information in Redis and enqueues it onto a Redis Queue
3. Available workers retrieve the request's information from Redis, generate a thumbnail, and update Redis
4. Client makes a GET request to retrieve the URL of the thumbnail

If needed, the client can poll the API endpoint and retrieve status of the thumbnail generation request.

![Optional Text](images/api_request_workflow.jpg)

## Image Processing Libraries
There are many Python libraries that offer image processing functionality:
- [scikit-image](https://github.com/scikit-image/scikit-image) - 3.7k stars, last commit yesterday, 366 contributors
- [Pillow](https://github.com/python-pillow/Pillow) - 7.3k stars, last commit yesterday, 270 contributors
- [OpenCV](https://github.com/skvark/opencv-python)  - 1.3k stars, last commit in April, 20 contributors
- [PIL](http://www.pythonware.com/products/pil/) - discontinued and lacks Python 3 support

In this case, I decided to be pragmatic and choose Pillow. It's received a lot of positive feedback on StackOverflow and resizing an image into a 100x100px can be done in three lines of code:

```python
image = Image.open("mt_fuji.jpg")
image.thumbnail((100,100))
image.save("thumbnail.jpg")
```

When building such a system for production use, much more in-depth research should be done, alongside proper performance testing. For example, just looking at Pillow's [performance testing(https://python-pillow.org/pillow-perf/), there's a highly optimized downstream fork named [Pillow-SIMD](https://github.com/uploadcare/pillow-simd) that is both production-ready and comes with performance improvements.

Resize functionality can also be implemented using [different algorithms](https://uploadcare.com/blog/the-fastest-image-resize/) (e.g. fast nearest neighbour, convolution resampling). As a result, depending on our constraints (e.g. memory, CPU, execution time, photo quality), we'd want to look more in-depth at any library we're considering to understand the details of how it works and why it works the way. 

## Task Queues
Within the Python ecosystem, there are a handful of [different task queues](https://www.fullstackpython.com/task-queues.html) you can use (sorted in order of popularity):
- [Celery](https://github.com/celery/celery) - most popular; supports both RabbitMQ and Redis as brokers
- [Redis Queue](https://github.com/rq/rq) - a simple library, apparently much easier to use than Celery.
- [Huey](https://github.com/coleifer/huey) - a lightweight redis-based queue with flexible scheduling
- [Dramatiq](https://github.com/Bogdanp/dramatiq) - fast, reliable alternative to Celery with RabbitMQ/Redis as brokers.

Since each task queue offers its own set of features and functionality, it'd be worthwhile to do further research depending on our use case (and potential use cases) to determine the right one to use. In a real-life setting, it also may be worth prototyping proof of concepts (POCs) with each one during evaluation.

To be pragmatic for this project, I opted for Redis Queue given its claims on being simpler and more lightweight than Celery.

## Database Choice
For this project, even though there weren't requirements for transactions, strict schema, complex joins, I decided to go with SQLite. It's easy to use and simple to setup, but in a real-life scenario, if we're more concerned with high availability than strong consistency, it may be worthwhile to explore a NoSQL type database.

## Usage
Requesting a new image to be resized:
```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"url": "https://images.pexels.com/photos/206359/pexels-photo-206359.jpeg"}' http://localhost:5000/v1/thumbnails
{"id":"96b725d0-14f5-48b7-b8b1-2182219fbf06","status":"queued","url":"https://images.pexels.com/photos/206359/pexels-photo-206359.jpeg"}
```

Checking status of an image:
```bash
curl http://127.0.0.1:5000/v1/thumbnails?id=96b725d0-14f5-48b7-b8b1-2182219fbf06
```
