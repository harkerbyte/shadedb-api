"""
shade_exceptions.py
Custom exceptions for the ShadeDB API Client architecture.
"""

class ShadeDBError(Exception):
    """Base exception for all ShadeDB specific errors."""
    pass


class URLEndpointMissingError(ShadeDBError):
    """Exception raised when the URL endpoint is missing."""
    def __init__(self, source: str):
        super().__init__(f"[{source}] Missing database endpoint URL.")


class ConnectionTokenMissingError(ShadeDBError):
    """Exception raised when the main connection token is missing."""
    def __init__(self, source: str):
        super().__init__(f"[{source}] Missing connection token.")


class ClusterTokenMissingError(ShadeDBError):
    """Exception raised when the cluster/instance token is missing."""
    def __init__(self, source: str):
        super().__init__(f"[{source}] Missing cluster token.")


class SNLMissingError(ShadeDBError):
    """Exception raised when an SNL command is missing."""
    def __init__(self, source: str):
        super().__init__(f"[{source}] Command payload is missing.")
  

class SNLContextMissingError(ShadeDBError):
    """Exception raised when the required dictionary context is missing."""
    def __init__(self, source: str):
        super().__init__(f"[{source}] Missing context dictionary.")


if __name__ == "__main__":
    # Quick sanity check/demonstration
    try:
        raise SNLMissingError("ConsoleAPI")
    except ShadeDBError as e:
        print(f"Caught expected exception: {e}")
