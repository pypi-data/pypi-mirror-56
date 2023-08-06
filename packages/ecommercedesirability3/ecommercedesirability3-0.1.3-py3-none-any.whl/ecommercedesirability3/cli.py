import click

from ecommercedesirability3 import index


@click.group()
def cli():
    pass


@cli.command()
@click.option('--output', '-o', help='Output directory to extract the index to.',
              default='/tmp/ecommercedesirability3')
def install(output):
    index.load_data(output)


def main():
    cli()
