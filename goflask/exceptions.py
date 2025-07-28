"""
GoFlask Exceptions - Exception classes for Flask compatibility
"""

import traceback
from typing import Optional, Dict, Any


class GoFlaskException(Exception):
    """Base exception for GoFlask"""
    pass


class BadRequest(GoFlaskException):
    """400 Bad Request"""
    def __init__(self, description=None):
        self.code = 400
        self.description = description or 'Bad request'
        super().__init__(self.description)


class Unauthorized(GoFlaskException):
    """401 Unauthorized"""
    def __init__(self, description=None):
        self.code = 401
        self.description = description or 'Unauthorized'
        super().__init__(self.description)


class Forbidden(GoFlaskException):
    """403 Forbidden"""
    def __init__(self, description=None):
        self.code = 403
        self.description = description or 'Forbidden'
        super().__init__(self.description)


class NotFound(GoFlaskException):
    """404 Not Found"""
    def __init__(self, description=None):
        self.code = 404
        self.description = description or 'Not found'
        super().__init__(self.description)


class MethodNotAllowed(GoFlaskException):
    """405 Method Not Allowed"""
    def __init__(self, description=None):
        self.code = 405
        self.description = description or 'Method not allowed'
        super().__init__(self.description)


class NotAcceptable(GoFlaskException):
    """406 Not Acceptable"""
    def __init__(self, description=None):
        self.code = 406
        self.description = description or 'Not acceptable'
        super().__init__(self.description)


class RequestTimeout(GoFlaskException):
    """408 Request Timeout"""
    def __init__(self, description=None):
        self.code = 408
        self.description = description or 'Request timeout'
        super().__init__(self.description)


class Conflict(GoFlaskException):
    """409 Conflict"""
    def __init__(self, description=None):
        self.code = 409
        self.description = description or 'Conflict'
        super().__init__(self.description)


class Gone(GoFlaskException):
    """410 Gone"""
    def __init__(self, description=None):
        self.code = 410
        self.description = description or 'Gone'
        super().__init__(self.description)


class LengthRequired(GoFlaskException):
    """411 Length Required"""
    def __init__(self, description=None):
        self.code = 411
        self.description = description or 'Length required'
        super().__init__(self.description)


class PreconditionFailed(GoFlaskException):
    """412 Precondition Failed"""
    def __init__(self, description=None):
        self.code = 412
        self.description = description or 'Precondition failed'
        super().__init__(self.description)


class RequestEntityTooLarge(GoFlaskException):
    """413 Request Entity Too Large"""
    def __init__(self, description=None):
        self.code = 413
        self.description = description or 'Request entity too large'
        super().__init__(self.description)


class RequestURITooLarge(GoFlaskException):
    """414 Request-URI Too Large"""
    def __init__(self, description=None):
        self.code = 414
        self.description = description or 'Request URI too large'
        super().__init__(self.description)


class UnsupportedMediaType(GoFlaskException):
    """415 Unsupported Media Type"""
    def __init__(self, description=None):
        self.code = 415
        self.description = description or 'Unsupported media type'
        super().__init__(self.description)


class RequestedRangeNotSatisfiable(GoFlaskException):
    """416 Requested Range Not Satisfiable"""
    def __init__(self, description=None):
        self.code = 416
        self.description = description or 'Requested range not satisfiable'
        super().__init__(self.description)


class ExpectationFailed(GoFlaskException):
    """417 Expectation Failed"""
    def __init__(self, description=None):
        self.code = 417
        self.description = description or 'Expectation failed'
        super().__init__(self.description)


class ImATeapot(GoFlaskException):
    """418 I'm a teapot"""
    def __init__(self, description=None):
        self.code = 418
        self.description = description or "I'm a teapot"
        super().__init__(self.description)


class UnprocessableEntity(GoFlaskException):
    """422 Unprocessable Entity"""
    def __init__(self, description=None):
        self.code = 422
        self.description = description or 'Unprocessable entity'
        super().__init__(self.description)


class Locked(GoFlaskException):
    """423 Locked"""
    def __init__(self, description=None):
        self.code = 423
        self.description = description or 'Locked'
        super().__init__(self.description)


class FailedDependency(GoFlaskException):
    """424 Failed Dependency"""
    def __init__(self, description=None):
        self.code = 424
        self.description = description or 'Failed dependency'
        super().__init__(self.description)


class PreconditionRequired(GoFlaskException):
    """428 Precondition Required"""
    def __init__(self, description=None):
        self.code = 428
        self.description = description or 'Precondition required'
        super().__init__(self.description)


class TooManyRequests(GoFlaskException):
    """429 Too Many Requests"""
    def __init__(self, description=None):
        self.code = 429
        self.description = description or 'Too many requests'
        super().__init__(self.description)


class RequestHeaderFieldsTooLarge(GoFlaskException):
    """431 Request Header Fields Too Large"""
    def __init__(self, description=None):
        self.code = 431
        self.description = description or 'Request header fields too large'
        super().__init__(self.description)


class UnavailableForLegalReasons(GoFlaskException):
    """451 Unavailable For Legal Reasons"""
    def __init__(self, description=None):
        self.code = 451
        self.description = description or 'Unavailable for legal reasons'
        super().__init__(self.description)


class InternalServerError(GoFlaskException):
    """500 Internal Server Error"""
    def __init__(self, description=None):
        self.code = 500
        self.description = description or 'Internal server error'
        super().__init__(self.description)


class NotImplemented(GoFlaskException):
    """501 Not Implemented"""
    def __init__(self, description=None):
        self.code = 501
        self.description = description or 'Not implemented'
        super().__init__(self.description)


class BadGateway(GoFlaskException):
    """502 Bad Gateway"""
    def __init__(self, description=None):
        self.code = 502
        self.description = description or 'Bad gateway'
        super().__init__(self.description)


class ServiceUnavailable(GoFlaskException):
    """503 Service Unavailable"""
    def __init__(self, description=None):
        self.code = 503
        self.description = description or 'Service unavailable'
        super().__init__(self.description)


class GatewayTimeout(GoFlaskException):
    """504 Gateway Timeout"""
    def __init__(self, description=None):
        self.code = 504
        self.description = description or 'Gateway timeout'
        super().__init__(self.description)


class HTTPVersionNotSupported(GoFlaskException):
    """505 HTTP Version Not Supported"""
    def __init__(self, description=None):
        self.code = 505
        self.description = description or 'HTTP version not supported'
        super().__init__(self.description)


def abort(code: int, description: Optional[str] = None):
    """Raise an HTTP exception with the given status code"""
    exceptions = {
        400: BadRequest,
        401: Unauthorized,
        403: Forbidden,
        404: NotFound,
        405: MethodNotAllowed,
        406: NotAcceptable,
        408: RequestTimeout,
        409: Conflict,
        410: Gone,
        411: LengthRequired,
        412: PreconditionFailed,
        413: RequestEntityTooLarge,
        414: RequestURITooLarge,
        415: UnsupportedMediaType,
        416: RequestedRangeNotSatisfiable,
        417: ExpectationFailed,
        418: ImATeapot,
        422: UnprocessableEntity,
        423: Locked,
        424: FailedDependency,
        428: PreconditionRequired,
        429: TooManyRequests,
        431: RequestHeaderFieldsTooLarge,
        451: UnavailableForLegalReasons,
        500: InternalServerError,
        501: NotImplemented,
        502: BadGateway,
        503: ServiceUnavailable,
        504: GatewayTimeout,
        505: HTTPVersionNotSupported,
    }
    
    exception_class = exceptions.get(code, GoFlaskException)
    raise exception_class(description)


class HTTPException(GoFlaskException):
    """HTTP exception base class for compatibility"""
    
    def __init__(self, description=None, response=None):
        self.code = getattr(self, 'code', 500)
        self.description = description
        self.response = response
        super().__init__(description or 'HTTP Exception')
    
    def get_description(self, environ=None):
        """Get the description"""
        return self.description
    
    def get_body(self, environ=None):
        """Get the response body"""
        return f"{self.code} {self.description}"
    
    def get_headers(self, environ=None):
        """Get response headers"""
        return [('Content-Type', 'text/plain')]
    
    def get_response(self, environ=None):
        """Get response object"""
        return self.response
