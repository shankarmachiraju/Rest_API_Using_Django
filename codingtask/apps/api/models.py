"""Api models file."""
from django.db import models
from django.utils.translation import ugettext as _


class FunctionLogs(models.Model):
    """Function logs model class.

    Parameters
    ----------
    models : django.db
    """

    name = models.CharField(_("name"), max_length=50, db_index=True)
    input_values = models.CharField(_("input_values"), max_length=50)
    execution_time = models.TimeField(_("execution_time"))

    class Meta:  
        verbose_name = "functionlog"
        verbose_name_plural = "functionlogs"

    def __str__(self):
        """Str representation of functionlogs model.

        Returns
        -------
        str
            containing function name and execution time of the given object
        """
        return f"{self.name}: {self.execution_time}"
