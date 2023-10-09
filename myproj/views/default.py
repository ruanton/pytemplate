from pyramid.view import view_config

# local imports
from ..models import AppRoot


@view_config(context=AppRoot, renderer='myproj:templates/mytemplate.jinja2')
def my_view(request):
    _unused = request
    return {'project': 'myproj'}
