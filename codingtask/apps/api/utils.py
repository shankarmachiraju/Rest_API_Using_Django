"""Api math utility file."""
from apps.api.exceptions import InvalidInputValueException


def calculate_fibonacci(params):
    """
    Function to calculate the fibonacci series for the `n` numbers.

    Parameters
    ----------
    params : dict
        containing the input value

    Returns
    -------
    list
        containing a list of fibonacci series

    Raises
    ------
    if n is not given, n is negative or n is not integer
        then the function raises an InvalidInputValueException
        
    """
    fibonacci_list = []
    a, b = 0, 1
    try:
        n = int(params.get("n", -1))
    except Exception:
        raise InvalidInputValueException("'n' should be integer")
    else:
        if n < 0:
            raise InvalidInputValueException("invalid/missing param 'n'")
        for i in range(n):
            fibonacci_list.append(b)
            a, b = b, a + b
        return fibonacci_list


def calculate_ackermann(params):
    """
    Calculate the ackermann value with the given `m` and `n` values.

    Parameters
    ----------
    params : dict
        containing the input values

    Returns
    -------
    int
        containing an ackermann value

    Raises
    ------
    if m/n is not given, m/n is negative or m/n is not integer
        raises an InvalidInputValueException
        
    """

    def A(m, n):
        if m == 0:
            return n + 1
        if n == 0:
            return A(m - 1, 1)
        return A(m - 1, A(m, n - 1))

    try:
        m = int(params.get("m", -1))
        n = int(params.get("n", -1))
    except Exception:
        raise InvalidInputValueException("'m and n' should be integer")
    else:
        if m < 0 or n < 0:
            raise InvalidInputValueException(
                "invalid/missing params 'm and n'"
            )
        return A(m, n)


def calculate_factorial(params):
    """
    Calculate the factorial value for the `n` numbers.

    Parameters
    ----------
    params : dict
        containing the input value

    Returns
    -------
    int
        containing a factorial value

    Raises
    ------
    if n is not given, n is negative or n is not integer

        raises an InvalidInputValueException
        
    """
    factorial = 1
    try:
        n = int(params.get("n", -1))
    except Exception:
        raise InvalidInputValueException("'n' should be integer")
    else:
        if n < 0:
            raise InvalidInputValueException("invalid/missing param 'n'")
        if n == 0:
            return 1
        else:
            for i in range(1, n + 1):
                factorial = factorial * i

        return factorial
