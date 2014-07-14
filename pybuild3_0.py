# -*- coding: utf-8 -*-
import os
import pycompile

#Alpha Beta RC
testname = "Alpha"      
basepath = "m:\\"
rev = pycompile.get_svn_rev( basepath )
rev.strip()
if len(rev)<6:
        rev="0"*(6-len(rev))+rev

revname = "V3.0.0_Build"+rev+".DUARIC30_"+testname;
destpath = u"D:\\字幕版本发布\\".encode("mbcs")+revname+"\\"

builder = pycompile.init_vcbuild( 10.0 )
os.chdir(basepath)

pycompile.delete_allfiles( r"bin64\plug_in\PlayEffects\\")

pycompile.build_solution( builder, r"Src\xcgMTCGPro2010.sln", "Debug", "x64", retry_count = 10 )
pycompile.build_solution( builder, r"SrcPlug_In\XCGPlugInSolution\XCGPlugInSolution2010.sln", "Debug", "x64", retry_count = 10,  rebuild = True )


pycompile.build_solution( builder, r"Src\xcgMTCGPro2010.sln", "Release", "x64", retry_count = 10 )
pycompile.build_solution( builder, r"SrcPlug_In\XCGPlugInSolution\XCGPlugInSolution2010.sln", "Release", "x64", retry_count = 10, rebuild = True )

print "build completed!"

ignore = pycompile.get_ignore_fromfile("ignore.txt")

pycompile.copy_output_direction("bin64", destpath, ignore )
os.chdir(destpath)
pycompile.call_shellcommand("makerelease.bat")
pycompile.copy_output_direction(u"D:\\字幕版本发布\\profile".encode('mbcs'), destpath+"profile" )
#pycompile.copy_output_file(u"D:\\字幕版本发布\\ServerConfig.ini".encode('mbcs'), destpath+"ServerConfig.ini" )

pycompile.git_commit(destpath, revname  )





