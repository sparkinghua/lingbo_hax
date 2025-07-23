(neuralyarn) public_account_1@AlgoServer:~/h50053752/neuralyarn/dependencies/mitsuba3/build$ ninja install
[1/1092] Linking CXX shared library libnanothread.so
FAILED: libnanothread.so 
: && /home/public_account_1/local/llvm-14/bin/clang++ -fPIC -stdlib=libc++ -D_LIBCPP_VERSION -fcolor-diagnostics -O3 -DNDEBUG -flto=thin  -stdlib=libc++ -shared -Wl,-soname,libnanothread.so -o libnanothread.so ext/drjit/ext/drjit-core/ext/nanothread/CMakeFiles/nanothread.dir/src/queue.cpp.o ext/drjit/ext/drjit-core/ext/nanothread/CMakeFiles/nanothread.dir/src/nanothread.cpp.o  -Wl,-rpath,:::::::::::::::::::::::: && :
/usr/bin/ld: /home/public_account_1/local/llvm-14/bin/../lib/LLVMgold.so: error loading plugin: /home/public_account_1/local/llvm-14/bin/../lib/LLVMgold.so: cannot open shared object file: No such file or directory
clang-10: error: linker command failed with exit code 1 (use -v to see invocation)
