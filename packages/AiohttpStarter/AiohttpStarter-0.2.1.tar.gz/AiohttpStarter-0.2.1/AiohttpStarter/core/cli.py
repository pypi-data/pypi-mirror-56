import click

from aiohttp import web 
from python_settings import settings

from .application_factory import ApplicationFactory

@click.group()
def cli():
    pass

@cli.command()
@click.option('-h', '--host', default='0.0.0.0', type=str, help='Host')
@click.option('-p', '--port', default=80, type=int, help='Port')
@click.option('-d', '--debug', default=False, type=bool, help='Debud: true or false')
def runserver(host, port, debug):
    """
    Run server.
    """
    # settings.HOST = host
    # settings.PORT = port
    
    application_factory = ApplicationFactory()
    
    web.run_app(application_factory.create(), host=settings.HOST, port=settings.PORT)
