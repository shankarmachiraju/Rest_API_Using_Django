"""Api filters file."""
from django_filters import FilterSet, filters

from apps.api.models import FunctionLogs


class FunctionLogsFilter(FilterSet):
    """Function logs filter class.

    This provides filters on the given set of input data.

    Parameters
    ----------
    FilterSet : django_filters
    """

    function = filters.CharFilter(field_name="name", lookup_expr="exact")

    class Meta:  
        model = FunctionLogs
        fields = ["function"]
