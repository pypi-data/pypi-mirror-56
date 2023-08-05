"""
Module used by c2cwsgiutils_run.sh to provide a WSGI application when starting gunicorn
"""
from typing import Callable, Any

from c2cwsgiutils import coverage_setup  # pragma: no cover

coverage_setup.init()  # pragma: no cover


def create() -> Callable[[Any, Any], Any]:  # pragma: no cover
    # first import and initialize the wsgi application in order to have the logs setup before importing
    # anything else
    from c2cwsgiutils import wsgi
    main_app = wsgi.create_application()

    # then, we can setup a few filters
    from c2cwsgiutils import sentry, profiler, client_info
    return sentry.filter_wsgi_app(profiler.filter_wsgi_app(client_info.Filter(main_app)))


application = create()  # pragma: no cover
