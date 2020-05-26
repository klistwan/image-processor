from flask import Flask

import settings

app = Flask(__name__, static_folder=settings.STATIC_FOLDER)