import click

@click.group()
def in_downloader():
    pass


@click.command()
def initdb():
    click.echo('Initialized the database')
    import requests
    r = requests.get('')
    r.text
    r.headers


@click.command()
def dropdb():
    click.echo('Dropped the database')
