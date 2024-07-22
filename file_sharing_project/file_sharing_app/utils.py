import os
import uuid
from django.conf import settings
from django.core.files.storage import default_storage

def generate_download_url(file):
    file_path = os.path.join(settings.MEDIA_ROOT, file.file.path)
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_name)[1]
    file_id = str(uuid.uuid4())

    download_url = f'http://localhost:8000/media/{file_id}{file_extension}'

    # Save the download URL to the file model
    file.download_url = download_url
    file.save()

    return download_url