def AuthError(Exception):
    pass


'''class APIKeyError(AuthError):  # Assuming AuthError is your base exception
    """Raised when an operation on an API key fails."""
    def __init__(self, message="Could not store API key", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
        
        to be added later'''