from bottle import request
from elasticapm.utils import compat, get_url_dict
from elasticapm.utils.disttracing import TraceParent

from bottle_elastic_apm.constants import HEADER_TRACER_PARENT


def get_data_from_request(server_request, capture_body=False,
                          capture_headers=True):
    data = {
        "method": server_request.method,
        "socket": {
            "remote_address": server_request.remote_addr,
            "encrypted": 'https' == server_request.urlparts[0]
        },
        "cookies": dict(**server_request.cookies),
        "url": get_url_dict(server_request.url)
    }
    # TODO: tratar multipart/form-data
    if capture_body and server_request.json:
        data["body"] = server_request.json
    if capture_headers:
        data["headers"] = dict(**server_request.headers)
        data["headers"].pop("Cookie", None)
    return data


def get_data_from_response(server_response, capture_headers=True):
    data = {"status_code": server_response.status_code}
    if capture_headers and server_response.headers:
        data["headers"] = {
            key: ";".join(server_response.headers.getall(key))
            for key in compat.iterkeys(server_response.headers)
        }
    return data


def trace_parent():
    trace_parent_header = request.headers.get(HEADER_TRACER_PARENT)
    if not trace_parent_header:
        return None
    return TraceParent.from_string(trace_parent_header)
