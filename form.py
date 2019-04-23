#!/usr/bin/env python3

from pathlib import Path

import click
from jinja2 import Environment, FileSystemLoader


@click.command()
@click.argument('template', type=click.Path(dir_okay=False, resolve_path=True))
@click.option('--output', type=click.Path(dir_okay=False, resolve_path=True))
def form(template, output):
    """Render the membership form template.

    A template "foo.j2" will be rendered to "foo.html", unless the --output
    parameter is used.
    """
    template_path = Path(template)
    base_path = template_path.parent
    if output is None:
        output_path = base_path.joinpath(template_path.stem + '.html')
    else:
        output_path = Path(output)

    env = Environment(loader=FileSystemLoader(str(base_path)))
    template = env.get_template(template_path.name)
    template.stream().dump(str(output_path), encoding='utf-8')


if __name__ == '__main__':
    form()
