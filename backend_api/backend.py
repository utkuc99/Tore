from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import os

from shorten import shorten_video
from archiveManager import checkArchive, writeArchieve
from download import download_video
from upload import upload_to_aws

app = Flask(__name__)
CORS(app)
api = Api(app)

class Api(Resource):
    def get(self):
        return "Please use post request to process video."  # return data and 200 OK code
    def post(self):
        args = request.args
        videoId = args['videoId']

        aResult = checkArchive(videoId)

        if(aResult):
            print( "i have ittt!!")
            return True
        else:
            dResult = download_video(videoId)
            sResult = shorten_video(videoId)
            writeArchieve(videoId)
            return True

        return False

api.add_resource(Api, '/api')  # '/users' is our entry point for Users

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
