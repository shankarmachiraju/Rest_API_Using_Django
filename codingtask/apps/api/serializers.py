"""Api serializers file."""
from rest_framework import serializers

from apps.api.models import FunctionLogs


class FunctionLogsSerializer(serializers.ModelSerializer):
    """Function Logs serializer class.

    Parameters
    ----------
    serializers : rest_framework
    """

    class Meta:
        model = FunctionLogs
        # display all the model fields except `id`
        exclude = ["id"]
