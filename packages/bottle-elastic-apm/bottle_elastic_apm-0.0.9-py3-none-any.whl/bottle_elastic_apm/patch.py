from logging import INFO

from elasticapm.utils import wrapt

from bottle_elastic_apm.tracer import ELKApmPlugin


def patch_all():
    wrapt.wrap_function_wrapper('bottle', 'Bottle.__init__', traced_init)


def traced_init(wrapper, instance, args, kwargs):
    wrapper(*args, **kwargs)

    plugin = ELKApmPlugin(logging=INFO)
    instance.install(plugin)
