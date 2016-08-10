__version__ = '0.5.2 beta'
__appname__ = 'Инвентаризация'


def app_name(request):
    return {'app_name': __appname__}


def app_version(request):
    return {'app_version': __version__}
