# -*- coding: utf-8 -*-

"""
Module et_micc_tools_tools.commands 
=================================================================

A module

"""
import os
import json
import shutil


import et_micc_tools.utils
import et_micc_tools.logging_tools
from et_micc_tools.f2py import build_f2py
from et_micc_tools.tomlfile import TomlFile


def micc_build( module_to_build, global_options ):
    """
    Build binary extensions, i.e. f2py modules and cpp modules.
    
    :param str module_to_build: name of the only module to build (the prefix 
        ``cpp_`` or ``f2py_`` may be omitted). If not provided, all binrary
        extensions are built.
    :param types.SimpleNamespace global_options: namespace object with
        options accepted by (almost) all et_micc_tools commands. Relevant attributes are 
        
        * **verbosity**
        * **project_path**: Path to the project on which the command operates.
        * **build_options**: all build options.
    """
    project_path = global_options.project_path

    et_micc_tools.utils.is_project_directory(project_path, raise_if=False)
    et_micc_tools.utils.is_package_project  (project_path, raise_if=False)
    et_micc_tools.utils.is_module_project   (project_path, raise_if=True )
    
    build_options = global_options.build_options
    
    package_path = project_path / et_micc_tools.utils.convert_to_valid_module_name(project_path.name)
        
    # get extension for binary extensions (depends on OS and python version)
    extension_suffix = et_micc_tools.utils.get_extension_suffix()
    
    dirs = os.listdir(package_path)
    for d in dirs:
        if (     (package_path / d).is_dir() 
             and (d.startswith("f2py_") or d.startswith("cpp_"))
           ):
            if module_to_build and not d.endswith(module_to_build): # build only this module
                continue

            build_log_file = project_path / f"et_micc_tools-build-{d}.log"
            build_logger = et_micc_tools.logging_tools.create_logger( build_log_file, filemode='w' )
 
            module_type,module_name = d.split('_',1)
            
            with et_micc_tools.logging_tools.log(build_logger.info,f"Building {module_type} module {module_name}"):
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
                    with et_micc_tools.utils.in_directory(module_dir):
                        if build_options.clean:
                            build_logger.info(f"--clean: removing {d}/_f2py_build")
                            shutil.rmtree('_f2py_build') 
                        returncode = build_f2py(module_name, args=f2py_args)
                    
                elif module_type=='cpp':
                    if build_options.load:
                        with open(str(module_dir / build_options.save),'r') as f:
                            build_options.cmake = json.load(f)
                    build_dir = module_dir  / '_cmake_build'
                    if build_options.clean:
                        build_logger.info(f"--clean: removing {d}/_cmake_build")
                        shutil.rmtree(build_dir) 
                    build_dir.mkdir(parents=True, exist_ok=True)
                    with et_micc_tools.utils.in_directory(build_dir):
                        cmake_cmd = ['poetry','run','cmake','-D',f"pybind11_DIR={et_micc_tools.utils.path_to_cmake_tools()}"]
                        for key,val in build_options.cmake.items():
                            cmake_cmd.extend(['-D',f"{key}={val}"])
                        cmake_cmd.append('..')
                        cmds = [ cmake_cmd
                               , ['make']
                               ]
                        # WARNING: for these commands to work in eclipse, eclipse must have
                        # started from the shell with the appropriate environment activated.
                        # Otherwise subprocess starts out with the wrong environment. It 
                        # may not pick the right Python version, and may not find pybind11.
                        returncode = et_micc_tools.utils.execute(cmds, build_logger.debug, stop_on_error=True, env=os.environ.copy())
                else:
                    raise RuntimeError(f"Unknown module_type: {module_type}")

                if returncode:
                    return returncode 
                
                built = build_dir / cextension
                destination = (package_path / cextension).resolve()
                if build_options.soft_link:
                    cmds = ['ln', '-sf', str(built), str(destination)]
                    returncode = et_micc_tools.utils.execute(cmds, build_logger.debug, stop_on_error=True, env=os.environ.copy())
                    if returncode:
                        return returncode 
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
                
            build_logger.info(f"Built: {destination}\n"
                              f"Check {build_log_file} for details."
                             )
    
    
    return 0


#eof