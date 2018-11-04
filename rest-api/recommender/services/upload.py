from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os

# CONSTANTS
FILES_FOLDER = 'files'

class FileUploadService():

    # DEFAULT CONSTRUCTOR
    def __init__(self, fileName):
        self.projectDir = os.getcwd()
        self.filesDir = os.path.join(self.projectDir, FILES_FOLDER)
        self.fileName = fileName

    def uploadFile(self, file):

        # Note file is currently always overwriting
        filePath = os.path.join(self.filesDir, self.fileName)
        print("Saving File: " + str(filePath))
        default_storage.delete(filePath)
        default_storage.save(filePath, ContentFile(file.read()))