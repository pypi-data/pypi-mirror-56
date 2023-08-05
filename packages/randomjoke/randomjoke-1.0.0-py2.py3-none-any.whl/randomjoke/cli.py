# -*- coding: utf-8 -*-

"""Console script for randomjoke."""
import sys

import click

from randomjoke.randomjoke import get_a_random_joke


@click.command()
def main(args=None):
    """Console script for randomjoke."""
    click.echo()
    click.echo(get_a_random_joke())
    click.echo()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
