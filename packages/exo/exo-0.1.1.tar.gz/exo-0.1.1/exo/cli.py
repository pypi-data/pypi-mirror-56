# -*- coding: utf-8 -*-

"""Console script for exo."""
import sys
import click
from exo import __author__
from exo import __version__
from pyfiglet import Figlet

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(options_metavar='<options>', context_settings=CONTEXT_SETTINGS)
@click.option('-v','--version', is_flag=True, help="print current version")
def main(version):
    """
    exo is a collection of command-line utilities for Yeast Epigenome Project

    List of available utilities:

    \b
        calculate-threshold : calculates & reports a contrast threshold from tagPileUP CDT for generating heatmaps.
        make-heatmap        : generates a heatmap from a tagPileUP CDT tabular file.
        make-composite      : generates a composite from a tagPileUP CDT tabular file.

    For help with each utility, use -help (ex: make-heatmap -help)
    """
    if version:
        click.echo(__version__)
    else:
        f = Figlet(font='larry3d')
        click.echo(f.renderText('yeast epigenome project !'))
        click.echo("Author: "+ __author__+ "\nVersion: "+__version__)
        click.echo("Usage: exo --help \n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
