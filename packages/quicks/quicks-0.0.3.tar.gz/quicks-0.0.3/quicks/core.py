import os
import yaml

from jinja2 import Environment, BaseLoader

from quicks.exceptions import PathExistsError

__version__ = '0.0.3'
VERSION = __version__


def get_env():
    return Environment(loader=BaseLoader)


def process_project(env, path, project, template):
    project_path = os.path.join(path, project)
    if os.path.exists(project_path):
        raise PathExistsError

    os.makedirs(project_path)
    project_files, templates, *_ = template
    for file in project_files:
        kwargs = dict(project=project)
        file_template = env.from_string(templates.get(file, '')).render(**kwargs)
        file_path = os.path.join(project_path, env.from_string(file).render(**kwargs))
        file_dir = os.path.dirname(file_path)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_template)


def parse_template(path):
    with open(path, encoding='utf-8') as f:
        data = yaml.load(f, yaml.FullLoader)

    return data.get('files', []), data.get('templates', {})
