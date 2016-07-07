__version__ = '0.4.3 alpha'
__appname__ = 'Инвентаризация ПФР'


def appname(request):
    return {'appname': __appname__}


def app_version(request):
    return {'app_version': __version__}
