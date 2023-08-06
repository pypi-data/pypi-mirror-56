import functools
import sys

import click


class FigitoolException(Exception):
    pass


def cover_figtool_exception(_func=None, *, exit_code=None):
    def decorator_cover(func):
        @functools.wraps(func)
        def covered_func(config=None, *args, **kwargs):
            try:
                if config:
                    func(config=config, *args, **kwargs)
                else:
                    func(*args, **kwargs)
            except KeyboardInterrupt:
                click.echo("Quitting on user request.")
                sys.exit(1)
            except FigitoolException as exc:
                click.echo(str(exc), err=True)
                sys.exit(exit_code or 2)
            except Exception as exc:
                click.echo(str(exc), err=True)
                click.echo(
                    "Unexpected exception occurred,\n"
                    "please fill an issue here:\n"
                    "https://gitlab.fi.muni.cz/xlachma1/figitool/issues",
                    err=True,
                )
                sys.exit(exit_code or 4)

        return covered_func

    if _func is None:
        return decorator_cover
    else:
        return decorator_cover(_func)
