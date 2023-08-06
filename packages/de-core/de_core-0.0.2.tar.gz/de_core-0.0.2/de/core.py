""" core portion of the 'de' namespace package """
import glob
import os
import re
from typing import Dict, List, Tuple, Union


__version__ = '0.0.2'       # ALSO CHANGE IN setup.py


EXTEND_NAMESPACE_FILE_NAME = "extend_namespace_env.py"

PORTIONS_COMMON_DIR = 'portions_common_root'

PT_PKG: str = 'sub-package'         #: sub-package portion type
PT_MOD: str = 'module'              #: module portion type
PY_EXT = '.py'

REQ_FILE_NAME = 'requirements.txt'
REQ_TEST_FILE_NAME = 'test_requirements.txt'

TEMPLATE_FILE_NAME_PREFIX = 'de_tpl_'

VERSION_PATCH_PARSER = re.compile(r"(^__version__ = ['\"]\d*[.]\d*[.])(\d+)([a-z]*['\"])", re.MULTILINE)


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
    content, replaced = VERSION_PATCH_PARSER.subn(lambda m: m.group(1) + str(int(m.group(2)) + 1) + m.group(3), content)
    if replaced != 1:
        return msg + f"single occurrence of module variable __version__, but found {replaced} times"
    with open(file_name, 'w') as file_handle:
        file_handle.write(content)
    return ""


def code_file_version(file_name: str) -> str:
    """ read version of Python code file - from __version__ module variable initialization.

    :param file_name:   file name to read the version number from.
    :return:            version number string.
    """
    content = file_content(file_name)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
    if not version_match:
        raise FileNotFoundError(f"Unable to find version string within {file_name}")
    return version_match.group(1)


def file_content(file_name: str) -> str:
    """ returning content of the file specified by file_name arg as string.

    :param file_name:   file name to load into a string.
    :return:            file content string.
    """
    with open(file_name) as file_handle:
        return file_handle.read()


def insert_includes(file_name: str) -> str:
    """ load file content, insert includes and return extended file content.

    :param file_name:   file name to load (mostly a template).
    :return:            file content extended with include snippets found in the same directory.
    """
    content = file_content(file_name)
    beg = 0
    while True:
        beg = content.find("{{{", beg)
        if beg == -1:
            break
        end = content.find("}}}", beg)
        if end == -1:
            break
        include = content[beg + 3: end].split(":::")
        if os.path.exists(include[0]):
            include.append(file_content(include[0]))
        else:
            include.insert(1, "")
        content = content[:beg] + include[-1] + content[end + 3:]

    return content


def namespace_env(namespace_name: str, pkg_root_path: str = "") -> Dict[str, Union[str, List[str]]]:
    """ determines names and file paths of the currently executed/installed namespace development environment.

    :param namespace_name:  root name of this namespace.
    :param pkg_root_path:   optional rel/abs path to package root (def=current working directory).
    :return:                dict with namespace environment variables/info.
    """
    nse: Dict[str, Union[str, List[str]]] = dict()
    nse['namespace_name'] = namespace_name

    if not pkg_root_path:
        pkg_root_path = os.getcwd()
    elif not os.path.isabs(pkg_root_path):
        pkg_root_path = os.path.join(os.getcwd(), pkg_root_path)
    nse['package_root_path'] = pkg_root_path

    if os.path.exists(os.path.join(pkg_root_path, 'setup.py')):     # namespace root or portion
        setup_path = pkg_root_path
    elif os.path.exists(os.path.join(pkg_root_path, 'conf.py')):    # RTD build
        setup_path = os.path.join(pkg_root_path, '..')
    else:
        raise RuntimeError(f"Neither setup.py nor conf.py found in package root {pkg_root_path}")
    nse['setup_path'] = setup_path

    portion_root_path = os.path.join(setup_path, namespace_name)
    portion_type, portion_name = portion_type_name(portion_root_path)
    nse['portion_type'] = portion_type
    nse['portion_name'] = portion_name

    nse['portion_file_name'] = portion_file_name = \
        portion_name + (os.path.sep + '__init__.py' if portion_type == PT_PKG else PY_EXT)
    nse['portion_file_path'] = portion_file_path = \
        os.path.abspath(os.path.join(portion_root_path, portion_file_name))
    nse['package_name'] = f"{namespace_name}_{portion_name}"
    nse['pip_name'] = f"{namespace_name}-{portion_name.replace('_', '-')}"
    nse['import_name'] = f"{namespace_name}.{portion_name}"
    nse['package_version'] = code_file_version(portion_file_path) if portion_type else 'x.y.z'
    nse['root_version'] = 'un.kno.wn' if portion_type else code_file_version(os.path.join(setup_path, 'setup.py'))
    nse['repo_root'] = f"https://gitlab.com/{namespace_name}-group"
    nse['repo_pages'] = f"https://{namespace_name}-group.gitlab.io"
    nse['pypi_root'] = "https://pypi.org/project"

    nse['PORTIONS_COMMON_DIR'] = PORTIONS_COMMON_DIR

    dev_require: List[str] = list()
    requirements_file = os.path.join(setup_path, REQ_FILE_NAME)
    if os.path.exists(requirements_file):
        dev_require.extend(
            _ for _ in file_content(requirements_file).strip().split('\n') if not _.startswith('#'))
    nse['docs_require'] = [_ for _ in dev_require if _.startswith('sphinx_')]
    nse['install_require'] = [_ for _ in dev_require if not _.startswith('sphinx_')]
    nse['setup_require'] = [_ for _ in nse['install_require'] if not _.startswith(f'{namespace_name}_')]  # e.g. de_core
    nse['portions_package_names'] = portions_package_names = [
        _ for _ in dev_require if _.startswith(f'{namespace_name}_')]

    tests_require: List[str] = list()
    requirements_file = os.path.join(setup_path, REQ_TEST_FILE_NAME)
    if os.path.exists(requirements_file):
        tests_require.extend(_ for _ in file_content(requirements_file).strip().split('\n')
                             if not _.startswith('#'))
    nse['tests_require'] = tests_require

    # provide additional package info for root package templates
    nse['portions_pypi_refs_md'] = "\n".join(
        f'* [{_}]({nse["pypi_root"]}/{_} "{namespace_name} namespace portion {_}")'
        for _ in portions_package_names)  # used in root README.md.tpl
    namespace_len = len(namespace_name)
    nse['portions_import_names'] = ("\n" + " " * 4).join(
        _[:namespace_len] + '.' + _[namespace_len + 1:]
        for _ in portions_package_names)  # used in docs/index.rst.tpl

    # finally check if optional extend_namespace_env.py exists and if yes
    file = os.path.join(setup_path, EXTEND_NAMESPACE_FILE_NAME)
    if os.path.exists(file):
        g_v = dict(namespace_env=nse)
        exec(compile(file_content(file), file, 'exec'), g_v)

    return nse


def patch_templates(namespace_env_vars: Dict[str, str], exclude_folder: str = '') -> List[str]:
    """ convert ae namespace package templates found in the cwd or underneath (except excluded) to the final files.

    :param namespace_env_vars:  dict namespace environment variables (determined by namespace_env()).
    :param exclude_folder:      directory name to exclude from templates search.
    :return:                    list of patched template file names.
    """
    patched = list()
    for file_path in glob.glob(f"**/{TEMPLATE_FILE_NAME_PREFIX}*.*", recursive=True):
        if not exclude_folder or not file_path.startswith(exclude_folder + os.path.sep):
            content = insert_includes(file_path)
            content = content.format(**namespace_env_vars)
            path, file = os.path.split(file_path)
            with open(os.path.join(path, file[len(TEMPLATE_FILE_NAME_PREFIX):]), 'w') as file_handle:
                file_handle.write(content)
            patched.append(file_path)
    return patched


def portion_type_name(portion_root_path: str, portion_type: str = PT_MOD, portion_end: str = PY_EXT) -> Tuple[str, str]:
    """ determine portion type and name.

    :param portion_root_path:   file path of the root of the namespace portions.
    :param portion_type:        searched portion type: PT_MOD or PT_PKG.
    :param portion_end:         file name suffix of the portion code file: PY_EXT or os.path.sep.
    :return:                    tuple of portion type and name strings.
    """
    if os.path.exists(portion_root_path):                   # run/imported by portion repository
        search_module = portion_type == PT_MOD
        files = [fn for fn in glob.glob(os.path.join(portion_root_path, '*' + portion_end)) if '__' not in fn]
        if len(files) > 1:
            raise RuntimeError(f"More than one {portion_type} found: {files}")
        if len(files) == 0:
            if not search_module:
                raise RuntimeError(f"Neither module nor sub-package found in package path {portion_root_path}")
            return portion_type_name(portion_root_path, PT_PKG, os.path.sep)
        portion_name = os.path.split(files[0][:-len(portion_end)])[1]
    else:                                                   # imported by namespace root repo
        portion_type = ''
        portion_name = "{portion-name}"

    return portion_type, portion_name
