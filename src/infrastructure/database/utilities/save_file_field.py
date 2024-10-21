import os
from sqlalchemy import String, TypeDecorator
# from werkzeug.utils import secure_filename  # Удобно для получения безопасного имени файла

# Настройки для пути к директории загрузок
UPLOAD_FOLDER = 'media/galery'

class SaveFileField(TypeDecorator):
    impl = String

    # Указываем максимальный размер поля в БД
    def __init__(self, length=None, *args, **kwargs):
        super(SaveFileField, self).__init__(length=length, *args, **kwargs)

    def process_bind_param(self, value, dialect):

        if value is None:
            return None

        
        # filename = secure_filename(value.filename)
        filename = value.filename
        relative_path = os.path.join('media/galery', filename)
        absolute_path = os.path.join(UPLOAD_FOLDER, filename)

        value.save(absolute_path)
        return relative_path
    

    def process_result_value(self, value, dialect):

        if value is None:
            return None

        return os.path.join(UPLOAD_FOLDER, value)