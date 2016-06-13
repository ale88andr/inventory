__version__ = '0.2.1 alpha'
__appname__ = 'Инвентаризация'


def appname(request):
    return {'appname': __appname__}


def app_version(request):
    return {'app_version': __version__}
