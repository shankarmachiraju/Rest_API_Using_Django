from rest_framework.response import Response


def api_response(status_code, data=None, message=None):
    """
    
    Parameters
    ----------
    status_code: str
        http status code
    message: str
        success/error message
    data: dict
        api data

    Returns
    -------
    rest_framework.response.Response
        returns the dict containing data and message of the given API
    """
    return Response(
        data={"data": data, "message": message}, status=status_code
    )
