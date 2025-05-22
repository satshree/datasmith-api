from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict


def send_with_cors(response: Response):
    """Django Rest Framework Response object with CORS Headers."""

    if settings.CORS_ORIGIN_ALLOW_ALL:
        response["Access-Control-Allow-Origin"] = "*"
    else:
        response["Access-Control-Allow-Origin"] = settings.CORS_ALLOWED_ORIGINS

    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
    # response["Access-Control-Allow-Headers"] = settings.CORS_ALLOW_HEADERS
    response["Allow"] = "GET, POST, OPTIONS, PUT, DELETE"
    return response


def success_response(data=None, message=None, error=None, status=status.HTTP_200_OK):
    """
    Django Rest Framework Response object with CORS Headers for Success Response.

    Default HTTP Status Code: 200 OK
    """

    new_data = {}
    new_data["status"] = True

    if message:
        new_data["message"] = message

    if error:
        new_data["error"] = error

    if type(data) in (list, dict, ReturnList, ReturnDict):
        new_data["results"] = data

    response = Response(new_data, status=status)
    return send_with_cors(response)


def error_response(
    message, data=None, error=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR
):
    """
    Django Rest Framework Response object with CORS Headers for Error Response.

    Default HTTP Status Code: 500 INTERNAL SERVER ERROR
    """

    new_data = {}
    new_data["status"] = False
    new_data["message"] = message

    if error:
        new_data["error"] = error

    if type(data) in (list, dict, ReturnList, ReturnDict):
        new_data["results"] = data

    response = Response(new_data, status=status)
    return send_with_cors(response)
