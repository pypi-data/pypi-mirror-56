"""
File: plugin_module.py
Description: pytest plugin module file
"""
from pytest import fixture


@fixture(scope='module')
def hello(request):
    name = request.config.getoption('--hello')
    print(f'Hello {name if name else "world"}')


def pytest_addoption(parser):
    # group = parser.getgroup('pytest_easy_api')
    parser.addoption('--hello', action='store',
                     default=None, help='Just print hello')