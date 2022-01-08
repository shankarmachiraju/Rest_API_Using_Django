"""Views test cases."""
import logging

import ddt
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from apps.api.models import FunctionLogs


@ddt.ddt
class MathAPIViewTestCase(TestCase):
    """ test cases.
    """

    @classmethod
    def setUpClass(cls):
        """Set up class for math api view test cases."""
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        """Tear down class for math api view test cases."""
        logging.disable(logging.NOTSET)

    def setUp(self):
        """Set up the api url for each test case."""
        self.url = reverse("math")

    def test_http_codes(self):
        """Test allowed or disallowed methods on the given url."""
        res = self.client.get(self.url, {"function": "factorial", "n": 1})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.get(self.url, {"function": "factorial", "n": -1})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        res = self.client.post(self.url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        res = self.client.put(self.url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        res = self.client.delete(self.url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @ddt.data(
        ({"function": "factorial", "n": 1}, {"factorial": 1}),
        ({"function": "fibonacci", "n": 3}, {"fibonacci": [1, 1, 2]}),
        ({"function": "ackermann", "m": 2, "n": 1}, {"ackermann": 5}),
    )
    @ddt.unpack
    def calculate_function_result(self, query_params, response_data):
        """
        calculates the function results according to given
        method and input values.
        """
        res = self.client.get(self.url, query_params).json()
        self.assertEqual(res.get("data"), response_data)

    @ddt.data(
        ("factorial", {"function": "factorial", "n": 1}, "{'n': '1'}"),
        ("fibonacci", {"function": "fibonacci", "n": 3}, "{'n': '3'}"),
        (
            "ackermann",
            {"function": "ackermann", "m": 2, "n": 1},
            "{'m': '2', 'n': '1'}",
        ),
    )
    @ddt.unpack
    def save_function_log_in_db(
        self, func_name, query_params, input_values
    ):
        """Test that url and save the function logs in the database."""
        self.client.get(self.url, query_params)
        log = FunctionLogs.objects.get(name=func_name)
        self.assertEqual(log.name, func_name)
        self.assertEqual(log.input_values, input_values)

    @ddt.data(
        ({"n": 1}, "param missing: function"),
        (
            {"function": "fib", "n": 3},
            "Not a valid method. Options are ('fibonacci', 'ackermann', 'factorial')",  
        ),
        (
            {"function": "factorial", "q": 1},
            "Not a valid param. Options are ('function', 'm', 'n')",
        ),
        ({"function": "factorial", "n": 2.5}, "'n' should be integer"),
        ({"function": "factorial", "n": -2}, "invalid/missing param 'n'"),
        ({"function": "fibonacci"}, "invalid/missing param 'n'"),
    )
    @ddt.unpack
    def invalid_params_returns_error(
        self, query_params, err_msg
    ):
        """Test that URL with invalid params returns error in the response."""
        res = self.client.get(self.url, query_params).json()
        self.assertEqual(res.get("data"), None)
        self.assertEqual(res.get("message"), err_msg)


@ddt.ddt
class FunctionLogsListAPIViewTestCase(TestCase):
    """Function logs api list view test cases.

    Parameters
    ----------
    TestCase : django.test
    """

    def setUp(self):
        """Set up the api urls and database records for each test case."""
        self.math_api_url = reverse("math")
        self.func_logs_url = reverse("funclogs-summary")
        self.query_params_list = [
            {"function": "factorial", "n": 1},
            {"function": "fibonacci", "n": 2},
            {"function": "ackermann", "m": 2, "n": 1},
            {"function": "factorial", "n": 4},
            {"function": "factorial", "n": 3},
        ]
        # save function logs in the database
        for query_params in self.query_params_list:
            self.client.get(self.math_api_url, query_params)

    def return_paginated_data(self):
        """returns the paginated data in the response."""
        res = self.client.get(self.func_logs_url).json()
        self.assertEqual(res.get("count"), len(self.query_params_list))
        self.assertEqual(
            res.get("next"), "http://devserver/api/funclogs-summary/?page=2"
        )
        # assert that results are equal to the page size of pagination
        self.assertEqual(len(res.get("results")), 2)

    @ddt.data(({"function": "factorial"}, 3), ({"function": "ackermann"}, 1))
    @ddt.unpack
    def filters_returns_filtered_data(
        self, query_params, expected_count
    ):
        """Test  url returns the filtered data in the response."""
        res = self.client.get(self.func_logs_url, query_params).json()
        self.assertEqual(res.get("count"), expected_count)

    @ddt.data(
        {"func": "factorial"}, {"function": "factorial", "test": "test_param"}
    )
    def invalid_filter_param_returns_error_response(
        self, query_params
    ):
        """
        Test url with the invalid filter params that returns an error
        in the response.
        """
        res = self.client.get(self.func_logs_url, query_params).json()
        self.assertEqual(
            res.get("error"),
            "Not a valid param. Options are ('function', 'page')",
        )
