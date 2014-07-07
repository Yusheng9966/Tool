# -*- coding: utf-8 -*-
import os
import pycompile
basepath = "N:\\dayang\\dyxcg\\xcg\\"

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


ignore = [ "*.dsw",
        "*.ncb",
        "*.plg",
        "*.opt",
        "*.aps",
        "*.bsc",
        "*.obj",
        "*.idb",
        "*.pdb",
        "*.pch",
        "*.res",
        "*.sbr",
        "*.hm",
        "*.clw",
        "*.scc",
        "*.stt",
        "*.tmp",
        "*.bak",
        "*.~*",
        "~*.*",
        "_*.*",
        "*.ilk",
        "*.exp",
        "*.vs?scc",
        "*debug\\",
        "*release\\" ]

pycompile.copy_output_direction("Bin", "D:\\字幕版本发布\\test\\Bin", ignore )





