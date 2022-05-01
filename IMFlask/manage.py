"""
Application Main Manage Module
"""
import unittest
import click
from config import config, APP_NAME
from app import create_flask_app
import model

application = create_flask_app(config)

@application.shell_context_processor
def make_shell_context():
    """Init shell context."""
    return dict(app_name=APP_NAME)


@application.cli.command()
def db_init():
    """First, run the Database init controller."""
    model.init_app(config)


@application.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
