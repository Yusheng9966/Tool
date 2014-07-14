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

def _do_buildcommand( a ):
        p = subprocess.Popen( a, stdout=subprocess.PIPE)
        listError = []
        while True:
                l = p.stdout.readline()
                if l=="":
                        break
                print l
                err = re.findall("error", l )
                if len(err) > 0 :
                        listError = listError + [l]
        return listError



def build_solution80( solution, configure = "Release", platform = "x64", rebuild = False ):
        a = [msvc.find_exe("vcbuild.exe"),
                        solution,
                        "%s|%s"%( configure, platform )
                        ]
        listError = _do_buildcommand(a)
        return listError


def build_solution100( solution, configure = "Release", platform = "x64", rebuild = False  ):
        a = [msvc.find_exe("msbuild.exe"),
                        "/m:8",
                        "/V:q",
                        "/property:WarningLevel=0;Configuration=%s;Platform=%s"%( configure, platform ),
                        solution
                        ]
        if rebuild:
                b =  [msvc.find_exe("msbuild.exe"),
                                "/t:clean",
                        "/property:WarningLevel=0;Configuration=%s;Platform=%s"%( configure, platform ),
                        solution
                        ]
                listError = _do_buildcommand(b)

        listError = _do_buildcommand(a)

        return listError


def init_vcbuild( version, x64 = True ):
        """init_vcbuild初始化vc的编译环境 version = 8.0 或者 10.0 x64=True或者False"""
        global msvc
        distutils.msvc9compiler.VERSION = version
        msvc = distutils.msvc9compiler.MSVCCompiler()
        if( x64 ):
                msvc.initialize("win-amd64")
        else:
                msvc.initialize("win32")
        if( version < 10.0 ):
                return build_solution80
        else:
                return build_solution100


def output_err_info( errs ):
        """输出错误信息，红色"""
        windll.Kernel32.GetStdHandle.restype = c_ulong
        h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))
        windll.Kernel32.SetConsoleTextAttribute(h, 12)
        for l in errs:
                print l 
        windll.Kernel32.SetConsoleTextAttribute(h, 15)

def build_solution( builder, solution, configure, platform, retry_count=1, rebuild = False ):
        while retry_count:
                listError = builder( solution, configure,platform, rebuild )
                if( len(listError) == 0 ):
                        break;

                rebuild = False
                listError = ["build solution %s, error count = %d" % ( solution, len(listError)), 
                                "-"*80] + listError + ["solution %s" % solution ]
                output_err_info(listError)

                if retry_count == 1:
                        answer = raw_input("input to build again(y/n)?...")
                        if answer != 'y':
                                break;
                        retry_count = 10
                else:
                        retry_count = retry_count - 1

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

def get_ignore_fromfile( filename ):
        '''
        从一个文本文件读过滤文件名。每行是一个过滤项，支持*和?为通配符
        '''
        f = open( filename )
        a = f.readlines()
        ignore = [l.strip('\n').strip() for l in a ]
        return ignore

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









