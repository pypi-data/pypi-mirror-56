"""Ecommerce desirability dataset

3 classes of images: desirable, average, bad.
"""
import os
import shutil
import tarfile
import time

from keras.utils.data_utils import get_file

_default_label = 'ecommercedesirability3'

def load_data(target_dir=_default_label):
    """Loads the index.
    """
    dirname = '/tmp/' + _default_label
    origin = 'https://zooper-datasets.s3-us-west-2.amazonaws.com/' + _default_label + '.tar.gz'

    st = time.time()
    path = get_file(dirname, origin=origin, untar=True)

    def tar_member(members):
        for tarinfo in members:
            yield tarinfo

    tar = tarfile.open(path + '.tar.gz')
    tar.extractall(members=tar_member(tar))
    tar.close()

    if os.path.isdir(target_dir):
        print('Deleting {} ...'.format(target_dir))
        shutil.rmtree(target_dir)
    if target_dir != _default_label:
        shutil.move(_default_label, target_dir)
    et = time.time()
    print('`{}` index downloaded to {}. Elapsed time: {} secs'.format(_default_label, target_dir, (et - st)))
