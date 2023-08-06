import base64
import collections
import functools
import io
import json
import os
import tarfile
from pathlib import Path

import torch
from PIL import Image
from sqlalchemy.orm import sessionmaker

from .config import Config

featurize_dir = Path() / '.featurize_experiments'

if not os.path.isdir(featurize_dir):
    os.mkdir(featurize_dir)


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname='')


def server_file(file_name, experiment=''):
    if not isinstance(experiment, str):
        experiment = experiment.name

    experiment_dir = Path.home() / '.minetorch_server' / experiment

    try:
        os.makedirs(experiment_dir)
    except FileExistsError:
        pass

    _file = experiment_dir / file_name
    if not os.path.isfile(_file):
        _file.touch()

    return _file.resolve()


def runtime_file(file_name, experiment=''):
    if not isinstance(experiment, str):
        experiment = experiment.name

    experiment_dir = Path.home() / '.minetorch' / experiment
    _file = experiment_dir / file_name

    try:
        os.makedirs(_file.parent)
    except FileExistsError:
        pass

    if not os.path.isfile(_file):
        _file.touch()

    return _file.resolve()


def dict_merge(dct, merge_dct):
    for k, _ in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


def update_json_file(file, object):
    try:
        with open(file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    dict_merge(data, object)
    with open(file, 'w') as f:
        json.dump(data, f)


def read_json_file(file):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def create_session():
    return sessionmaker(bind=Config.engine)()


def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def image_base64(image_path):
    image = Image.open(image_path)
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('ascii')


def get_transform_func(sample):

    def transform(image, permute):
        if not isinstance(image, torch.Tensor):
            image = torch.Tensor(image)
        image = torch.Tensor(image)
        if permute:
            image = image.permute(2, 0, 1)
        return image.unsqueeze(0)

    sample = torch.Tensor(sample)
    should_permute = len(sample.shape) == 3 and sample.shape[2] <= 3
    return functools.partial(transform, permute=should_permute)


__all__ = ['server_file', 'runtime_file', 'dict_merge', 'human_readable_size', 'image_base64']
