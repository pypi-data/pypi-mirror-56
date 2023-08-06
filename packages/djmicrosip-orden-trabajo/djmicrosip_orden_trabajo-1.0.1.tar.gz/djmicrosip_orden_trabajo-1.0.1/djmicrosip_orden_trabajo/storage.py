from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name):
        # Si el nombre del archivo existe, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

def actualizar_datos(model,connection):
	pass
