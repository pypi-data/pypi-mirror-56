# Copyright 2018 Blink Health LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

try:  # pragma: no cover
    # YAY PYTHON!
    # noinspection PyPackageRequirements
    from collections.abc import Mapping, Hashable
except ImportError:  # pragma: no cover
    try:
        # noinspection PyPackageRequirements
        from collections import Mapping, Hashable
    except ImportError:
        # noinspection PyPackageRequirements
        from future.moves.collections import Mapping, Hashable
import warnings


def merge_dicts(src, dest, parent=[]):
    for key in dest:
        full_path = parent + [key]
        if key in src:
            if isinstance(src[key], Mapping) and isinstance(dest[key], Mapping):
                if src[key].get("encrypted", False):
                    msg = (
                        "Overriding an encrypted value at <{}>. This can lead to trouble, since these "
                        "values were likely encrypted with different keys!"
                    )
                    warnings.warn(msg.format(".".join(full_path)), DeprecationWarning)
                src[key] = merge_dicts(src[key], dest[key], parent=full_path)
            elif src[key] == dest[key]:
                pass  # same leaf value
            else:
                src[key] = dest[key]
        else:
            # don't let overrides create keys
            msg = (
                "Trying to override a value on a non-existing default! "
                "The value at path <{}> will be ignored".format(".".join(full_path))
            )
            warnings.warn(msg, DeprecationWarning)
            pass
    return src
