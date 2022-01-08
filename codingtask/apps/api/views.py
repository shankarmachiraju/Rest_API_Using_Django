"""Api views file."""
import logging
from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from apps.api.exceptions import InvalidInputValueException
from apps.api.filters import FunctionLogsFilter
from apps.api.models import FunctionLogs
from apps.api.serializers import FunctionLogsSerializer
from apps.api.utils import (calculate_ackermann, calculate_factorial,
                            calculate_fibonacci)
from apps.pagination import StandardResultsSetPagination
from apps.utils import api_response

logger = logging.getLogger(__name__)


func_mappings = {
    "fibonacci": calculate_fibonacci,
    "ackermann": calculate_ackermann,
    "factorial": calculate_factorial,
}


class MathAPIView(APIView):
    """Math api view class.

    This class is an HTTP API  endpoint which provides the results of math functions and then it
    saves the execution time in the database.

    Parameters
    ----------
    APIView : rest_framework.views
    """

    def _validate_input(self, query_params):
        """Validate input values given in the request query params."""
        valid_params = ("function", "m", "n")
        valid_function_names = ("fibonacci", "ackermann", "factorial")
        is_validated = True
        message = None

        if "function" not in query_params:
            is_validated = False
            message = "param missing: function"

        elif query_params.get("function") not in valid_function_names:
            is_validated = False
            message = f"Not a valid method. Options are {valid_function_names}"

        elif any(map(lambda x: x not in valid_params, query_params.keys())):
            is_validated = False
            message = f"Not a valid param. Options are {valid_params}"

        return is_validated, message

    def _save_function_log(self, **kwargs):
        """This saves the function log in db."""
        log = None
        try:
            log = FunctionLogs.objects.create(**kwargs)
        except Exception:
            logger.exception(
                f"unable to save log for method: {kwargs.get('name')}"
            )
        else:
            logger.info(f"Log {log} saved successfully into the db.")

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="function", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name="m", in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                name="n", in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER
            ),
        ],
        responses={
            200: "OK",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def get(self, request, format=None):
        """
        Http GET method. Includes the following functions:
        - Factorial
        - Fibonacci
        - Ackermann

        Parameters
        ----------
        request : django.http.request

        Returns
        -------
        rest_framework.response.Response
            returns the dict containing the results of math function,
            else it throws an error
        """
        query_params = self.request.query_params
        is_validated, message = self._validate_input(query_params)
        if not is_validated:
            return api_response(
                message=message, status_code=status.HTTP_400_BAD_REQUEST
            )

        params = query_params.copy()
        function = params.pop("function")[0]
        result = None
        try:
            start_time = datetime.now()
            # function calling
            result = func_mappings.get(function)(params)
            end_time = datetime.now()
        except InvalidInputValueException as e:
            logging.exception(str(e))
            return api_response(
                message=str(e), status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.exception(str(e))
            return api_response(
                message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        else:
            # execution time in timedelta
            time_diff = end_time - start_time
            # convert execution time to datetime.time object
            exec_time = (datetime.min + time_diff).time()
            # save the function log in the database
            self._save_function_log(
                name=function,
                input_values=str(params.dict()),
                execution_time=exec_time,
            )

            return api_response(
                data={function: result}, status_code=status.HTTP_200_OK
            )


@swagger_auto_schema(
    request_body=FunctionLogsSerializer,
    responses={"200": FunctionLogsSerializer},
)
class FunctionLogsListAPIView(ListAPIView):
    """Function logs list api view class.

    A HTTP api endpoint which shows the summary of math functions based
    on the filtered params in a paginated form.

    Parameters
    ----------
    ListAPIView : rest_framework.generics

    Raises
    ------
    if invalid data is passed in the query params, it raises
    ValidationError
        
    """

    queryset = FunctionLogs.objects.all().order_by("-id")
    serializer_class = FunctionLogsSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filter_class = FunctionLogsFilter
    permission_classes = [permissions.AllowAny]

    def initial(self, request, *args, **kwargs):  
        """
        Runs anything that needs to occur prior to calling the method handler.

        Parameters
        ----------
        request : django.http.request
        """
        super(FunctionLogsListAPIView, self).initial(request, *args, **kwargs)
        # validates the query params
        self.validate()

    def validate(self):  
        """
        Validates the query params in the given request.

        Raises
        ------
        ValidationError
            if data in the query params is invalid
        """
        valid_params = ("function", "page")

        # get query parameters from the request object
        query_params = self.request.query_params
        if any(map(lambda x: x not in valid_params, query_params.keys())):
            raise ValidationError(
                {"error": f"Not a valid param. Options are {valid_params}"}
            )
