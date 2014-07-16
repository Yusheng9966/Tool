# -*- coding: utf-8 -*-
import os
import pycompile

package_now = raw_input(u"是否打包发版本(y/n)...?".encode('mbcs')) == 'y'
if package_now:
        package_cg = raw_input(u"是否为图文发布包(y/n)...?".encode('mbcs')) == 'y'
        if package_cg:
                print u"字幕发布模式...".encode('mbcs')
        else:
                print u"图文发布模式...".encode('mbcs')
        myversion = raw_input(u"输入版本号0 or 1...?".encode('mbcs'))
        print u"版本号为3.%d, 开始编译...".encode('mbcs')%myversion

#Alpha Beta RC
testname = "Alpha"      
basepath = "m:\\"

builder = pycompile.init_vcbuild( 10.0 )
os.chdir(basepath)

pycompile.delete_allfiles( r"bin64\plug_in\PlayEffects\\")

pycompile.build_prj_list( builder, "buildfile.txt", "buildoutput.txt" )
pycompile.build_prj_list( builder, "buildPlugInfile.txt", "buildPlugInoutput.txt" )

#pycompile.build_solution( builder, r"Src\xcgMTCGPro2010.sln", "Debug", "x64", retry_count = 10 )
#pycompile.build_solution( builder, r"SrcPlug_In\XCGPlugInSolution\XCGPlugInSolution2010.sln", "Debug", "x64", retry_count = 10 )

#pycompile.build_solution( builder, r"Src\xcgMTCGPro2010.sln", "Release", "x64", retry_count = 10 )
#pycompile.build_solution( builder, r"SrcPlug_In\XCGPlugInSolution\XCGPlugInSolution2010.sln", "Release", "x64", retry_count = 10 )

print "build completed!"

if not package_now:
        exit()

rev = pycompile.get_svn_rev( basepath )
rev.strip()
if len(rev)<6:
        rev="0"*(6-len(rev))+rev

if package_cg:
        revname = "V3.0.0_Build"+rev+".CGLive_Alpha"
        destpath = u"D:\\字幕版本发布\\".encode("mbcs")+revname+"\\"
else:
        if myversion == 0:
                revname = "V3.0.0_Build"+rev+".DUARIC30_"+testname;
                destpath = u"D:\\字幕版本发布\\".encode("mbcs")+revname+"\\"
        else:
                revname = "V3.1.0_Build"+rev+".DUARIC31_"+testname
                destpath = u"D:\\字幕版本发布\\".encode("mbcs")+revname+"\\"

ignore = pycompile.get_ignore_fromfile("ignore.txt")

pycompile.copy_output_direction("bin64", destpath, ignore )
os.chdir(destpath)
pycompile.call_shellcommand("makerelease.bat")
pycompile.copy_output_direction(u"D:\\字幕版本发布\\profile".encode('mbcs'), destpath+"profile" )

if package_cg:
        pycompile.copy_output_file(u"D:\\字幕版本发布\\ServerConfig.ini".encode('mbcs'), destpath+"ServerConfig.ini" )

pycompile.git_commit(destpath, revname )



