import click
import yaml
import subprocess

from .classes import Apperator

@click.group()
def cli():
    pass

@cli.command()
@click.option('-f', default='-', help='apperator manifest')
def build(f):
    if f == '-':
        f = click.get_text_stream('stdin')
        crd = yaml.safe_load(f.read())
    else:
        with open(f, 'r') as f:
            crd = yaml.safe_load(f.read())

    App = Apperator(crd)

    print(App.template().replace('\n\n', '\n').replace('\n\n', '\n'))

@cli.command()
@click.option('-f', default='-', help='apperator manifest')
def apply(f):
    if f == '-':
        f = click.get_text_stream('stdin')
        crd = yaml.safe_load(f.read())
    else:
        with open(f, 'r') as f:
            crd = yaml.safe_load(f.read())

    App = Apperator(crd)
    t = App.template().replace('\n\n', '\n').replace('\n\n', '\n')
    out = subprocess.check_output(
        ['kubectl', 'apply', '-f', '-'],
        input=t.encode(),
    )
    print(out.decode('utf-8'))

@cli.command()
@click.option('-f', default='-', help='apperator manifest')
def delete(f):
    if f == '-':
        f = click.get_text_stream('stdin')
        crd = yaml.safe_load(f.read())
    else:
        with open(f, 'r') as f:
            crd = yaml.safe_load(f.read())

    App = Apperator(crd)
    t = App.template().replace('\n\n', '\n').replace('\n\n', '\n')
    out = subprocess.check_output(
        ['kubectl', 'delete', '-f', '-'],
        input=t.encode(),
    )
    print(out.decode('utf-8'))

@click.group()
def cli():
    pass

cli.add_command(build)
cli.add_command(apply)
cli.add_command(delete)
