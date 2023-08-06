# -*- coding: utf-8 -*-

"""Console script for git_code_counter."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for git_code_counter."""
    click.echo("Replace this message by putting your code into "
               "git_code_counter.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
