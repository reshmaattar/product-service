from rest_framework.response import Response
from rest_framework.views import status
from functools import wraps
import json,ast,copy
from jsonschema import FormatChecker, validate, ValidationError 

def error_response(message):
    return Response(
                data={
                    "message": message
                },
                status=status.HTTP_400_BAD_REQUEST
            )

"""
form data always send data in string to converted it in correct form

"""
def convert_type(val):
    try:
        val = ast.literal_eval(val)
    except ValueError:
        pass
    return val
"""
convert QueryDict to dict assuming each key has one value and
This is used for form data
"""
def convert_dict(data):
    new_data = {}
    for k in data:
        if k != 'csrfmiddlewaretoken':
            new_data[k]=convert_type(data[k])
    return new_data

def validate_json(schema=None):
    if schema is None:
        schema = dict()

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if args[0].request.headers["Content-Type"] == "application/json":
                data = args[0].request.data
            elif "multipart/form-data" in args[0].request.headers["Content-Type"]:
                data = convert_dict(args[0].request.data)
            else:
                return error_response("content type must be application/json")
            if data is None:
                return error_response("data is none")
            try:
                validate(data, schema, format_checker=FormatChecker())
            except ValidationError as e:
                return error_response(e.message)
            return f(*args, **kwargs)

        return decorated_function

    return decorator