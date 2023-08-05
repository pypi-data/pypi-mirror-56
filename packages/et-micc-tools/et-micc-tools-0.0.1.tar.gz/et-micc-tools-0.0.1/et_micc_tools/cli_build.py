# -*- coding: utf-8 -*-
"""Command line interface build (no sub-commands)."""


import os,sys
from types import SimpleNamespace
from pathlib import Path

import click

import et_micc_tools.commands as cmds
# import et_micc_tools.utils
import et_micc_tools.logging_tools
import et_micc_tools.expand

__template_help  =  "Ordered list of Cookiecutter templates, or a single Cookiecutter template."

__micc_file_help = ("The path to the *micc-file* with the parameter values used in the cookiecutter"
                    "templates. When a new project is created, "
                    "in the cookiecutter templates (default = ``micc.json``). "
                    "*Micc* does not use the standard ``cookiecutter.json`` file to provide the "
                    "template parameters, but uses a *micc-file*, usually named ``micc.json``, to "
                    "generate a ``cookiecutter.json`` file. Unlike the ``cookiecutter.json`` file, "
                    "the ``micc.json`` file can contain default values for the template parameters. "
                    "You will be prompted to provide a value for all parameters without default value. "
                    "*Micc* looks for the *micc-file* in the template directory **only** "
                    "(as specified with the ``--template`` option)."
                   )


@click.group()
@click.option('-v', '--verbosity', count=True
             , help="The verbosity of the program output."
             , default=1
             )
@click.option('-p', '--project-path'
             , help="The path to the project directory. "
                    "The default is the current working directory."
             , default='.'
             , type=Path
             )
@click.option('--clear-log'
             , help="If specified clears the project's ``et_micc_tools.log`` file."
             , default=False, is_flag=True
             )
@click.pass_context
def main(ctx, verbosity, project_path, clear_log):
    """Micc command line interface.
    
    All commands that change the state of the project produce some output that
    is send to the console (taking verbosity into account). It is also sent to
    a logfile ``et_micc_tools.log`` in the project directory. All output is always appended
    to the logfile. If you think the file has gotten too big, or you are no more
    interested in the history of your project, you can specify the ``--clear-log``
    flag to clear the logfile before any command is executed. In this way the
    command you execute is logged to an empty logfile.
    
    See below for (sub)commands.
    """
    if clear_log:
        os.remove(project_path / 'micc.log')
        
    ctx.obj = SimpleNamespace( verbosity=verbosity
                             , project_path=project_path.resolve()
                             , clear_log=clear_log
                             , template_parameters={}
                             )

#     if et_micc_tools.utils.is_conda_python():
#         click.echo( click.style("==========================================================\n"
#                                 "WARNING: You are running in a conda Python environment.\n"
#                                 "         Note that poetry does not play well with conda.\n",   fg='yellow')
#                   + click.style("         Especially, do NOT use:\n"
#                                 "         >  poetry install\n",                                 fg='bright_red')
#                   + click.style("==========================================================\n", fg='yellow')
#                   )
    template_parameters_json = project_path / 'micc.json'
    if template_parameters_json.exists():
        ctx.obj.template_parameters.update(
            et_micc_tools.expand.get_template_parameters(template_parameters_json)
        )
    else:
        ctx.obj.template_parameters.update(
            et_micc_tools.expand.get_template_parameters(
                et_micc_tools.expand.get_preferences(Path('.'))
            )
        )
    

def _check_cxx_flags(cxx_flags,cli_option):
    """
    :param str cxx_flags: C++ compiler flags
    :param str cli_option: typically '--cxx-flags', or '--cxx-flags-all'.
    :raises: RunTimeError if cxx_flags starts or ends with a '"' but not both.
    """
    if cxx_flags.startswith('"') and cxx_flags.endswith('"'):
        # compile options appear between quotes
        pass
    elif not cxx_flags.startswith('"') and not cxx_flags.endswith('"'):
        # a singlecompile option must still be surrounded with quotes. 
        cxx_flags = f'"{cxx_flags}"'
    else:
        raise RuntimeError(f"{cli_option}: unmatched quotes: {cxx_flags}")
    return cxx_flags


def _check_load_save(filename,loadorsave):
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


@main.command()
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
@click.pass_context
def build( ctx, module
         , build_type
# F2py specific options
         , f90exec
         , f90flags, opt, arch
         , debug, noopt, noarch
# Cpp specific options
         , cxx_compiler
         , cxx_flags, cxx_flags_all
# Other options
         , clean
         , soft_link
         , load, save
         ):
    """Build binary extension libraries (f2py and cpp modules)."""
    if save:
        if os.sep in save:
            raise RuntimeError(f"--save {save}: only filename allowed, not path.")
        if not save.endswith('.json'):
            save += '.json'
    if load:
        if os.sep in load:
            raise RuntimeError(f"--load {load}: only filename allowed, not path.")
        if not load.endswith('.json'):
            load += '.json'
    
    with et_micc_tools.logging_tools.logtime(ctx.obj):            
        build_options=SimpleNamespace( build_type = build_type.upper() )
        build_options.clean = clean
        build_options.soft_link = soft_link
        build_options.save = _check_load_save(save, "save")
        build_options.load = _check_load_save(load, "load")
        if not load:
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
                cmake[f"CMAKE_CXX_FLAGS_{build_type}"] = _check_cxx_flags(cxx_flags,"--cxx-flags")
            if cxx_flags_all:
                cmake["CMAKE_CXX_FLAGS"] = _check_cxx_flags(cxx_flags_all,"--cxx-flags-all")
            build_options.cmake = cmake
            
        ctx.obj.build_options = build_options
        
        rc = cmds.micc_build( module_to_build=module
                            , global_options=ctx.obj
                            )
    if rc:
        ctx.exit(rc)
      

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
#eodf
