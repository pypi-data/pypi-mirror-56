""" core portion of the 'de' namespace package """
import glob
import os
import re
from typing import Callable, Dict, List, Optional, Tuple, Union


__version__ = '0.0.5'       # ALSO CHANGE IN setup.py


NevVarType = Union[str, List[str]]
NevType = Dict[str, NevVarType]


EXTEND_NAMESPACE_FILE_NAME = "extend_namespace_env.py"  #: default hook file name for namespace env values update/change

PORTIONS_COMMON_DIR = 'portions_common_root'            #: default folder in root package for portions common files

_PT_PKG: str = 'sub-package'                            #: sub-package portion type
_PT_MOD: str = 'module'                                 #: module portion type

PY_EXT = '.py'                                          #: default file extension for portions and hooks

REQ_FILE_NAME = 'requirements.txt'                      #: default file name for all/dev requirements
REQ_TEST_FILE_NAME = 'test_requirements.txt'            #: default file name for test requirements

TEMPLATE_FILE_NAME_PREFIX = 'de_tpl_'                   #: template file name prefix
TEMPLATE_PLACEHOLDER_ID_PREFIX = "# "                   #: template id prefix marker
TEMPLATE_PLACEHOLDER_ID_SUFFIX = "#("                   #: template id suffix marker
TEMPLATE_PLACEHOLDER_ARGS_SUFFIX = ")#"                 #: template args suffix marker
TEMPLATE_INCLUDE_FILE_PLACEHOLDER_ID = "IncludeFile"    #: placeholder id (func:`replace_with_file_content_or_default`)

VERSION_PATCH_PARSER = re.compile(r"(^__version__ = ['\"]\d*[.]\d*[.])(\d+)([a-z]*['\"])", re.MULTILINE)
""" pre-compiled regular expression for to detect and bump the patch number of version string """


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


def load_requirements(namespace_name: str, nev: NevType, path: str) -> List[str]:
    """ load requirements from *requirements.txt and return list of portions package names.

    :param namespace_name:  name space name/id.
    :param nev:             dict of namespace environment variables.
    :param path:            folder from where to load the *requirements.txt files.
    :return:                portion package name.
    """
    dev_require: List[str] = list()
    requirements_file = os.path.join(path, nev_str(nev, 'REQ_FILE_NAME'))
    if os.path.exists(requirements_file):
        dev_require.extend(
            _ for _ in file_content(requirements_file).strip().split('\n') if not _.startswith('#'))
    nev['docs_require'] = [_ for _ in dev_require if _.startswith('sphinx_')]
    nev['install_require'] = [_ for _ in dev_require if not _.startswith('sphinx_')]
    nev['setup_require'] = [_ for _ in nev['install_require'] if not _.startswith(f'{namespace_name}_')]  # e.g. de_core
    nev['portions_package_names'] = portions_package_names = [_ for _ in dev_require
                                                              if _.startswith(f'{namespace_name}_')]

    tests_require: List[str] = list()
    requirements_file = os.path.join(path, nev_str(nev, 'REQ_TEST_FILE_NAME'))
    if os.path.exists(requirements_file):
        tests_require.extend(_ for _ in file_content(requirements_file).strip().split('\n') if not _.startswith('#'))
    nev['tests_require'] = tests_require

    return portions_package_names


def namespace_env_vars(namespace_name: str, pkg_root_path: str = "", old_nev: Optional[NevType] = None) -> NevType:
    """ update variables, names and file paths of the currently executed/installed namespace development environment.

    :param namespace_name:  root name of this namespace.
    :param pkg_root_path:   optional rel/abs path to package root (def=current working directory).
    :param old_nev          optional current namespace environment variables to be updated.
    :return:                dict with namespace environment variables/info.
    """
    nev: NevType = old_nev if isinstance(old_nev, dict) else dict()
    nev['namespace_name'] = namespace_name

    # add string globals like PORTIONS_COMMON_DIR if not already added
    for var_name, var_val in globals().items():
        if not var_name.startswith('_') and var_name not in nev and isinstance(var_val, str):
            nev[var_name] = var_val

    if not pkg_root_path:
        pkg_root_path = os.getcwd()
    elif not os.path.isabs(pkg_root_path):
        pkg_root_path = os.path.join(os.getcwd(), pkg_root_path)
    nev['package_root_path'] = pkg_root_path

    if os.path.exists(os.path.join(pkg_root_path, 'setup.py')):     # namespace root or portion
        setup_path = pkg_root_path
    elif os.path.exists(os.path.join(pkg_root_path, 'conf.py')):    # RTD build
        setup_path = os.path.join(pkg_root_path, '..')
    else:
        raise RuntimeError(f"Neither setup.py nor conf.py found in package root {pkg_root_path}")
    nev['setup_path'] = setup_path

    portion_root_path = os.path.join(setup_path, namespace_name)
    portion_type, portion_name = portion_type_name(portion_root_path)
    nev['portion_type'] = portion_type
    nev['portion_name'] = portion_name

    nev['portion_file_name'] = portion_file_name = \
        portion_name + (os.path.sep + '__init__.py' if portion_type == _PT_PKG else nev_str(nev, 'PY_EXT'))
    nev['portion_file_path'] = portion_file_path = \
        os.path.abspath(os.path.join(portion_root_path, portion_file_name))
    nev['package_name'] = f"{namespace_name}_{portion_name}"
    nev['pip_name'] = f"{namespace_name}-{portion_name.replace('_', '-')}"
    nev['import_name'] = f"{namespace_name}.{portion_name}"
    nev['package_version'] = code_file_version(portion_file_path) if portion_type else 'x.y.z'
    nev['root_version'] = 'un.kno.wn' if portion_type else code_file_version(os.path.join(setup_path, 'setup.py'))
    nev['repo_root'] = f"https://gitlab.com/{namespace_name}-group"
    nev['repo_pages'] = f"https://{namespace_name}-group.gitlab.io"
    nev['pypi_root'] = "https://pypi.org/project"

    # load requirements from *requirements.txt
    portions_package_names = load_requirements(namespace_name, nev, setup_path)

    # provide additional package info used by the root package templates
    nev['portions_pypi_refs_md'] = "\n".join(
        f'* [{_}]({nev["pypi_root"]}/{_} "{namespace_name} namespace portion {_}")'
        for _ in portions_package_names)  # used in root README.md.tpl
    namespace_len = len(namespace_name)
    nev['portions_import_names'] = ("\n" + " " * 4).join(
        _[:namespace_len] + '.' + _[namespace_len + 1:]
        for _ in portions_package_names)  # used in docs/index.rst.tpl

    # finally check if optional hook exists and if yes then run it for to change the nev values accordingly
    if nev_update_hook_exec(nev, pkg_root_path, setup_path) and old_nev is None:
        # run this function one time recursively for to update nev with extended env var values
        nev = namespace_env_vars(namespace_name, pkg_root_path=pkg_root_path, old_nev=nev)

    return nev


def nev_update_hook_exec(nev: NevType, path: str = "", extra_path: str = "") -> bool:
    """ check if optional EXTEND_NAMESPACE_FILE_NAME hook file exists and if yes then run it for to change nev values.

    :param nev:         namespace environment variables.
    :param path:        optional first search path/folder of the Python hook file.
    :param extra_path:  optional second search path/folder of the Python hook file.
    :return:            True if nev got updated, else False.
    """
    old_file = nev_str(nev, 'EXTEND_NAMESPACE_FILE_NAME')

    file_path = os.path.join(path, old_file)
    if not os.path.exists(file_path):
        file_path = os.path.join(extra_path, old_file)
        if not os.path.exists(file_path):
            file_path = ""

    if file_path:
        exec(compile(file_content(file_path), file_path, 'exec'), dict(nev=nev))
        if nev_str(nev, 'EXTEND_NAMESPACE_FILE_NAME') != old_file:
            # run the redirected hook recursively, now with a new hook file name
            nev_update_hook_exec(nev, path=path, extra_path=extra_path)

    return bool(file_path)


def nev_str(nev: NevType, var_name: str) -> str:
    """ determine string value of namespace environment variable from passed nev or use default.

    AssertionError will be raised if the specified variable value is not of type str. Use :func:`nev_val` instead.

    :param nev:         namespace environment variables.
    :param var_name:    name of variable.
    :return:            variable value - if not exists in nev then the constant/default value of this module or "".
    """
    val = nev_val(nev, var_name)
    assert isinstance(val, str), f"nev_str() can only return environment variables of type string, got {type(val)}"
    return val


def nev_val(nev: NevType, var_name: str) -> NevVarType:
    """ determine value of namespace environment variable from passed nev or use default.

    :param nev:         namespace environment variables.
    :param var_name:    name of variable.
    :return:            variable value - if not exists in nev then the constant/default value of this module or "".
    """
    return nev.get(var_name, globals().get(var_name, ""))


def patch_string(string: str, placeholder: str, replacer: Callable[[str], str], nev: Optional[NevType] = None) -> str:
    """ load file content, then replace patch_name placeholders and return patched/extended file content.

    :param string:      file name to patch (mostly a template).
    :param placeholder: name/id of the placeholder.
    :param replacer:    callable for to convert placeholder args into replacement string.
    :param nev:         optional namespace environment vars used (only needed if TEMPLATE_* constants got patched).
    :return:            file content extended with include snippets found in the same directory.
    """
    if nev is None:
        nev = dict()

    beg = 0
    pre = nev_str(nev, 'TEMPLATE_PLACEHOLDER_ID_PREFIX') + placeholder + nev_str(nev, 'TEMPLATE_PLACEHOLDER_ID_SUFFIX')
    len_pre = len(pre)
    suf = nev_str(nev, 'TEMPLATE_PLACEHOLDER_ARGS_SUFFIX')
    len_suf = len(suf)

    while True:
        beg = string.find(pre, beg)
        if beg == -1:
            break
        end = string.find(suf, beg)
        assert end != -1, f"patch_string() is missing args suffix marker ({suf})"
        string = string[:beg] + replacer(string[beg + len_pre: end]) + string[end + len_suf:]

    return string


def patch_templates(nev: NevType, exclude_folder: str = '', **replacer: Callable[[str], str]) -> List[str]:
    """ convert ae namespace package templates found in the cwd or underneath (except excluded) to the final files.

    :param nev:             dict namespace environment variables (determined by namespace_env_vars()).
    :param exclude_folder:  directory name to exclude from templates search.
    :param replacer:        optional dict of replacer with key=placeholder-id and value=callable.
                            If not passed then only the replacer with id TEMPLATE_INCLUDE_FILE_PLACEHOLDER_ID and its
                            callable/func :func:`replace_with_file_content_or_default` will be executed.
    :return:                list of patched template file names.
    """
    patched = list()
    fn_prefix = nev_str(nev, 'TEMPLATE_FILE_NAME_PREFIX')
    if len(replacer) == 0:
        replacer[nev_str(nev, 'TEMPLATE_INCLUDE_FILE_PLACEHOLDER_ID')] = replace_with_file_content_or_default
    for file_path in glob.glob(f"**/{fn_prefix}*.*", recursive=True):
        if not exclude_folder or not file_path.startswith(exclude_folder + os.path.sep):
            content = file_content(file_path)
            content = content.format(**nev)
            for key, func in replacer.items():
                content = patch_string(content, key, func)
            path, file = os.path.split(file_path)
            with open(os.path.join(path, file[len(fn_prefix):]), 'w') as file_handle:
                file_handle.write(content)
            patched.append(file_path)
    return patched


def portion_type_name(portion_root_path: str, portion_type: str = _PT_MOD, portion_end: str = PY_EXT
                      ) -> Tuple[str, str]:
    """ determine portion type and name.

    :param portion_root_path:   file path of the root of the namespace portions.
    :param portion_type:        searched portion type: PT_MOD or PT_PKG.
    :param portion_end:         file name suffix of the portion code file: PY_EXT or os.path.sep.
    :return:                    tuple of portion type and name strings.
    """
    if os.path.exists(portion_root_path):                   # run/imported by portion repository
        search_module = portion_type == _PT_MOD
        files = [fn for fn in glob.glob(os.path.join(portion_root_path, '*' + portion_end)) if '__' not in fn]
        if len(files) > 1:
            raise RuntimeError(f"More than one {portion_type} found: {files}")
        if len(files) == 0:
            if not search_module:
                raise RuntimeError(f"Neither module nor sub-package found in package path {portion_root_path}")
            return portion_type_name(portion_root_path, _PT_PKG, os.path.sep)
        portion_name = os.path.split(files[0][:-len(portion_end)])[1]
    else:                                                   # imported by namespace root repo
        portion_type = ''
        portion_name = "{portion-name}"

    return portion_type, portion_name


def replace_with_file_content_or_default(args_str: str) -> str:
    """ return file content if file name specified in first string arg exists, else return empty string or 2nd arg str.

    :param args_str:    pass either file name or file name and default string separated by a comma character.
    :return:            file content or default string or empty string (if file not exists and no default string given).
    """
    include = args_str.split(",")
    file_name = include[0].strip()
    if os.path.exists(file_name):
        include.append(file_content(file_name))
    else:
        include.insert(1, "")
    return include[-1]
