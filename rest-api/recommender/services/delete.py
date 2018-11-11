from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os

# CONSTANTS
FILES_FOLDER = 'files'

class FileDeleteService():

    # DEFAULT CONSTRUCTOR
    def __init__(self, userID):
        self.userID = userID

    def deleteFile(self, file):
        
        # Note file is currently always overwriting
        print("Deleting File: " + str(file))
        default_storage.delete(file)