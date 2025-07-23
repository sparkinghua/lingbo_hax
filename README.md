[807/812] Generating ../../python/mitsuba/__init__.pyi
      FAILED: python/mitsuba/__init__.pyi /home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3/_skbuild/linux-x86_64-3.12/cmake-build/python/mitsuba/__init__.pyi
      cd /home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3/_skbuild/linux-x86_64-3.12/cmake-build/src/python && /tmp/pip-build-env-7x94au_s/overlay/lib/python3.12/site-packages/cmake/data/bin/cmake -E env PYTHONPATH=/home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3/_skbuild/linux-x86_64-3.12/cmake-build/python:/tmp/pip-build-env-7x94au_s/site /home/public_account_1/miniconda3/envs/neuralyarn/bin/python -Xutf8 /home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3/src/python/../../resources/generate_stub_files.py /home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3/_skbuild/linux-x86_64-3.12/cmake-build/python/mitsuba
      WARNING:root:The `mitsuba` package relies on `drjit` and needs it to be installed at a specific location. Currently, `drjit` is located at "/tmp/pip-build-env-7x94au_s/overlay/lib/python3.12/site-packages/drjit" when it is expected to be at "/home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3/_skbuild/linux-x86_64-3.12/cmake-build/python/drjit". This can happen when both packages are not installed in the same Python environment. You will very likely experience linking issues if you do not fix this.
      Traceback (most recent call last):
        File "/home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3/_skbuild/linux-x86_64-3.12/cmake-build/python/mitsuba/__init__.py", line 107, in __getattribute__
          _import('mitsuba.mitsuba_' + variant + '_ext'),
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "/home/public_account_1/miniconda3/envs/neuralyarn/lib/python3.12/importlib/__init__.py", line 90, in import_module
          return _bootstrap._gcd_import(name[level:], package, level)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
        File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
        File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
        File "<frozen importlib._bootstrap>", line 921, in _load_unlocked
        File "<frozen importlib._bootstrap>", line 813, in module_from_spec
        File "<frozen importlib._bootstrap_external>", line 1289, in create_module
        File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
      ImportError: pybind11::detail::get_type_info: unable to find type info for "drjit::Array<float, 0ul>"
      
      During handling of the above exception, another exception occurred:
      
      Traceback (most recent call last):
        File "/home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3/src/python/../../resources/generate_stub_files.py", line 369, in <module>
          buffer, submodules = process_module(mi, top_module=True)
                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "/home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3/src/python/../../resources/generate_stub_files.py", line 305, in process_module
          for k in dir(m):
                   ^^^^^^
        File "/home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3/_skbuild/linux-x86_64-3.12/cmake-build/python/mitsuba/__init__.py", line 253, in __getattribute__
          result = module.__getattribute__(key)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "/home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3/_skbuild/linux-x86_64-3.12/cmake-build/python/mitsuba/__init__.py", line 115, in __getattribute__
          raise AttributeError(e)
      AttributeError: pybind11::detail::get_type_info: unable to find type info for "drjit::Array<float, 0ul>"
      [808/812] Building CXX object src/integrators/CMakeFiles/volpath.dir/volpath.cpp.o
      [809/812] Building CXX object src/integrators/CMakeFiles/volpathmis.dir/volpathmis.cpp.o
      ninja: build stopped: subcommand failed.
      Traceback (most recent call last):
        File "/tmp/pip-build-env-7x94au_s/overlay/lib/python3.12/site-packages/skbuild/setuptools_wrap.py", line 668, in setup
          cmkr.make(make_args, install_target=cmake_install_target, env=env)
        File "/tmp/pip-build-env-7x94au_s/overlay/lib/python3.12/site-packages/skbuild/cmaker.py", line 696, in make
          self.make_impl(clargs=clargs, config=config, source_dir=source_dir, install_target=install_target, env=env)
        File "/tmp/pip-build-env-7x94au_s/overlay/lib/python3.12/site-packages/skbuild/cmaker.py", line 741, in make_impl
          raise SKBuildError(msg)
      
      An error occurred while building with CMake.
        Command:
          /tmp/pip-build-env-7x94au_s/overlay/lib/python3.12/site-packages/cmake/data/bin/cmake --build . --target install --config Release --
        Install target:
          install
        Source directory:
          /home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3
        Working directory:
          /home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3/_skbuild/linux-x86_64-3.12/cmake-build
      Please check the install target is valid and see CMake's output for more information.
      
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for mitsuba
Failed to build mitsuba
ERROR: Could not build wheels for mitsuba, which is required to install pyproject.toml-based projects
(neuralyarn) public_account_1@AlgoServer:~/h50053752/neuralyarn/dependencies/mitsuba3$ pip show drjit
Name: drjit
Version: 0.4.6
Summary: A Just-In-Time-Compiler for Differentiable Rendering
Home-page: https://github.com/mitsuba-renderer/drjit
Author: Wenzel Jakob
Author-email: wenzel.jakob@epfl.ch
License: BSD
Location: /home/public_account_1/miniconda3/envs/neuralyarn/lib/python3.12/site-packages
Requires: 
Required-by:
