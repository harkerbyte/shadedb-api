class URLEndpointMissingError(Exception):
    """Exception raised when the URL endpoint is missing."""
    def __init__(self, source):
        self.message = f"{source} missing endpoint url"
        super().__init__(self.message)

class TokenMissingError(Exception):
    """Exception raised when the auth token is missing."""
    def __init__(self, source):
        self.message = f"{source} missing token"
        super().__init__(self.message)

class SNLMissingError(Exception):
    """Exception raised when command is missing."""
    def __init__(self, source):
      self.message = f"command missing : {source}"
      super().__init__(self.message)
  
class SNLContextMissingError(Exception):
  """Exception raised when dict context is missing."""
  def __init__(self, source):
    self.message = f"missing dictionary context : {source}"
    super().__init__(self.message)

if __name__ == "__main__":
  pass