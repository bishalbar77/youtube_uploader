import os
import io
from googleapiclient.http import MediaIoBaseDownload
from flask import Flask, jsonify, request
from flask_cors import CORS,cross_origin
from Google import Create_Service
from werkzeug.utils import secure_filename
from argparse import Namespace
from upload import uploadfun
from googleapiclient.http import MediaFileUpload

CLIENT_SECRET_FILE = os.environ.get('client_secret')
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

app = Flask(__name__)
CORS(app)


FILE_NAME = 'video.mp4'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def helloWorld():
    return "Flask App Running"

@app.route('/add_video_to_youtube_playlist', methods=['POST'])
def add_video_to_youtube_playlist():
    fileId = request.form.get('drive_link') 
    title = request.form.get('title') 
    description = request.form.get('description') 
    playlist_id = request.form.get('playlist_id') 
    response = service.files().get_media(fileId=fileId[32:])
    fileByte = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fileByte, request=response)

    # done = False
    # while not done:
    #     status, done = downloader.next_chunk()
    #     print('Download progress {0}'.format(status.progress() * 100))

    # fileByte.seek(0)

    # with open(os.path.join(UPLOAD_FOLDER, FILE_NAME), 'wb') as f:
    #     f.write(fileByte.read())
    #     f.close()
        
    # mediaBody = MediaFileUpload('./static/uploads/video.mp4')
    # argss = Namespace(
    #     auth_host_name='localhost', 
    #     auth_host_port=[8000, 8080], 
    #     category='27', 
    #     description=description, 
    #     keywords='', 
    #     file=mediaBody,
    #     logging_level='ERROR', 
    #     noauth_local_webserver=False, 
    #     privacyStatus='private', 
    #     title=title
    # )
    # finalResponse = uploadfun(argss, playlist_id)
    return jsonify({'status' : "Success", 'status_code' : 200, 'message' : "Video will be added to the playlist!", 'data' : ''})

if __name__ == "__main__":
    app.run(debug=True)