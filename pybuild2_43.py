# -*- coding: utf-8 -*-
import os
import pycompile
basepath = "N:\\dayang\\dyxcg\\xcg\\"
rev = pycompile.get_svn_rev( basepath )
rev.strip()
if len(rev)<6:
        rev="0"*(6-len(rev))+rev

destpath = u"D:\\字幕版本发布\\".encode("mbcs")+"V2.4.3_Build"+rev+".DAURIC_Alpha\\"

builder = pycompile.init_vcbuild( 8.0 )
os.chdir(basepath)

pycompile.build_solution( builder, r"CommonShare\Src\DSCommonShare2005.sln", "Debug", "x64" )
pycompile.build_solution( builder, r"CommonShare\Plugin\DSFilePlugIn\DSFilePlugIn2005.sln", "Debug", "x64" )

pycompile.build_solution( builder, r"CommonShare\Src\DSCommonShare2005.sln", "Release", "x64" )
pycompile.build_solution( builder, r"CommonShare\Plugin\DSFilePlugIn\DSFilePlugIn2005.sln", "Release", "x64" )
pycompile.call_shellcommand("CopyCommonShare.bat")
pycompile.call_shellcommand('echo "" |compileShader.bat')

pycompile.build_solution( builder, r"Src\XCGSolution\ComOdbcInterface.sln", "Unicode_Debug", "win32" )
pycompile.build_solution( builder, r"Src\XCGSolution\UtilitySolution.sln", "Unicode_Debug", "x64" )
pycompile.build_solution( builder, r"Src\XCGSolution\CoreSolution.sln", "Unicode_Debug", "x64" )
pycompile.build_solution( builder, r"Src\XCGSolution\ApplicationSolution.sln", "Unicode_Debug", "x64" )

#注意这个工程
pycompile.build_solution( builder, r"SrcPlug_In\Models\X3D_LIB\CyberX3D\vc\CyberX3D.sln", "Debug", "x64" )

pycompile.build_solution( builder, r"SrcPlug_In\XCGPlugInSolution\XCGPlugInSolution.sln", "Unicode_Debug", "x64" )

pycompile.build_solution( builder, r"Src\XCGSolution\ComOdbcInterface.sln", "Unicode_ReleaseD", "win32" )
pycompile.build_solution( builder, r"Src\XCGSolution\UtilitySolution.sln", "Unicode_ReleaseD", "x64" )
pycompile.build_solution( builder, r"Src\XCGSolution\CoreSolution.sln", "Unicode_ReleaseD", "x64" )
pycompile.build_solution( builder, r"Src\XCGSolution\ApplicationSolution.sln", "Unicode_ReleaseD", "x64" )
pycompile.build_solution( builder, r"SrcPlug_In\Models\X3D_LIB\CyberX3D\vc\CyberX3D.sln", "Release", "x64" )
pycompile.build_solution( builder, r"SrcPlug_In\XCGPlugInSolution\XCGPlugInSolution.sln", "Unicode_Release", "x64" )

print "build completed!"

a = """ *debug\\
*release\\
bin_release\\
Log\\
pdbdata
*.dsw
*.ncb
*.plg
*.opt
*.aps
*.bsc
*.obj
*.idb
*.pdb
*.pch
*.res
*.sbr
*.hm
*.clw
*.scc
*.stt
*.tmp
*.bak
*.~*
~*.*
_*.*
*.ilk
*.exp
*.vs?scc
*.lib
*.map
*UD.dll
*UD.exe
*UD.ocx
*UD.ski
CGReviewUD.exe
CGReviewU.exe"""
ignore = [l.strip() for l in a.split("\n" )]

pycompile.copy_output_direction("Bin", destpath+"Bin", ignore )
pycompile.copy_output_direction("Plug_In", destpath+"Plug_In", ignore )
pycompile.copy_output_direction("Sys", destpath+"Sys", ignore )


