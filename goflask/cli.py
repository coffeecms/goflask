"""
GoFlask CLI - Command line interface for Flask compatibility
"""

import os
import sys
import click
from typing import Optional, Dict, Any
from .core import GoFlask


class FlaskGroup(click.Group):
    """A special group for Flask CLI commands"""
    
    def __init__(self, add_default_commands=True, add_version_option=True, **extra):
        params = list(extra.pop('params', None) or ())
        
        if add_version_option:
            from . import __version__
            params.append(click.version_option(__version__, '--version', '-v'))
        
        super().__init__(params=params, **extra)
        
        if add_default_commands:
            self.add_command(run_command)
            self.add_command(shell_command)
            self.add_command(routes_command)
    
    def get_command(self, ctx, name):
        """Get a command by name"""
        info_name = f"{name}_command"
        try:
            return super().get_command(ctx, name)
        except:
            return None
    
    def list_commands(self, ctx):
        """List all available commands"""
        rv = set(super().list_commands(ctx))
        return sorted(rv)


@click.command('run', short_help='Run a development server.')
@click.option('--host', '-h', default='127.0.0.1',
              help='The interface to bind to.')
@click.option('--port', '-p', default=5000,
              help='The port to bind to.')
@click.option('--cert', type=click.Path(exists=True),
              help='Specify a certificate file to use HTTPS.')
@click.option('--key', type=click.Path(exists=True),
              help='The key file to use when specifying a certificate.')
@click.option('--reload/--no-reload', default=None,
              help='Enable or disable the reloader. By default the reloader '
                   'is active if debug is enabled.')
@click.option('--debugger/--no-debugger', default=None,
              help='Enable or disable the debugger. By default the debugger '
                   'is active if debug is enabled.')
@click.option('--eager-loading/--lazy-loader', default=None,
              help='Enable or disable eager loading. By default eager '
                   'loading is enabled if the reloader is disabled.')
@click.option('--with-threads/--without-threads', default=True,
              help='Enable or disable multithreading.')
@click.option('--extra-files', type=click.Path(exists=True), multiple=True,
              help='Extra files that trigger a reload on change. Multiple '
                   'files can be specified.')
def run_command(host, port, reload, debugger, eager_loading, with_threads, 
                cert, key, extra_files):
    """Run a local development server.
    
    This server is for development purposes only. It does not provide
    the stability, security, or performance of production WSGI servers.
    
    The reloader and debugger are enabled by default if FLASK_ENV=development
    or FLASK_DEBUG=1.
    """
    from werkzeug.serving import run_simple
    
    # Get the current app
    app = click.get_current_context().obj
    if app is None:
        click.echo('Error: Could not locate a GoFlask application.')
        sys.exit(1)
    
    debug = app.debug
    
    if reload is None:
        reload = debug
    if debugger is None:
        debugger = debug
    if eager_loading is None:
        eager_loading = not reload
    
    show_server_banner = True
    
    if cert is not None:
        ssl_context = (cert, key)
    else:
        ssl_context = None
    
    click.echo(f' * Running on {"https" if ssl_context else "http"}://{host}:{port}/')
    
    # Run the Go server
    app.run(host=host, port=port, debug=debug)


@click.command('shell', short_help='Run a shell in the app context.')
def shell_command():
    """Run an interactive Python shell in the context of a given GoFlask application."""
    import code
    from flask.globals import _app_ctx_stack
    
    app = click.get_current_context().obj
    if app is None:
        click.echo('Error: Could not locate a GoFlask application.')
        sys.exit(1)
    
    banner = f'Python {sys.version} on {sys.platform}\nGoFlask {app.__class__.__name__} ({app.name})'
    ctx = {}
    
    # Add app to context
    ctx['app'] = app
    
    # Import commonly used modules
    try:
        from .context import g, request, session
        ctx.update(g=g, request=request, session=session)
    except ImportError:
        pass
    
    code.interact(banner=banner, local=ctx)


@click.command('routes', short_help='Show the routes for the app.')
@click.option('--sort', '-s', type=click.Choice(['endpoint', 'methods', 'rule']),
              default='endpoint', help='Method to sort routes by.')
@click.option('--all-methods', is_flag=True, 
              help='Show HEAD and OPTIONS methods.')
def routes_command(sort, all_methods):
    """Show all registered routes with endpoints and methods."""
    app = click.get_current_context().obj
    if app is None:
        click.echo('Error: Could not locate a GoFlask application.')
        sys.exit(1)
    
    rules = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        if not all_methods:
            methods = ','.join([m for m in rule.methods if m not in ('HEAD', 'OPTIONS')])
        
        rules.append({
            'endpoint': rule.endpoint,
            'methods': methods,
            'rule': rule.rule
        })
    
    if sort == 'endpoint':
        rules = sorted(rules, key=lambda x: x['endpoint'])
    elif sort == 'methods':
        rules = sorted(rules, key=lambda x: x['methods'])
    elif sort == 'rule':
        rules = sorted(rules, key=lambda x: x['rule'])
    
    headers = ['Endpoint', 'Methods', 'Rule']
    click.echo(f"{headers[0]:<30} {headers[1]:<15} {headers[2]}")
    click.echo('-' * 70)
    
    for rule in rules:
        click.echo(f"{rule['endpoint']:<30} {rule['methods']:<15} {rule['rule']}")


class AppGroup(FlaskGroup):
    """A group for application-specific commands"""
    
    def __init__(self, app=None, **extra):
        self.app = app
        super().__init__(**extra)


def with_appcontext(f):
    """Wraps a callback so that it's guaranteed to be executed with the
    script's application context.  If callbacks are registered directly
    to the ``app.cli`` object then they are wrapped with this function
    by default unless it's disabled.
    """
    def decorator(*args, **kwargs):
        with click.get_current_context().obj.app_context():
            return f(*args, **kwargs)
    return decorator


def pass_script_info(f):
    """Marks a function so that an instance of :class:`ScriptInfo` is passed
    as first argument to the click callback.
    """
    def new_func(*args, **kwargs):
        return f(ScriptInfo(), *args, **kwargs)
    return new_func


class ScriptInfo:
    """Helper object to deal with GoFlask app loading."""
    
    def __init__(self, app_import_path=None, create_app=None, set_debug_flag=True):
        self.app_import_path = app_import_path or os.environ.get('FLASK_APP')
        self.create_app = create_app
        self.set_debug_flag = set_debug_flag
        self._loaded_app = None
    
    def load_app(self):
        """Load the GoFlask application"""
        if self._loaded_app is not None:
            return self._loaded_app
        
        if self.create_app is not None:
            app = self.create_app()
        else:
            if self.app_import_path:
                path, name = (self.app_import_path.split(':', 1) + [None])[:2]
                import_name = prepare_import(path)
                app = locate_app(import_name, name)
            else:
                for path in ('wsgi.py', 'app.py'):
                    import_name = prepare_import(path)
                    app = locate_app(import_name, None, raise_if_not_found=False)
                    if app:
                        break
        
        if app is None:
            raise RuntimeError('Could not locate a GoFlask application.')
        
        if self.set_debug_flag:
            debug = os.environ.get('FLASK_DEBUG')
            if debug is not None:
                app.debug = debug.lower() not in ('0', 'false', 'no')
        
        self._loaded_app = app
        return app


def prepare_import(path):
    """Prepare import path"""
    path = os.path.realpath(path)
    fname, ext = os.path.splitext(path)
    if ext == '.py':
        path = fname
    
    if os.path.basename(path) == '__init__':
        path = os.path.dirname(path)
    
    module_name = []
    
    # Find package directory
    while True:
        path, name = os.path.split(path)
        module_name.append(name)
        
        if not os.path.isfile(os.path.join(path, '__init__.py')):
            break
    
    if sys.path[0] != path:
        sys.path.insert(0, path)
    
    return '.'.join(module_name[::-1])


def locate_app(module_name, app_name, raise_if_not_found=True):
    """Locate the application object"""
    try:
        __import__(module_name)
    except ImportError:
        if raise_if_not_found:
            raise RuntimeError(f'Could not import "{module_name}".')
        return None
    
    module = sys.modules[module_name]
    
    if app_name is None:
        # Look for common app names
        for attr_name in ('app', 'application', 'create_app'):
            app = getattr(module, attr_name, None)
            if app is not None:
                if isinstance(app, GoFlask):
                    return app
                elif callable(app):
                    try:
                        app = app()
                        if isinstance(app, GoFlask):
                            return app
                    except TypeError:
                        pass
    else:
        app = getattr(module, app_name, None)
        if app is None and raise_if_not_found:
            raise RuntimeError(f'Failed to find attribute "{app_name}" in "{module_name}".')
        
        if callable(app):
            try:
                app = app()
            except TypeError:
                if raise_if_not_found:
                    raise RuntimeError(f'The factory "{app_name}" in module "{module_name}" could not be called.')
                return None
    
    if not isinstance(app, GoFlask) and raise_if_not_found:
        raise RuntimeError(f'A valid GoFlask application was not obtained from "{module_name}:{app_name}".')
    
    return app


def main(as_module=False):
    """Main CLI entry point"""
    this_module = __package__ + '.cli'
    args = sys.argv[1:]
    
    if as_module:
        name = 'python -m ' + this_module.rsplit('.', 1)[0]
    else:
        name = None
    
    FlaskGroup(
        name=name,
        help="""A general utility script for GoFlask applications."""
    )(args)
