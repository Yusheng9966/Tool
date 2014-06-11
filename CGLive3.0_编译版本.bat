echo off
set e1=0


call "%VS100COMNTOOLS%vsvars32.bat"

cd C:\"Program Files (x86)"\Git\bin 
cd M:\
M:

echo "输入回车显示SVN版本号"
c:git svn log -1
set /p version=请输入SVN版本号:


rem msbuild /m:8 /V:m /t:clean /p:Configuration="Release" /p:Platform="x64" "M:\Src\xcgMTCGPro2010.sln" 

:loop1
cls
msbuild /m:8 /V:q /property:WarningLevel=0;Configuration="Release";Platform="x64" "M:\Src\xcgMTCGPro2010.sln"
if errorlevel 1 (pause
goto loop1)

rem msbuild /m:8 /V:m /t:clean /p:Configuration="Release" /p:Platform="x64" "M:\SrcPlug_In\XCGPlugInSolution\XCGPlugInSolution2010.sln"

:loop2
cls
msbuild /m:8 /V:m /ds /p:WarningLevel=0;Configuration="Release";Platform="x64" "M:\SrcPlug_In\XCGPlugInSolution\XCGPlugInSolution2010.sln"
if errorlevel 1 (pause
goto loop2)





md D:\字幕版本发布\V3.0.0_Build%version%.CGLive_Alpha
cd D:\字幕版本发布\V3.0.0_Build%version%.CGLive_Alpha
d:

rmdir /S /Q m:\bin64\temp
rmdir /S /Q m:\bin64\log

xcopy M:\bin64 d: /E /C /D /R /Y /EXCLUDE:D:\字幕版本发布\copyfilter.txt
call makerelease.bat
cd d:\D:\字幕版本发布


copy D:\字幕版本发布\\ServerConfig.ini D:\字幕版本发布\V3.0.0_Build%version%.CGLive_Alpha\

xcopy D:\字幕版本发布\profile D:\字幕版本发布\V3.0.0_Build%version%.CGLive_Alpha\ /E /C /D /R /Y 

start D:\字幕版本发布\V3.0.0_Build%version%.CGLive_Alpha

set /p bAdd=是否自动添加到库中（y/n）?
if bAdd==y c:git add D:\字幕版本发布\V3.0.0_Build%version%.CGLive_Alpha

c:
cd \tool
echo %version%| CGLive3.0_生成启动批处理.bat
pause
