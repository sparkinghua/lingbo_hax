(neuralyarn) public_account_1@AlgoServer:~/h50053752/neuralyarn/dependencies/mitsuba3$ pip install .
Looking in indexes: http://mirrors.tools.huawei.com/pypi/simple
Processing /home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Collecting drjit==0.4.6 (from mitsuba==3.5.2)
  Downloading http://mirrors.tools.huawei.com/pypi/packages/65/94/b7a9f0ff142a770ad0a2f33e802c74d553d615ea0300ee644a884ebe8761/drjit-0.4.6-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (4.7 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.7/4.7 MB 64.8 MB/s eta 0:00:00
Building wheels for collected packages: mitsuba
  Building wheel for mitsuba (pyproject.toml) ... error
  error: subprocess-exited-with-error
  
  × Building wheel for mitsuba (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [105 lines of output]
      
      
      --------------------------------------------------------------------------------
      -- Trying 'Ninja' generator
      --------------------------------
      ---------------------------
      ----------------------
      -----------------
      ------------
      -------
      --
      CMake Deprecation Warning at CMakeLists.txt:1 (cmake_minimum_required):
        Compatibility with CMake < 3.10 will be removed from a future version of
        CMake.
      
        Update the VERSION argument <min> value.  Or, use the <min>...<max> syntax
        to tell CMake that the project requires at least <min> but has been updated
        to work with policies introduced by <max> or earlier.
      
      Not searching for unused variables given on the command line.
      
      -- The C compiler identification is GNU 11.4.0
      -- Detecting C compiler ABI info
      -- Detecting C compiler ABI info - done
      -- Check for working C compiler: /usr/bin/cc - skipped
      -- Detecting C compile features
      -- Detecting C compile features - done
      -- The CXX compiler identification is GNU 11.4.0
      -- Detecting CXX compiler ABI info
      -- Detecting CXX compiler ABI info - done
      -- Check for working CXX compiler: /usr/bin/c++ - skipped
      -- Detecting CXX compile features
      -- Detecting CXX compile features - done
      -- Configuring done (0.5s)
      -- Generating done (0.0s)
      -- Build files have been written to: /home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3/_cmake_test_compile/build
      --
      -------
      ------------
      -----------------
      ----------------------
      ---------------------------
      --------------------------------
      -- Trying 'Ninja' generator - success
      --------------------------------------------------------------------------------
      
      Configuring Project
        Working directory:
          /home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3/_skbuild/linux-x86_64-3.12/cmake-build
        Command:
          /tmp/pip-build-env-cjnetbq_/overlay/lib/python3.12/site-packages/cmake/data/bin/cmake /home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3 -G Ninja -DCMAKE_MAKE_PROGRAM:FILEPATH=/home/public_account_1/miniconda3/envs/neuralyarn/bin/ninja --no-warn-unused-cli -DCMAKE_INSTALL_PREFIX:PATH=/home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3/_skbuild/linux-x86_64-3.12/cmake-install -DPYTHON_VERSION_STRING:STRING=3.12.4 -DSKBUILD:INTERNAL=TRUE -DCMAKE_MODULE_PATH:PATH=/tmp/pip-build-env-cjnetbq_/overlay/lib/python3.12/site-packages/skbuild/resources/cmake -DPYTHON_EXECUTABLE:PATH=/home/public_account_1/miniconda3/envs/neuralyarn/bin/python -DPYTHON_INCLUDE_DIR:PATH=/home/public_account_1/miniconda3/envs/neuralyarn/include/python3.12 -DPYTHON_LIBRARY:PATH=/home/public_account_1/miniconda3/envs/neuralyarn/lib/libpython3.12.so -DPython_EXECUTABLE:PATH=/home/public_account_1/miniconda3/envs/neuralyarn/bin/python -DPython_ROOT_DIR:PATH=/home/public_account_1/miniconda3/envs/neuralyarn -DPython_FIND_REGISTRY:STRING=NEVER -DPython_INCLUDE_DIR:PATH=/home/public_account_1/miniconda3/envs/neuralyarn/include/python3.12 -DPython3_EXECUTABLE:PATH=/home/public_account_1/miniconda3/envs/neuralyarn/bin/python -DPython3_ROOT_DIR:PATH=/home/public_account_1/miniconda3/envs/neuralyarn -DPython3_FIND_REGISTRY:STRING=NEVER -DPython3_INCLUDE_DIR:PATH=/home/public_account_1/miniconda3/envs/neuralyarn/include/python3.12 -DCMAKE_MAKE_PROGRAM:FILEPATH=/home/public_account_1/miniconda3/envs/neuralyarn/bin/ninja -DCMAKE_INSTALL_LIBDIR=mitsuba -DCMAKE_INSTALL_BINDIR=mitsuba -DCMAKE_INSTALL_INCLUDEDIR=mitsuba/include -DCMAKE_INSTALL_DATAROOTDIR=mitsuba/data -DCMAKE_TOOLCHAIN_FILE= -DMI_DRJIT_CMAKE_DIR:STRING= -DMI_SRGB_COEFF_FILE:STRING= -DMI_PYTHON_STUBS_DIR:STRING= -DCMAKE_BUILD_TYPE:STRING=Release
      
      Not searching for unused variables given on the command line.
      -- Mitsuba v3.5.2
      -- Mitsuba: setting portable compilation defaults for scikit-build.
      -- Mitsuba: using libc++.
      CMake Warning (dev) at /tmp/pip-build-env-cjnetbq_/overlay/lib/python3.12/site-packages/pybind11/share/cmake/pybind11/FindPythonLibsNew.cmake:98 (find_package):
        Policy CMP0148 is not set: The FindPythonInterp and FindPythonLibs modules
        are removed.  Run "cmake --help-policy CMP0148" for policy details.  Use
        the cmake_policy command to set the policy and suppress this warning.
      
      Call Stack (most recent call first):
        /tmp/pip-build-env-cjnetbq_/overlay/lib/python3.12/site-packages/pybind11/share/cmake/pybind11/pybind11Tools.cmake:50 (find_package)
        /tmp/pip-build-env-cjnetbq_/overlay/lib/python3.12/site-packages/pybind11/share/cmake/pybind11/pybind11Common.cmake:188 (include)
        /tmp/pip-build-env-cjnetbq_/overlay/lib/python3.12/site-packages/pybind11/share/cmake/pybind11/pybind11Config.cmake:250 (include)
        ext/drjit/ext/drjit-core/ext/nanothread/ext/cmake-defaults/CMakeLists.txt:284 (find_package)
        CMakeLists.txt:79 (include)
      This warning is for project developers.  Use -Wno-dev to suppress it.
      '/home/public_account_1/miniconda3/envs/neuralyarn/bin/python' '-c' 'import pybind11; print(pybind11.get_cmake_dir())'
      
      -- Found pybind11: /tmp/pip-build-env-cjnetbq_/overlay/lib/python3.12/site-packages/pybind11/include (found version "2.11.1")
      '/home/public_account_1/miniconda3/envs/neuralyarn/bin/python' '-c' 'import drjit; print(drjit.get_cmake_dir())'
      -- Found Dr.Jit: /tmp/pip-build-env-cjnetbq_/overlay/lib/python3.12/site-packages/drjit/include (found version "0.4.6" )
      -- Mitsuba: building the following variants:
      --  * scalar_rgb
      --  * scalar_spectral
      --  * cuda_ad_rgb
      --  * llvm_ad_rgb
      CMake Error at ext/embree/CMakeLists.txt:19 (CMAKE_MINIMUM_REQUIRED):
        Compatibility with CMake < 3.5 has been removed from CMake.
      
        Update the VERSION argument <min> value.  Or, use the <min>...<max> syntax
        to tell CMake that the project requires at least <min> but has been updated
        to work with policies introduced by <max> or earlier.
      
        Or, add -DCMAKE_POLICY_VERSION_MINIMUM=3.5 to try configuring anyway.
      
      
      -- Configuring incomplete, errors occurred!
      Traceback (most recent call last):
        File "/tmp/pip-build-env-cjnetbq_/overlay/lib/python3.12/site-packages/skbuild/setuptools_wrap.py", line 660, in setup
          env = cmkr.configure(
                ^^^^^^^^^^^^^^^
        File "/tmp/pip-build-env-cjnetbq_/overlay/lib/python3.12/site-packages/skbuild/cmaker.py", line 354, in configure
          raise SKBuildError(msg)
      
      An error occurred while configuring with CMake.
        Command:
          /tmp/pip-build-env-cjnetbq_/overlay/lib/python3.12/site-packages/cmake/data/bin/cmake /home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3 -G Ninja -DCMAKE_MAKE_PROGRAM:FILEPATH=/home/public_account_1/miniconda3/envs/neuralyarn/bin/ninja --no-warn-unused-cli -DCMAKE_INSTALL_PREFIX:PATH=/home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3/_skbuild/linux-x86_64-3.12/cmake-install -DPYTHON_VERSION_STRING:STRING=3.12.4 -DSKBUILD:INTERNAL=TRUE -DCMAKE_MODULE_PATH:PATH=/tmp/pip-build-env-cjnetbq_/overlay/lib/python3.12/site-packages/skbuild/resources/cmake -DPYTHON_EXECUTABLE:PATH=/home/public_account_1/miniconda3/envs/neuralyarn/bin/python -DPYTHON_INCLUDE_DIR:PATH=/home/public_account_1/miniconda3/envs/neuralyarn/include/python3.12 -DPYTHON_LIBRARY:PATH=/home/public_account_1/miniconda3/envs/neuralyarn/lib/libpython3.12.so -DPython_EXECUTABLE:PATH=/home/public_account_1/miniconda3/envs/neuralyarn/bin/python -DPython_ROOT_DIR:PATH=/home/public_account_1/miniconda3/envs/neuralyarn -DPython_FIND_REGISTRY:STRING=NEVER -DPython_INCLUDE_DIR:PATH=/home/public_account_1/miniconda3/envs/neuralyarn/include/python3.12 -DPython3_EXECUTABLE:PATH=/home/public_account_1/miniconda3/envs/neuralyarn/bin/python -DPython3_ROOT_DIR:PATH=/home/public_account_1/miniconda3/envs/neuralyarn -DPython3_FIND_REGISTRY:STRING=NEVER -DPython3_INCLUDE_DIR:PATH=/home/public_account_1/miniconda3/envs/neuralyarn/include/python3.12 -DCMAKE_MAKE_PROGRAM:FILEPATH=/home/public_account_1/miniconda3/envs/neuralyarn/bin/ninja -DCMAKE_INSTALL_LIBDIR=mitsuba -DCMAKE_INSTALL_BINDIR=mitsuba -DCMAKE_INSTALL_INCLUDEDIR=mitsuba/include -DCMAKE_INSTALL_DATAROOTDIR=mitsuba/data -DCMAKE_TOOLCHAIN_FILE= -DMI_DRJIT_CMAKE_DIR:STRING= -DMI_SRGB_COEFF_FILE:STRING= -DMI_PYTHON_STUBS_DIR:STRING= -DCMAKE_BUILD_TYPE:STRING=Release
        Source directory:
          /home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3
        Working directory:
          /home/public_account_1/h50053752/neuralyarn/dependencies/mitsuba3/_skbuild/linux-x86_64-3.12/cmake-build
      Please see CMake's output for more information.
      
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for mitsuba
Failed to build mitsuba
ERROR: Could not build wheels for mitsuba, which is required to install pyproject.toml-based projects
