import click

from hackernews500kindex import index


@click.group()
def cli():
    pass


@cli.command()
@click.option('--output', '-o', help='Output directory to extract the index to.',
              default='/tmp/hackernews500kindex')
def install(output):
    index.load_data(output)


def main():
    cli()
