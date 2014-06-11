
set e1=0

call "%VS100COMNTOOLS%vsvars32.bat"

devenv D:\dayang2.4ForLoader2010\dayang\dyxcg\xcg\MTPrjFileLoader2010.sln /build "Unicode_ReleaseD" 
if errorlevel 1 set e1=1
devenv D:\dayang2.4ForLoader2010\dayang\dyxcg\xcg\MTPrjFileLoader2010.sln /build "Unicode_Debug" 
if errorlevel 1 set e1=1

if et==1 echo "±‡“Î¥ÌŒÛ£°*******************" else echo "±‡“Î≥…π¶£°*******************"


C:\"Program Files (x86)"\"Beyond Compare 3\"BCompare.exe "D:\dayang2.4ForLoader2010\dayang\dyxcg\xcg\Bin" "M:\bin64\plug_in\PRJFileLoad"
pause

