"""Ecommerce desirability dataset

3 classes of images: desirable, average, bad.
"""
import os
import shutil
import tarfile
import time

from keras.utils.data_utils import get_file

_default_label = 'ecommercedesirability3'
_default_target_dir = os.path.join('/tmp', _default_label)

def load_data(target_dir=_default_target_dir):
    """Loads the dataset.
    """
    if os.path.isdir(target_dir):
        print('Deleting {} ...'.format(target_dir))
        shutil.rmtree(target_dir)
    dirname = '/tmp/' + _default_label
    origin = 'https://zooper-datasets.s3.amazonaws.com/' + _default_label + '.tar.gz'

    tarpath = dirname + '.tar.gz'
    if os.path.exists(tarpath):
        os.remove(tarpath)
    st = time.time()
    path = get_file(dirname, origin=origin, untar=True)

    def tar_member(members):
        for tarinfo in members:
            yield tarinfo

    tar = tarfile.open(path + '.tar.gz')
    os.makedirs(target_dir, exist_ok=True)
    tar.extractall('/tmp', members=tar_member(tar))
    tar.close()

    if target_dir != _default_target_dir:
        shutil.move(_default_label, target_dir)
    et = time.time()
    print('`{}` index downloaded to {}. Elapsed time: {} secs'.format(_default_label, target_dir, (et - st)))
