# clide:
#   source: https://raw.githubusercontent.com/qix/clide/master/clide/date.py
#   version: 0.9.0
# License under the MIT License.
# See https://github.com/qix/clide/blob/master/LICENSE for details

from datetime import datetime, timezone

def utc_now():
    return datetime.utcnow().replace(tzinfo=timezone.utc)

__all__ = ["utc_now"]
