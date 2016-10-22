from string import Template
from contextlib import contextmanager

import tempfile
import os


@contextmanager
def instance_template(path, *args, **kwargs):
    """
    Load a Template (variable like bash) string and replace with args

    :param path: path of template
    :param args: variables
    :param kwargs: variables
    :return:
    """
    handle, tmp_path = tempfile.mkstemp()
    try:
        with open(path) as rfp, open(tmp_path, "w") as tfp:
            tpl = rfp.read()
            res = Template(tpl).substitute(*args, **kwargs)
            tfp.write(res)
        yield tmp_path
    finally:
        os.unlink(tmp_path)

