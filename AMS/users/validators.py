from django.core.exceptions import ValidationError

# Validator to validate the image field against these below extensions
def validate_image_file_extension(value):
    valid_extensions = ['jpg', 'jpeg', 'png']
    if not value.name.split('.')[-1] in valid_extensions:
        raise ValidationError('Unsupported file extension.')
    