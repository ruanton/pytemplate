from pyramid.view import view_config
from pyramid.request import Request

# module imports
from zmodels import AppRoot

# local imports
from ..settings import settings


@view_config(context=AppRoot, renderer='myproj:templates/mytemplate.jinja2')
def my_view(request: Request):
    _unused = request
    app_root: AppRoot = request.context

    # for testing pytemplate, remove in real project
    app_root.my_view_counter = getattr(app_root, 'my_view_counter', settings.custom_app_parameter) + 1
    return {'project': 'myproj', 'counter': app_root.my_view_counter}
