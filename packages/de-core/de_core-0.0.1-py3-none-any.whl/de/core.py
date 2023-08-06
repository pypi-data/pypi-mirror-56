""" core portion of the 'de' namespace package """
import glob
import os
import re
from typing import Dict, List


__version__ = '0.0.1'


PT_PKG: str = 'sub-package'         #: sub-package portion type
PT_MOD: str = 'module'              #: module portion type
PY_EXT = '.py'

REQ_FILE_NAME = 'requirements.txt'
REQ_TEST_FILE_NAME = 'test_requirements.txt'

template_extension = '.tpl'

version_patch_parser = re.compile(r"(^__version__ = ['\"]\d*[.]\d*[.])(\d+)([a-z]*['\"])", re.MULTILINE)


def bump_code_file_patch_number(file_name: str) -> str:
    """ read code file version and then increment the patch number by one and write the code file back.

    :param file_name:   code file name to be patched.
    :return:            empty string on success, else error string.
    """
    msg = f"bump_code_file_patch_number({file_name}) expects "
    if not os.path.exists(file_name):
        return msg + f"existing code file in folder {os.getcwd()}"
    content = file_content(file_name)
    if not content:
        return msg + f"non-empty code file in {os.getcwd()}"
    content, replaced = version_patch_parser.subn(lambda m: m.group(1) + str(int(m.group(2)) + 1) + m.group(3), content)
    if replaced != 1:
        return msg + f"single occurrence of module variable __version__, but found {replaced} times"
    with open(file_name, 'w') as fp:
        fp.write(content)
    return ""


def code_file_version(file_name: str) -> str:
    """ read version of Python code file - from __version__ module variable initialization. """
    content = file_content(file_name)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
    if not version_match:
        raise FileNotFoundError(f"Unable to find version string within {file_name}")
    return version_match.group(1)


def determine_package_vars(namespace_name: str, portion_root_path: str,
                           portion_type: str = PT_MOD, portion_end: str = PY_EXT
                           ) -> Dict[str, str]:
    """ determine vars of a ae namespace package portion (and if it is either a module or a sub-package).

    :param namespace_name:      namespace name/id string.
    :param portion_root_path:   file path of the root of the namespace portions.
    :param portion_type:        searched portion type: PT_MOD or PT_PKG.
    :param portion_end:         file name suffix of the portion code file: PY_EXT or os.path.sep.
    :return:                    dict with package variables.
    """
    if os.path.exists(portion_root_path):                   # run/imported by portion repository
        search_module = portion_type == PT_MOD
        files = [fn for fn in glob.glob(os.path.join(portion_root_path, '*' + portion_end)) if '__' not in fn]
        if len(files) > 1:
            raise RuntimeError(f"More than one {portion_type} found: {files}")
        if len(files) == 0:
            if not search_module:
                raise RuntimeError(f"Neither module nor sub-package found in package path {portion_root_path}")
            return determine_package_vars(portion_root_path, PT_PKG, os.path.sep)
        portion_name = os.path.split(files[0][:-len(portion_end)])[1]
    else:                                                   # imported by namespace root repo
        portion_type = ''
        portion_name = "{portion-name}"

    p_vars = dict()
    p_vars['namespace_name'] = namespace_name
    p_vars['portion_type'] = portion_type
    p_vars['portion_name'] = portion_name
    p_vars['portion_file_name'] = portion_name + (os.path.sep + '__init__.py' if portion_type == PT_PKG else PY_EXT)
    p_vars['portion_file_path'] = os.path.abspath(os.path.join(portion_root_path, p_vars['portion_file_name']))
    p_vars['package_name'] = f"{namespace_name}_{portion_name}"
    p_vars['pip_name'] = f"{namespace_name}-{portion_name.replace('_', '-')}"
    p_vars['import_name'] = f"{namespace_name}.{portion_name}"
    p_vars['package_version'] = code_file_version(p_vars['portion_file_path']) if portion_type else 'x.y.z'
    setup_path = determine_setup_path()
    p_vars['root_version'] = 'un.kno.wn' if portion_type else code_file_version(os.path.join(setup_path, 'setup.py'))
    p_vars['repo_root'] = f"https://gitlab.com/{namespace_name}-group"
    p_vars['repo_pages'] = f"https://{namespace_name}-group.gitlab.io"
    p_vars['pypi_root'] = "https://pypi.org/project"

    return p_vars


def determine_setup_path() -> str:
    """ check if setup.py got called from portion root or from docs/RTD root. """
    cwd = os.getcwd()
    if os.path.exists('setup.py'):      # local build
        return cwd
    if os.path.exists('conf.py'):       # RTD build
        return os.path.abspath('..')
    raise RuntimeError(f"Neither setup.py nor conf.py found in current working directory {cwd}")


def file_content(file_name: str) -> str:
    """ returning content of the file specified by file_name arg as string. """
    with open(file_name) as fp:
        return fp.read()


def patch_templates(patch_vars: Dict[str, str], exclude_folder: str = '') -> List[str]:
    """ convert ae namespace package templates found in the cwd or underneath (except excluded) to the final files. """
    patched = list()
    for fn in glob.glob('**/*.*' + template_extension, recursive=True):
        if not exclude_folder or not fn.startswith(exclude_folder + os.path.sep):
            content = file_content(fn).format(**patch_vars)
            with open(fn[:-len(template_extension)], 'w') as fp:
                fp.write(content)
            patched.append(fn)
    return patched
