import uuid

import flask
from flask import request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Thumbnail

from app import app

engine = create_engine('sqlite:///image_processor.db', echo=True)

@app.route('/v1/thumbnails', methods=['POST'])
def add_thumbnail_request():
    if 'url' not in request.get_json():
        return "Error: No url provided. Please specify a url.", 422

    original_url = request.args.get('url')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a new thumbnail request.
    tid = str(uuid.uuid4())
    new_thumbnail = Thumbnail(tid, request.get_json()['url'])
    session.add(new_thumbnail)
    session.commit()

    # Respond back to the user.
    return jsonify(new_thumbnail), 201


@app.route('/v1/thumbnails', methods=['GET'])
def get_thumbnail():
    thumbnail_id = request.args.get('id')
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Thumbnail).filter(Thumbnail.id==thumbnail_id)
    return jsonify(result.first())

if __name__ == '__main__':
    app.run()