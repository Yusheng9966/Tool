echo off
set e1=0

subst n: /d
subst n: d:\dayang1.8

if errorlevel 1 ( echo "����ӳ�����"
pause
exit )


call "%VS80COMNTOOLS%vsvars32.bat"



cd C:\"Program Files (x86)"\Git\bin 
cd N:\dayang\dyxcg\xcg
n:

echo "����س���ʾSVN�汾��"
c:git svn log -1
set /p version=������SVN�汾��:

rem ����

:loop1
vcbuild N:\dayang\dyxcg\xcg\Src\XCGSolution\XCG3DSolution_for_30.sln "Unicode_Release|x64" 
if errorlevel 1 goto loop1

:loop2
vcbuild N:\dayang\dyxcg\xcg\SrcPlug_In\XCGPlugInSolution\XCGPlugInSolution_for_30.sln "Unicode_Release|x64" 
if errorlevel 1 goto loop2

echo "����ɹ���*******************"

md D:\��Ļ�汾����\Build%version%.CGNews_Alpha
cd D:\��Ļ�汾����\Build%version%.CGNews_Alpha



d:
md d:Bin
md d:Plug_In
md d:Sys

xcopy N:\dayang\dyxcg\xcg\Bin d:Bin /E /C /D /R /Y /EXCLUDE:D:\��Ļ�汾����\copyfilter.txt
xcopy N:\dayang\dyxcg\xcg\Plug_In d:Plug_In /E /C /D /R /Y /EXCLUDE:D:\��Ļ�汾����\copyfilter.txt
xcopy N:\dayang\dyxcg\xcg\Sys d:Sys /E /C /D /R /Y /EXCLUDE:D:\��Ļ�汾����\copyfilter.txt
xcopy N:\dayang\dyxcg\xcg\makerelease.bat d: /C /D /Y /EXCLUDE:D:\��Ļ�汾����\copyfilter.txt




call makerelease.bat

start D:\��Ļ�汾����\Build%version%.CGNews_Alpha

::**********************************���������******************************************
start C:\Application\dependes\depends.exe "D:\��Ļ�汾����\Build%version%.CGNews_Alpha\Bin\D3-CG-NewsReportU.exe"


pause
