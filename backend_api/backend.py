from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import os

from shorten import shorten_video
from archiveManager import checkArchive, writeArchieve
from download import download_video

app = Flask(__name__)
CORS(app)
api = Api(app)

class Api(Resource):
    def get(self):
        return "Please use post request to process video."  # return data and 200 OK code
    def post(self):

        #Parse arguments
        args = request.args
        videoId = args['videoId']

        #Check video Archieve
        aResult = checkArchive(videoId)

        if(aResult):
            print( "i have ittt!!")
            return "http://localhost:8080/" + videoId + "_short.mp4"
        else:
            dResult = download_video(videoId) #Download Video
            sResult = shorten_video(videoId)  #Shorten Video
            writeArchieve(videoId) #Write2Archieve
            return "http://localhost:8080/" + sResult

#Create API
api.add_resource(Api, '/api')  # '/users' is our entry point for Users

#Run Flask Server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
