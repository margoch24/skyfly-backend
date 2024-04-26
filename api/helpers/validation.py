from marshmallow import ValidationError, validate

from api.constants import CabinClass


def class_props_to_arr(Class):
    values = [getattr(Class, attr) for attr in dir(Class) if not attr.startswith("__")]
    return values


def price_range_validation(value):
    try:
        [min, max] = value.split(",")

        min_to_num = float(min)
        max_to_num = float(max)

        if min_to_num < 0 or max_to_num < 0:
            raise ValidationError

        if min_to_num >= max_to_num:
            raise ValidationError
    except:
        raise ValidationError("Invalid price range format. Use 'price=min,max' format.")


def cabin_class_validation(value):
    try:
        values = value.split(",")
        choices = class_props_to_arr(CabinClass)

        isValid = any(element in values for element in choices)
        if not isValid:
            raise ValidationError
    except:
        raise ValidationError(f"Must be one of: {', '.join(choices)}.")
