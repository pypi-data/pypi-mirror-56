class RecursiveExpansionForbiddenError(RuntimeError):
    """
    An error indicating that resolvref was used to expand a recursive document, but with
    recursive documents disabled (e.g. as in an interactive context)
    """
