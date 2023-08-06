# The MIT License
#
# Copyright (c) 2019 imuxin https://github.com/imuxin.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Single point of entry to generate the sample configuration file.

This module collects all the necessary info from the other modules in this
package. It is assumed that:

* Every other module in this package has a 'list_opts' function which
  returns a dict where:

  * The keys are strings which are the group names.

  * The value of each key is a list of config options for that group.

* The conf package doesn't have further packages with config options.

* This module is only used in the context of sample file generation.

"""

import collections
import importlib
import os
import pkgutil


LIST_OPTS_FUNC_NAME = 'list_opts'
IGNORED_MODULES = ('opts', 'constants', 'utils')


def list_opts():
    opts = collections.defaultdict(list)
    module_names = _list_module_names()
    imported_modules = _import_modules(module_names)
    _append_config_options(imported_modules, opts)
    return _tupleize(opts)


def _tupleize(d):
    """Convert a dict of options to the 2-tuple format."""
    return [(key, value) for key, value in d.items()]


def _list_module_names():
    module_names = []
    package_path = os.path.dirname(os.path.abspath(__file__))
    for _, module_name, ispkg in pkgutil.iter_modules(path=[package_path]):
        if module_name in IGNORED_MODULES or ispkg:
            # Skip this module.
            continue
        else:
            module_names.append(module_name)
    return module_names


def _import_modules(module_names):
    imported_modules = []
    for module_name in module_names:
        full_module_path = '.'.join(__name__.split('.')[:-1] + [module_name])
        module = importlib.import_module(full_module_path)
        if not hasattr(module, LIST_OPTS_FUNC_NAME):
            raise Exception(
                "The module '%s' should have a '%s' function which "
                "returns the config options." % (
                    full_module_path,
                    LIST_OPTS_FUNC_NAME))
        else:
            imported_modules.append(module)
    return imported_modules


def _append_config_options(imported_modules, config_options):
    for module in imported_modules:
        configs = module.list_opts()
        for key, val in configs.items():
            config_options[key].extend(val)
