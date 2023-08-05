import logging

logger = logging.getLogger(__name__)


class ApiError(Exception):
    pass


class ErrorHandler:
    def __init__(self, response):
        self.response = response
        self._check_code()

    def _check_code(self):
        sc = self.response.status_code
        try:
            if sc < 300:
                return None
            else:
                raise ApiError
        except ApiError:
            logger.warning(f'---- API Error ----\n'
                           f'Status Code {sc}: {self.response.text}\n'
                           f'URL: {self.response.request.method} {self.response.request.url}\n'
                           f'Data: {self.response.request.body}\n'
                           f'Headers: {self.response.request.headers}\n'
                           f'--------------------')
