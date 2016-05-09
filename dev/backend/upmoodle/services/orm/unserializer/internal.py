# noinspection PyUnresolvedReferences
from copy import copy


def unserialize(model, fields, form, *args, **kwargs):
    fields_copy = copy(fields)
    optional = kwargs.get('optional', False)

    for field in fields_copy:
        # If the field doesnt exists raises an MultiValueDictKeyError
        try:
            setattr(model, field, form[field])
        except KeyError as m:
            if not optional:
                raise m
            else:
                fields.remove(field)
    return model
