from importlib import import_module
from collections.abc import Iterable

from marshmallow import ValidationError, Schema
from python_settings import settings
from aiohttp import web

from .installs_exceptions import *
from AiohttpStarter.exceptions import ServerException


# TYPE_CHECKING:
from types import ModuleType
from typing import (
    Callable, Tuple, List,
    Optional, Mapping, NoReturn
)

from aiohttp.web import Application


def module_and_object_by_path(path: str) -> Tuple[str, str]:
    *module_path_list, object_path = path.split('.')
    module_path: str = '.'
    if  module_path_list:
        module_path = '.'.join(module_path_list)
    return (module_path, object_path)


def install_applications(app: Application) -> None:
    if hasattr(settings, "APPLICATIONS") and isinstance(settings.APPLICATIONS, Iterable):
        for url, application in settings.APPLICATIONS:
            try:
                module_path, object_path = module_and_object_by_path(application)
                application_module = import_module(module_path)
                app.add_subapp(url, getattr(application_module, object_path))
            except ModuleNotFoundError:
                raise InstallApplicationError(f"Application {application} not found.")
            
            
def install_startups(app: Application) -> None:
    if hasattr(settings, "STARTUPS") and isinstance(settings.STARTUPS, Iterable):
        for startup in settings.STARTUPS:
            try:
                module_path, object_path = module_and_object_by_path(startup)
                startup_module = import_module(module_path)
                app.on_startup.append(getattr(startup_module, object_path))
            except ModuleNotFoundError:
                raise InstallStartupError(f"Startup {startup} not found.")


def install_cleanups(app: Application) -> None:
    if hasattr(settings, "CLEANUPS") and isinstance(settings.CLEANUPS, Iterable):
        for cleanup in settings.CLEANUPS:
            try:
                module_path, object_path = module_and_object_by_path(cleanup)
                cleanup_module = import_module(module_path)
                app.on_cleanup.append(getattr(cleanup_module, object_path))
            except ModuleNotFoundError:
                raise InstallCleanupError(f"Cleanup {cleanup} not found.")


def install_middlewares() -> List[Callable]:
    middleware_modules: List[Callable] = list()
    if hasattr(settings, "MIDDLEWARES") and isinstance(settings.MIDDLEWARES, Iterable):
        for middleware in settings.MIDDLEWARES:
            try:
                module_path, object_path = module_and_object_by_path(middleware)
                middleware_module = import_module(module_path)
                middleware_modules.append(getattr(middleware_module, object_path))
            except ModuleNotFoundError:
                raise InstallMiddlewareError(f"Middleware {middleware} not found.")
    return middleware_modules


def error_handler(
    error: ValidationError,
    req: web.Request,
    schema: Schema,
    error_status_code: Optional[int] = None,
    error_headers: Optional[Mapping[str, str]] = None,
) -> NoReturn:
    raise ServerException(
        1,
        "Ошибка валидации",
        f"Error in schema {schema} validation",
        details=error.messages,
    )

class ApplicationFactory(object):
    def __init__(self) -> None:
        self.__creators: List[Callable] = list()
        self.__creators.append(install_applications)
        self.__creators.append(install_startups)
        self.__creators.append(install_cleanups)
    
    def add_creator(self, creator: Callable[[Application], None]) -> None:
        self.__creators.append(creator)
    
    def create(self) -> Application:
        app = web.Application(middlewares=install_middlewares())
        
        if hasattr(settings, "SWAGGER"):
            from aiohttp_apispec import setup_aiohttp_apispec

            setup_aiohttp_apispec(
                app=app,
                **settings.SWAGGER,
                error_callback=error_handler
            )
        
        for creator in self.__creators:
            creator(app)
        
        return app