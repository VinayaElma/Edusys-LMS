import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.svg', '.gif', '.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls', '.c', '.txt', '.py', '.html']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
