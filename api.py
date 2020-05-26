import json
import os
import uuid

from flask import Flask, request, jsonify, send_from_directory
from redis import Redis
from rq import Queue

from app import app
from worker import generate_thumbnail

redis_conn = Redis(host=os.environ['REDIS_HOST'], port=6379)
q = Queue(connection=redis_conn)


@app.route('/v1/thumbnails', methods=['POST'])
def add_thumbnail_request():
    if 'url' not in request.json:
        return jsonify("Error: No url provided. Please specify a url."), 422

    # Create a new thumbnail request.
    thumbnail = request.json
    thumbnail['id'] = str(uuid.uuid4())
    thumbnail['status'] = 'queued'
    redis_conn.set(thumbnail['id'], json.dumps(thumbnail))

    # Enqueue it.
    q.enqueue(generate_thumbnail, args=(thumbnail['id'], ))

    # Respond back to the user.
    return jsonify(thumbnail), 201


@app.route('/v1/thumbnails', methods=['GET'])
def get_thumbnail():
    tid = request.args.get('id', '')
    thumbnail = redis_conn.get(tid)
    if not thumbnail:
        message = {'status': 404, 'message': f"Thumbnail {tid} not found"}
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    return thumbnail, 200


@app.route('/<path:filename>')
def send_file(filename):
    return send_from_directory(app.static_folder, filename)


if __name__ == '__main__':
    app.run(host=os.environ['FLASK_RUN_HOST'])
