from rest_framework.views import exception_handler

def core_exception_handler(exc, context):
    response = exception_handler(exc, context)
    handlers = {
        'ValidationError': _handle__generic_error
    }

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class(exc, context, response)]
    return response

def _handle__generic_error(exc, context, response):
    resopnse.data = {
        'errors': response.data
    }
    return response


