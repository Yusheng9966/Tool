import distutils.msvc9compiler
print "VERSION 0", distutils.msvc9compiler.VERSION
distutils.msvc9compiler.VERSION = 10.0
msvc = distutils.msvc9compiler.MSVCCompiler()
msvc.initialize("win32")
a = msvc.find_exe("devenv.exe")
print a
