from string import Template
from contextlib import contextmanager

import tempfile
import os


@contextmanager
def instance_template(path, *args, **kwargs):
    handle, tmp_path = tempfile.mkstemp()
    try:
        with open(path) as rfp, open(tmp_path, "w") as tfp:
            tpl = rfp.read()
            res = Template(tpl).substitute(*args, **kwargs)
            tfp.write(res)
        yield tmp_path
    finally:
        os.unlink(tmp_path)


