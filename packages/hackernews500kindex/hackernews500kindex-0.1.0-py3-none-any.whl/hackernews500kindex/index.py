import os
import shutil
import tarfile
import time

from keras.utils.data_utils import get_file

_default_label = 'hackernews500kindex'
_default_target_dir = '/tmp/' + _default_label

def load_data():
    """Loads the index.
    Returns: hn500kindex.fvec hn500kindex.caption hackernews.caption
    """
    if os.path.isdir(_default_target_dir):
        print('Deleting {} ...'.format(_default_target_dir))
        shutil.rmtree(_default_target_dir)
    dirname = '/tmp/' + _default_label
    origin = 'https://zooper-index.s3-us-west-2.amazonaws.com/hackernews500kindex.tar.gz'

    tarpath = _default_target_dir + '.tar.gz'
    if os.path.exists(tarpath):
        print('Deleting {}'.format(tarpath))
        os.remove(tarpath)

    st = time.time()
    path = get_file(dirname, origin=origin, untar=True)

    def tar_member(members):
        for tarinfo in members:
            yield tarinfo

    tar = tarfile.open(path + '.tar.gz')
    tar.extractall('/tmp', members=tar_member(tar))
    tar.close()
    et = time.time()
    print('`{}` index downloaded to {}. Elapsed time: {} secs'.format(target_dir, (et - st)))
