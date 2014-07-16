
import os
import pycompile
basepath = "M:\\"
builder = pycompile.init_vcbuild( 10.0 )
os.chdir(basepath)

#pycompile.build_prj_list( builder, "buildfile.txt", "buildoutput.txt" )
pycompile.build_prj_list( builder, "buildPlugInfile.txt", "buildPlugInoutput.txt" )

