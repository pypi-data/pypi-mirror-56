import bottle
import elasticapm
from bottle import request, response
from elasticapm import setup_logging
from elasticapm.handlers.logging import LoggingHandler
from elasticapm.utils import get_url_dict, compat
from elasticapm.utils.disttracing import TraceParent


class ELKApmPLugin(object):
    name = 'elastic_apm'
    api = 2

    def __init__(self, config=None, logging=False):
        self.logging = logging
        self.client = elasticapm.Client(
            framework_name=bottle.__name__,
            framework_version=bottle.__version__,
            config=config
        )

    def setup(self, _app):
        if self.logging or self.logging is 0:
            if self.logging is not True:
                kwargs = {"level": self.logging}
            else:
                kwargs = {}
            setup_logging(LoggingHandler(self.client, **kwargs))

    def apply(self, callback, _context):
        def wrapper(*args, **kwargs):
            self.client.begin_transaction('request',
                                          trace_parent=self.trace_parent())
            try:
                res = callback(*args, **kwargs)
                self.set_response_information()
                return res
            except Exception as error:
                self.set_request_information()
                self.client.capture_exception(context={
                    "request": self.get_data_from_request(request)
                }, handled=False)
                return error
            finally:
                transaction_name = self.set_request_information()
                transaction_result = self.set_response_information()
                self.client.end_transaction(transaction_name,
                                            transaction_result)

        return wrapper

    def set_request_information(self):
        submodule = request.script_name or ''
        transaction_name = f"{request.method} {submodule[:-1]}{request.route.rule}"
        elasticapm.set_context(
            lambda: self.get_data_from_request(request),
            "request")
        return transaction_name

    def set_response_information(self):
        transaction_result = str(response.status_code)[0] + 'xx'
        elasticapm.set_context(
            lambda: self.get_data_from_response(response),
            "response")
        return transaction_result

    @staticmethod
    def get_data_from_request(server_request):
        data = {
            "headers": dict(**server_request.headers),
            "method": server_request.method,
            "socket": {
                "remote_address": server_request.remote_addr,
                "encrypted": request.url.split('//')[0].replace(':',
                                                                '') == 'https'
            },
            "cookies": dict(**server_request.cookies),
            "url": get_url_dict(server_request.url)
        }
        data["headers"].pop("Cookie", None)
        return data

    @staticmethod
    def get_data_from_response(server_response):
        data = {"status_code": server_response.status_code}
        if server_response.headers:
            data["headers"] = {
                key: ";".join(server_response.headers.getall(key))
                for key in compat.iterkeys(server_response.headers)
            }
        return data

    @staticmethod
    def trace_parent():
        trace_parent = request.headers.get('Elastic-Apm-Traceparent')
        if not trace_parent:
            return None
        return TraceParent.from_string(trace_parent)
