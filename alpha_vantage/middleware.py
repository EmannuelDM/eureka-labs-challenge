import logging
logging.basicConfig(filename="log.txt", level=logging.DEBUG)

import time


class LogRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)
        end = time.perf_counter()
        self.log(request, start, end)
        return response

    def log(self, request, start, end):
        logging.info(f"{request.method} - {request.path_info} | {start} - {end}")

