from django.core.exceptions import ValidationError
from . models import ZipCode


def zip_code_validator(value):
    zip_code = ZipCode.objects.filter(zip=value).first()

    if zip_code is None:
        raise ValidationError("Zip code is not valid")

