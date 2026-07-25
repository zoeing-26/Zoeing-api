from rest_framework import status
# import api.constants.messages as msg
from rest_framework.response import Response


def error_response(
    message, error_code=None, data={}, status_code=status.HTTP_400_BAD_REQUEST
):
    return Response(
        {"error": message, "error_code": error_code, "data": data}, status=status_code
    )


def success_response(message, data=[], status_code=status.HTTP_200_OK):
    rsp_message = {"message": message}
    if data:
        rsp_message["data"] = data
    else:
        rsp_message["data"] = []
    return Response(rsp_message, status=status_code)


def create_response(message, data=[]):
    return success_response(
        message=message, data=data, status_code=status.HTTP_201_CREATED
    )


def update_response(message, data=[]):
    return success_response(message=message, data=data)

def custom_response(data, status_code):
    return Response(data, status=status_code)
