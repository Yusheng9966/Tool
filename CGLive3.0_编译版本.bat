echo off
set e1=0


call "%VS100COMNTOOLS%vsvars32.bat"

cd C:\"Program Files (x86)"\Git\bin 
cd M:\
M:

echo "����س���ʾSVN�汾��"
c:git svn log -1
set /p version=������SVN�汾��:


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





md D:\��Ļ�汾����\V3.0.0_Build%version%.CGLive_Alpha
cd D:\��Ļ�汾����\V3.0.0_Build%version%.CGLive_Alpha
d:

rmdir /S /Q m:\bin64\temp
rmdir /S /Q m:\bin64\log

xcopy M:\bin64 d: /E /C /D /R /Y /EXCLUDE:D:\��Ļ�汾����\copyfilter.txt
call makerelease.bat
cd d:\D:\��Ļ�汾����


copy D:\��Ļ�汾����\\ServerConfig.ini D:\��Ļ�汾����\V3.0.0_Build%version%.CGLive_Alpha\

xcopy D:\��Ļ�汾����\profile D:\��Ļ�汾����\V3.0.0_Build%version%.CGLive_Alpha\ /E /C /D /R /Y 

start D:\��Ļ�汾����\V3.0.0_Build%version%.CGLive_Alpha

set /p bAdd=�Ƿ��Զ���ӵ����У�y/n��?
if bAdd==y c:git add D:\��Ļ�汾����\V3.0.0_Build%version%.CGLive_Alpha

c:
cd \tool
echo %version%| CGLive3.0_��������������.bat
pause
