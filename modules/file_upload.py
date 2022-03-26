import firebase_admin
from firebase_admin import credentials, firestore, storage
import time, os
from django import forms

MAX_UPLOAD_SIZE = 5242880

class UploadFile(object):
    def __init__(self, request, filename=None):
        self.file = request.FILES[filename] if filename in request.FILES.keys() else None

        self.cred=credentials.Certificate(os.getcwd() + '/modules/project-showcase-cred.json')
        try:
            firebase_admin.initialize_app(self.cred, {
                'storageBucket': 'project-showcase-e6617.appspot.com',
            })
        except:
            pass

        self.db = firestore.client()
        self.bucket = storage.bucket()

    def is_valid(self):
        if self.file.size <= MAX_UPLOAD_SIZE:
            return True
        else:
            return {'status': False, 'msg': 'Must be less than 5MB!'}

    def upload(self):
        try:
            self.file_name = str(int(time.time())) + '-' + self.file.name 
            blob = self.bucket.blob(self.file_name)
            blob.upload_from_file(self.file, content_type=self.file.content_type, timeout=30)
            blob.make_public()
            return blob.public_url
        except Exception as e:
            if 'timeout' in str(e).lower():
                self.error_msg = 'File too large, or slow connection.'
                return False
            
            self.error_msg = 'Error occured.'
            return False

    def delete(self, firebase_url=None):
        if firebase_url == None:
            return
        
        blobs = self.bucket.list_blobs()
        for blob in blobs:
            if firebase_url in blob.public_url:
                blob.delete()
