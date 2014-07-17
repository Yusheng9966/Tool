# -*- coding: utf-8 -*-
import distutils.msvc9compiler
import re,subprocess
import fnmatch
import os
from ctypes import *
from shutil import *

msvc = ""

""" git路径 """
gitpath = "C:\\Program Files (x86)\\Git\\bin\\git"

def _do_buildcommand( a, pretty = "" ):
        p = subprocess.Popen( a, stdout=subprocess.PIPE)
        listError = []
        while True:
                l = p.stdout.readline()
                if l=="":
                        break

                if pretty == "":
                        print l

                err = re.findall("error", l )
                if len(err) > 0 :
                        listError = listError + [l]
        return listError



def _build_solution80( solution, configure = "Release", platform = "x64", rebuild = False, clear = False, pretty = "" ):
        a = [msvc.find_exe("vcbuild.exe"),
                        solution,
                        "%s|%s"%( configure, platform )
                        ]
        listError = _do_buildcommand(a,  pretty )
        return listError


def _build_solution100( solution, configure = "Release", platform = "x64", rebuild = False, clear = False, pretty = ""  ):
        """
        pretty可以为空，"none"代表是否有编译输出
        """
        a = [msvc.find_exe("msbuild.exe"),
                        "/m:8",
                        "/V:q",
                        "/property:WarningLevel=0;Configuration=%s;Platform=%s"%( configure, platform ),
                        solution
                        ]
        if rebuild or clear:
                b =  [msvc.find_exe("msbuild.exe"),
                                "/t:clean",
                        "/property:WarningLevel=0;Configuration=%s;Platform=%s"%( configure, platform ),
                        solution
                        ]
                listError = _do_buildcommand(b, pretty)
                if clear:
                        return listError

        listError = _do_buildcommand(a, pretty)

        return listError


def init_vcbuild( version, x64 = True ):
        """
        init_vcbuild初始化vc的编译环境 version = 8.0 或者 10.0 x64=True或者False
        """
        global msvc
        distutils.msvc9compiler.VERSION = version
        msvc = distutils.msvc9compiler.MSVCCompiler()
        if( x64 ):
                msvc.initialize("win-amd64")
        else:
                msvc.initialize("win32")
        if( version < 10.0 ):
                return _build_solution80
        else:
                return _build_solution100


ouputWhite = 15
outputRed = 12
outputGreen = 10
outputYellow = 14

def _output_info( info, color= 15 ):
        """输出信息，红色"""
        windll.Kernel32.GetStdHandle.restype = c_ulong
        h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))
        windll.Kernel32.SetConsoleTextAttribute(h, color)
        for l in info:
                print l 
        windll.Kernel32.SetConsoleTextAttribute(h, 15)

def build_solution( builder, solution, configure, platform, retry_count=1, rebuild = False ):
        '''
        build_solution编译工程或者解决方案
        '''
        while retry_count:
                listError = builder( solution, configure,platform, rebuild )
                if( len(listError) == 0 ):
                        break;

                rebuild = False
                listError = ["build solution %s, error count = %d" % ( solution, len(listError)), 
                                "-"*80] + listError + ["solution %s" % solution ]
                _output_info(listError, color = outputRed )

                if retry_count == 1:
                        answer = raw_input("input to build again(y/n)?...")
                        if answer != 'y':
                                break;
                        retry_count = 10
                else:
                        retry_count = retry_count - 1

                        
def test_build_dependenc_order( builder, prj_info,  clear = True,pretty = "none" ):
        '''
        测试工程编译的依赖项，输入工程文件名，进行依赖测试，返回能够正确编译的工程顺序
        '''

        #所有的工程清理
        if clear:
                for info in prj_info:
                        name,configure, platform = info
                        builder( name, configure, platform, clear = True )

        prj_output = []
        prj_set = set()
        max = int((len(prj_info)+1)*len(prj_info) * 0.5)
        for i in range(0,max):
                find = False
                for info in prj_info:
                        name,configure, platform = info
                        if name+configure+platform in prj_set:
                                continue
                        listError = builder( name, configure, platform, rebuild = False, pretty = pretty)
                        if len(listError)>0:
                                listError = builder( name, configure, platform, rebuild = False, pretty = pretty)
                        if len(listError)<=0:
                                prj_output.append( (name, configure, platform ))
                                prj_set.add( name+configure+platform )
                                _output_info( ["Test Build %s Success...."%name], outputGreen )
                                find = True
                        else:
                                _output_info( ["Test Build %s Failed...."%name], outputRed )
                if not find:
                        break;

        errorprj = []
        for info in prj_info:
                name,configure, platform = info
                if name+configure+platform in prj_set:
                        continue
                errorprj.append(info)

        return prj_output,errorprj

def get_buildproject_fromfile( filename ):
        '''
        从文本文件读取工程文件。每行包含工程名，configure, platform
        '''
        f = open( filename )
        a = f.readlines()
        prj_info = []
        for l in a:
                if l[0]=='-':
                        continue
                ll = l.strip('\n').split(',')
                if len(ll)>2:
                        prj_info.append( tuple( [t.strip() for t in ll] ))

        f.close();
        return prj_info;
                
def build_prj_list( builder, prjlistfile, outputlistfile,  clear = True ):
        '''
        读取prjlistfile中的工程，一行一行的编译，将编译成功的工程顺序输出到outputlistfile
        '''
        prjinfo = get_buildproject_fromfile( prjlistfile )
        for info in prjinfo:
                print "%s,%s,%s"%info

        prj, errorprj = test_build_dependenc_order( builder, prjinfo, clear = clear )

        f = open(outputlistfile, "w")

        for info in prj:
                name,configure, platform = info
                print name
                f.write("%s,%s,%s\n"%info)

        while len(errorprj) > 0 :
                print "-"*80
                for info in errorprj:
                        name,configure, platform = info
                        print "Error %s,%s,%s"% info
                answer = raw_input("input to build again(y/n)?...")
                if answer != 'y':
                        break;

                prj, errorprj = test_build_dependenc_order( builder, errorprj, clear, "" )
                for info in prj:
                        name,configure, platform = info
                        print name
                        f.write("%s,%s,%s\n"%info)

        print "-"*80
        for info in errorprj:
                name,configure, platform = info
                print name
                f.write("-%s,%s,%s\n"%info)
        f.close()

                

                

def call_shellcommand( command ):
        a = [command]
        p = subprocess.Popen( a, stdout=subprocess.PIPE, shell = True)
        while True:
                l = p.stdout.readline()
                if l=="":
                        break
                print l
        p.wait()

def _ignore_patterns(patterns = []):
        """Function that can be used as copytree() ignore parameter.
        Patterns is a sequence of glob-style patterns
        that are used to exclude files"""
        def _ignore_patterns(path, names):
                ignored_names = []
                #for pattern in patterns:
                #        print "trans re---:", fnmatch.translate(pattern)
                #raw_input("input ENTER to build again...")

                for name in names:
                        name2 = path + "\\" + name
                        for pattern in patterns:
                                if( fnmatch.fnmatch( name2, pattern )):
                                        ignored_names.extend( [name] )
                                        break;
                s = set(ignored_names)
                for name in names:
                        if( not (name in s) ):
                                print "copy %s\\%s"%(path, name)
                return s
        return _ignore_patterns


def copy_output_direction( src, dest, ignorefile = []):
        '''
        复制输出目录。从src到dest，dest目录不能为根目录，不能已经存在。ignorefile为忽略项
        '''
        rmtree( dest, ignore_errors=True )
        copytree( src, dest, ignore=_ignore_patterns(ignorefile))

def copy_output_file( src, dest ):
        '''
        拷贝文件
        '''
        copy2(src, dest)

def delete_allfiles( path ):
        '''
        删除path目录下的所以文件和目录
        '''
        rmtree( path, ignore_errors = True )
        os.mkdir( path )

        
"""
Git相关工具
"""
def get_svn_rev( path ):
        '''
        获得SVN的版本号 
        '''
        os.chdir(path)
        a = [gitpath, "svn", "log", "-1" ]
        p = subprocess.Popen( a, stdout=subprocess.PIPE)
        #p.stdin.writelines("\n\n")
        #p.stdin.flush()
        rev ="" 
        while True:
                l = p.stdout.readline()
                if l=="":
                        break
                k = l.split("|")
                if len(k)>1:
                        rev=k[0].strip()
                        print k
                print l
        p.wait()
        return rev.strip("r")
        
def git_commit( path, loginfo ):
        '''
        将目录提交到git库
        '''
        os.chdir(path)
        a = [gitpath, "add", "."]
        p = subprocess.Popen( a )
        p.wait()
        a = [gitpath, "commit", "-m", '%s'%loginfo]
        p = subprocess.Popen( a )
        p.wait()





"""
从文件数据读取
"""
def get_ignore_fromfile( filename ):
        '''
        从一个文本文件读过滤文件名。每行是一个过滤项，支持*和?为通配符
        '''
        f = open( filename )
        a = f.readlines()
        ignore = [l.strip('\n').strip() for l in a ]
        f.close();
        return ignore






