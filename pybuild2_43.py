# -*- coding: utf-8 -*-
import os
import pycompile
basepath = "N:\\dayang\\dyxcg\\xcg\\"
rev = pycompile.get_svn_rev( basepath )
rev.strip()
if len(rev)<6:
        rev="0"*(6-len(rev))+rev

revname = "V2.4.3_Build"+rev+".DAURIC_Alpha"
destpath = u"D:\\字幕版本发布\\".encode("mbcs")+revname +"\\"

builder = pycompile.init_vcbuild( 8.0 )
os.chdir(basepath)

pycompile.build_solution( builder, r"CommonShare\Src\DSCommonShare2005.sln", "Debug", "x64", retry_count = 10 )
pycompile.build_solution( builder, r"CommonShare\Plugin\DSFilePlugIn\DSFilePlugIn2005.sln", "Debug", "x64", retry_count = 10 )

pycompile.build_solution( builder, r"CommonShare\Src\DSCommonShare2005.sln", "Release", "x64", retry_count = 10 )
pycompile.build_solution( builder, r"CommonShare\Plugin\DSFilePlugIn\DSFilePlugIn2005.sln", "Release", "x64", retry_count = 10 )
pycompile.call_shellcommand("CopyCommonShare.bat")
pycompile.call_shellcommand('echo "" |compileShader.bat')

pycompile.build_solution( builder, r"Src\XCGSolution\ComOdbcInterface.sln", "Unicode_Debug", "win32" )
pycompile.build_solution( builder, r"Src\XCGSolution\UtilitySolution.sln", "Unicode_Debug", "x64", retry_count = 10 )
pycompile.build_solution( builder, r"Src\XCGSolution\CoreSolution.sln", "Unicode_Debug", "x64", retry_count = 10 )
pycompile.copy_output_file(r"Src\CGDesigner\CGDesignerRes.h", r"Src\CGDesigner\CGDesignerRes.h~~" )
pycompile.copy_output_file(r"Src\CGDesigner\CGDesignerRes_map.h", r"Src\CGDesigner\CGDesignerRes.h" )
pycompile.build_solution( builder, r"Src\XCGSolution\ApplicationSolution.sln", "Unicode_Debug_Map", "x64", retry_count = 10 )
pycompile.copy_output_file(r"Src\CGDesigner\CGDesignerRes.h~~", r"Src\CGDesigner\CGDesignerRes.h" )
pycompile.build_solution( builder, r"Src\XCGSolution\ApplicationSolution.sln", "Unicode_Debug_Weather", "x64", retry_count = 10 )
#注意这个工程
pycompile.build_solution( builder, r"SrcPlug_In\Models\X3D_LIB\CyberX3D\vc\CyberX3D.sln", "Debug", "x64", retry_count = 10 )
pycompile.build_solution( builder, r"SrcPlug_In\XCGPlugInSolution\XCGPlugInSolution.sln", "Unicode_Debug", "x64", retry_count = 10 )


pycompile.build_solution( builder, r"Src\XCGSolution\ComOdbcInterface.sln", "Unicode_ReleaseD", "win32" )
pycompile.build_solution( builder, r"Src\XCGSolution\UtilitySolution.sln", "Unicode_ReleaseD", "x64", retry_count = 10 )
pycompile.build_solution( builder, r"Src\XCGSolution\CoreSolution.sln", "Unicode_ReleaseD", "x64", retry_count = 10 )
pycompile.build_solution( builder, r"Src\XCGSolution\ApplicationSolution.sln", "Unicode_ReleaseD", "x64", retry_count = 10 )
pycompile.copy_output_file(r"Src\CGDesigner\CGDesignerRes.h", r"Src\CGDesigner\CGDesignerRes.h~~" )
pycompile.copy_output_file(r"Src\CGDesigner\CGDesignerRes_map.h", r"Src\CGDesigner\CGDesignerRes.h" )
pycompile.build_solution( builder, r"Src\XCGSolution\ApplicationSolution.sln", "Unicode_Release_Map", "x64", retry_count = 10 )
pycompile.copy_output_file(r"Src\CGDesigner\CGDesignerRes.h~~", r"Src\CGDesigner\CGDesignerRes.h" )
pycompile.build_solution( builder, r"Src\XCGSolution\ApplicationSolution.sln", "Unicode_Release_Weather", "x64", retry_count = 10 )

pycompile.build_solution( builder, r"SrcPlug_In\Models\X3D_LIB\CyberX3D\vc\CyberX3D.sln", "Release", "x64", retry_count = 10 )
pycompile.build_solution( builder, r"SrcPlug_In\XCGPlugInSolution\XCGPlugInSolution.sln", "Unicode_Release", "x64", retry_count = 10 )

os.chdir("Plug_In\\filters")
pycompile.call_shellcommand('ReName.bat')
os.chdir(basepath)


print "build completed!"

ignore = pycompile.get_ignore_fromfile("ignore.txt")

pycompile.copy_output_direction("Bin", destpath+"Bin", ignore )
pycompile.copy_output_direction("Plug_In", destpath+"Plug_In", ignore )
pycompile.copy_output_direction("Sys", destpath+"Sys", ignore )

pycompile.git_commit(destpath, revname  )

