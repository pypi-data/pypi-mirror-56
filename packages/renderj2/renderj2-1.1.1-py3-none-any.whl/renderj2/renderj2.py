#!/usr/bin/env python3

import click
import yaml
from jinja2 import Environment, FileSystemLoader


@click.command()
@click.option('-v', '--varsfile', type=click.File('r'), multiple=True,
              help='vars file path for jinja2')
@click.argument('template', type=click.Path(exists=True))
def cmd(template, varsfile):
    env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
    _template = env.get_template(template)

    vars = {}
    for file in varsfile:
        vars.update(yaml.safe_load(file))

    print(_template.render(vars))


def main():
    cmd()


if __name__ == '__main__':
    main()
