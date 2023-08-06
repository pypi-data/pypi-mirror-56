# -*- coding: utf-8 -*-
"""Command line interface build (no sub-commands)."""

import json
from pathlib import Path
import os
import shutil
import sys
import sysconfig
from types import SimpleNamespace

import click
import numpy.f2py

from et_micc.project import Project, micc_version
import et_micc.logging
import et_micc.utils


def get_extension_suffix():
    """Return the extension suffix, e.g. :file:`.cpython-37m-darwin.so`."""
    return sysconfig.get_config_var('EXT_SUFFIX')


def build_f2py(module_name,args=[]):
    """
    :param Path path: to f90 source
    """
    src_file = module_name + '.f90'

    path_to_src_file = Path(src_file).resolve()
    if not path_to_src_file.exists():
        raise FileNotFoundError(str(path_to_src_file))

    f2py_args = ['--build-dir','_f2py_build']
    f2py_args .extend(args)

    with open(str(path_to_src_file.name)) as f:
        fsource = f.read()
    returncode = numpy.f2py.compile(fsource, extension='.f90', modulename=module_name, extra_args=f2py_args, verbose=True)

    return returncode

def check_cxx_flags(cxx_flags,cli_option):
    """
    :param str cxx_flags: C++ compiler flags
    :param str cli_option: typically '--cxx-flags', or '--cxx-flags-all'.
    :raises: RunTimeError if cxx_flags starts or ends with a '"' but not both.
    """
    if cxx_flags.startswith('"') and cxx_flags.endswith('"'):
        # compile options appear between quotes
        pass
    elif not cxx_flags.startswith('"') and not cxx_flags.endswith('"'):
        # a single compile option must still be surrounded with quotes.
        cxx_flags = f'"{cxx_flags}"'
    else:
        raise RuntimeError(f"{cli_option}: unmatched quotes: {cxx_flags}")
    return cxx_flags


def path_to_cmake_tools():
    """Return the path to the folder with the CMake tools."""

    p = (Path(__file__) / '..' / 'cmake_tools').resolve()
    return str(p)


def check_load_save(filename,loadorsave):
    """
    :param str filename: possibly empty string.
    :param str loadorsave: 'load'|'save'.
    :raises: RunTimeError if filename is actually a file path.
    """
    if filename:
        if os.sep in filename:
            raise RuntimeError(f"--{loadorsave} {filename}: only filename allowed, not path.")
        if not filename.endswith('.json'):
            filename += '.json'
    return filename


def build_cmd(project):
    """
    Build binary extensions, i.e. f2py modules and cpp modules.

    :param str module_to_build: name of the only module to build (the prefix
        ``cpp_`` or ``f2py_`` may be omitted). If not provided, all binrary
        extensions are built.
    :param types.SimpleNamespace options: namespace object with
        options accepted by (almost) all et_micc commands. Relevant attributes are

        * **verbosity**
        * **project_path**: Path to the project on which the command operates.
        * **build_options**: all build options.
    """
    project_path = project.options.project_path
    if project.module:
        project.warning(
            f"Nothing to do. A module project ({project.project_name}) cannot have binary extension modules."
        )

    build_options = project.options.build_options

    # get extension for binary extensions (depends on OS and python version)
    extension_suffix = get_extension_suffix()

    package_path = project.options.project_path / project.package_name
    dirs = os.listdir(package_path)
    succeeded = []
    failed    = []
    for d in dirs:
        if (     (package_path / d).is_dir()
             and (d.startswith("f2py_") or d.startswith("cpp_"))
           ):
            if project.options.module_to_build and not d.endswith(project.options.module_to_build): 
                # build only  module module_to_build.
                continue
            
            build_log_file = project_path / f"et_micc-build-{d}.log"
            build_logger = et_micc.logging.create_logger( build_log_file, filemode='w' )

            module_type,module_name = d.split('_',1)

            with et_micc.logging.log(build_logger.info,f"Building {module_type} module {module_name}"):
                cextension = module_name + extension_suffix
                destination = (package_path / cextension).resolve()
                if build_options.clean:
                    os.remove(str(destination))
                module_dir = package_path / d
                if build_options.save:
                    with open(str(module_dir / build_options.save),'w') as f:
                        json.dump(build_options.f2py,f)

                if module_type=='f2py':
                    if build_options.load:
                        with open(str(module_dir / build_options.save),'r') as f:
                            build_options.f2py = json.load(f)
                    build_dir = module_dir
                    f2py_args = []
                    for arg,val in build_options.f2py.items():
                        if val is None:
                            # this is a flag
                            f2py_args.append(arg)
                        else:
                            f2py_args.append(f"{arg}=\"{val}\"")

                    if build_options.save:
                        with open(str(module_dir / build_options.save),'w') as f:
                            json.dump(build_options.f2py,f)
                    with et_micc.utils.in_directory(module_dir):
                        if build_options.clean:
                            build_logger.info(f"--clean: removing {d}/_f2py_build")
                            shutil.rmtree('_f2py_build')
                        project.exit_code = build_f2py(module_name, args=f2py_args)

                elif module_type=='cpp':
                    if build_options.load:
                        with open(str(module_dir / build_options.save),'r') as f:
                            build_options.cmake = json.load(f)
                    build_dir = module_dir  / '_cmake_build'
                    if build_options.clean:
                        build_logger.info(f"--clean: removing {d}/_cmake_build")
                        shutil.rmtree(build_dir)
                    build_dir.mkdir(parents=True, exist_ok=True)
                    with et_micc.utils.in_directory(build_dir):
                        cmake_cmd = ['cmake',
                                     '-D',f"PYTHON_EXECUTABLE={project.options.project_path / '.venv/bin/python'}",
                                     '-D',f"pybind11_DIR={path_to_cmake_tools()}",
                                    ]
                        for key,val in build_options.cmake.items():
                            cmake_cmd.extend(['-D',f"{key}={val}"])
                        cmake_cmd.append('..')
                        cmds = [ cmake_cmd
                               , ['make']
                               ]
                        # WARNING: for these commands to work in eclipse, eclipse must have
                        # been started from the shell with the appropriate environment acti-
                        # vated. Otherwise subprocess starts out with the wrong environment. 
                        # It may not pick the right Python version, and may not find pybind11.
                        project.exit_code = et_micc.utils.execute(cmds, build_logger.debug, stop_on_error=True, env=os.environ.copy())

                if project.exit_code:
                    failed.append(project.options.project_path.name / project.package_name / cextension)
                else:
                    built = build_dir / cextension
                    destination = (package_path / cextension).resolve()
                    if build_options.soft_link:
                        cmds = ['ln', '-sf', str(built), str(destination)]
                        returncode = et_micc.utils.execute(cmds, build_logger.debug, stop_on_error=True, env=os.environ.copy())
                        if returncode:
                            failed.append(project.options.project_path.name / project.package_name / cextension)
                    else:
                        if destination.exists():
                            build_logger.debug(f">>> os.remove({destination})\n")
                            destination.unlink()
                        build_logger.debug(f">>> shutil.copyfile( '{built}', '{destination}' )\n")
                        shutil.copyfile(built, destination)
    
                        # Remove the build directory to avoid that it will be included in the wheel
                        # (we cannot do this if build_options.soft_link is True
                        if module_type=='f2py':
                            build_dir = module_dir / '_f2py_build'
                        shutil.rmtree(build_dir)

                    succeeded.append(project.options.project_path.name / project.package_name / cextension)
    if succeeded:
        build_logger.info("\n\nBinary extensions built successfully:")
        for cextension in succeeded:
            build_logger.info(f"  - {cextension}")
    if failed:
        build_logger.error("\nBinary extensions failing to build:")
        for cextension in failed:
            build_logger.error(f"  - {cextension}")
    else:
        project.warning(
            f"No binary extensions found in package ({project.package_name})."
        )

@click.command()
@click.option('-v', '--verbosity', count=True
             , help="The verbosity of the program."
             , default=1
             )
@click.option('-p', '--project-path'
             , help="The path to the project directory. "
                    "The default is the current working directory."
             , default='.'
             , type=Path
             )
@click.option('-m','--module'
             , help="Build only this module. The module kind prefix (``cpp_`` "
                    "for C++ modules, ``f2py_`` for Fortran modules) may be omitted."
             , default=''
             )
@click.option('-b','--build-type'
             , help="build type: For f2py modules, either RELEASE or DEBUG, where the latter"
                    "toggles the --debug, --noopt, and --noarch, and ignores all other "
                    "f2py compile flags. For cpp modules any of the standard CMake build types: "
                    "DEBUG, MINSIZEREL, RELEASE, RELWITHDEBINFO."
             , default='RELEASE'
             )
# F2py specific options
@click.option('--f90exec'
             , help="F2py: Specify the path to F90 compiler."
             , default=''
             )
@click.option('--f90flags'
             , help="F2py: Specify F90 compiler flags."
             , default='-O3'
             )
@click.option('--opt'
             , help="F2py: Specify optimization flags."
             , default=''
             )
@click.option('--arch'
             , help="F2py: Specify architecture specific optimization flags."
             , default=''
             )
@click.option('--debug'
             , help="F2py: Compile with debugging information."
             , default=False, is_flag=True
             )
@click.option('--noopt'
             , help="F2py: Compile without optimization."
             , default=False, is_flag=True
             )
@click.option('--noarch'
             , help="F2py: Compile without architecture specific optimization."
             , default=False, is_flag=True
             )
# Cpp specific options
@click.option('--cxx-compiler'
             , help="CMake: specify the C++ compiler (sets CMAKE_CXX_COMPILER)."
             , default=''
             )
@click.option('--cxx-flags'
             , help="CMake: set CMAKE_CXX_FLAGS_<built_type> to <cxx_flags>."
             , default=''
             )
@click.option('--cxx-flags-all'
             , help="CMake: set CMAKE_CXX_FLAGS_<built_type> to <cxx_flags>."
             , default=''
             )
# Other options
@click.option('--clean'
             , help="Perform a clean build."
             , default=False, is_flag=True
             )
@click.option('--load'
             , help="Load the build options from a (.json) file in the module directory. "
                    "All other compile options are ignored."
             , default=''
             )
@click.option('--save'
             , help="Save the build options to a (.json) file in the module directory."
             , default=''
             )
@click.option('-s', '--soft-link'
             , help="Create a soft link rather than a copy of the binary extension module."
             , default=False, is_flag=True
             )
@click.version_option(version=micc_version())
def main(
        verbosity,
        project_path,
        module,
        build_type,
# F2py specific options
        f90exec,
        f90flags, opt, arch,
        debug, noopt, noarch,
# Cpp specific options
        cxx_compiler,
        cxx_flags, cxx_flags_all,
# Other options
        clean,
        soft_link,
        load, save,
    ):
    """Build binary extension libraries (f2py and cpp modules)."""
    if save:
        if os.sep in save:
            # TODO replace exception with error message and exit
            raise RuntimeError(f"--save {save}: only filename allowed, not path.")
        if not save.endswith('.json'):
            save += '.json'
    if load:
        if os.sep in load:
            # TODO replace exception with error message and exit
            raise RuntimeError(f"--load {load}: only filename allowed, not path.")
        if not load.endswith('.json'):
            load += '.json'

    options = SimpleNamespace(
        verbosity=verbosity,
        project_path=project_path.resolve(),
        clear_log = False
    )
    project = Project(options)
    with et_micc.logging.logtime(options):
        build_options = SimpleNamespace( build_type = build_type.upper() )
        build_options.clean = clean
        build_options.soft_link = soft_link
        build_options.save = check_load_save(save, "save")
        build_options.load = check_load_save(load, "load")
        if not load:
            # collect build options from command line:
            if build_type=='DEBUG':
                f2py = {'--debug' :None
                       ,'--noopt' :None
                       ,'--noarch':None
                       }
            else:
                f2py = {}
                if f90exec:
                    f2py['--f90exec'] = f90exec
                if f90flags:
                    f2py['--f90flags'] = f90flags
                if opt:
                    f2py['--opt'] = opt
                if arch:
                    f2py['--arch'] = arch
                if noopt:
                    f2py['--noopt'] = None
                if noarch:
                    f2py['--noarch'] = None
                if debug:
                    f2py['--debug'] = None
            build_options.f2py = f2py

            cmake = {}
            cmake['CMAKE_BUILD_TYPE'] = build_type
            if cxx_compiler:
                path_to_cxx_compiler = Path(cxx_compiler).resolve()
                if not path_to_cxx_compiler.exists():
                    raise FileNotFoundError(f"C++ compiler {path_to_cxx_compiler} not found.")
                cmake['CMAKE_CXX_COMPILER'] = str(path_to_cxx_compiler)
            if cxx_flags:
                cmake[f"CMAKE_CXX_FLAGS_{build_type}"] = check_cxx_flags(cxx_flags,"--cxx-flags")
            if cxx_flags_all:
                cmake["CMAKE_CXX_FLAGS"] = check_cxx_flags(cxx_flags_all,"--cxx-flags-all")
            build_options.cmake = cmake

        project.options.module_to_build = module
        project.options.build_options = build_options

        build_cmd(project)
    
    sys.exit(project.exit_code)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
#eodf
