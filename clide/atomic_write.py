# clide:
#   source: https://raw.githubusercontent.com/qix/clide/master/clide/atomic_write.py
#   version: 0.9.0
# License under the MIT License.
# See https://github.com/qix/clide/blob/master/LICENSE for details

import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional, Union


@contextmanager
def atomic_write_context(path: Path, mode: str = "w+b", *, chmod: Optional[int] = None):
    path = Path(path)
    with NamedTemporaryFile(
        mode=mode, prefix=f"{path.name}.tmp.", dir=path.parent, delete=False
    ) as f:
        try:
            yield f
            f.flush()
            os.fsync(f.fileno())
            if chmod is not None:
                os.chmod(f.fileno(), chmod)
            os.rename(f.name, path)
        finally:
            # Make sure we removed the file if something went wrong
            try:
                os.unlink(f.name)
            except FileNotFoundError:
                pass


def atomic_write(
    path: Path, contents: Union[str, bytes], *, chmod: Optional[int] = None
):
    with atomic_write_context(
        path, "w" if isinstance(contents, str) else "wb", chmod=chmod
    ) as f:
        f.write(contents)
