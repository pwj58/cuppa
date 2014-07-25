
#          Copyright Jamie Allsop 2011-2014
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

#-------------------------------------------------------------------------------
#   GCC Toolchain
#-------------------------------------------------------------------------------

import SCons.Script

from subprocess import Popen, PIPE
from string import strip, replace
import re
import os.path
from exceptions import Exception

import modules.registration

from cpp.create_version_file_cpp import CreateVersionHeaderCpp, CreateVersionFileCpp
from cpp.run_boost_test import RunBoostTestEmitter, RunBoostTest
from cpp.run_process_test import RunProcessTestEmitter, RunProcessTest
from cpp.run_gcov_coverage import RunGcovCoverageEmitter, RunGcovCoverage


class GccException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)


class Gcc:

    @classmethod
    def add_options( cls ):
        pass


    @classmethod
    def add_to_env( cls, args ):
        args['env']['toolchains']['gcc34'] = cls( 'gcc34' )
        args['env']['toolchains']['gcc40'] = cls( 'gcc40' )
        args['env']['toolchains']['gcc41'] = cls( 'gcc41' )
        args['env']['toolchains']['gcc42'] = cls( 'gcc42' )
        args['env']['toolchains']['gcc43'] = cls( 'gcc43' )
        args['env']['toolchains']['gcc44'] = cls( 'gcc44' )
        args['env']['toolchains']['gcc45'] = cls( 'gcc45' )
        args['env']['toolchains']['gcc46'] = cls( 'gcc46' )
        args['env']['toolchains']['gcc47'] = cls( 'gcc47' )
        args['env']['toolchains']['gcc48'] = cls( 'gcc48' )
        args['env']['toolchains']['gcc49'] = cls( 'gcc49' )


    @classmethod
    def default_variants( cls ):
        return [ 'dbg', 'rel' ]


    def __init__( self, toolchain ):
        self.values = {}

        self.values['name'] = toolchain

        if toolchain == 'gcc34':
            self.__get_gcc34_toolchain( toolchain )

        elif toolchain == 'gcc40':
            self.__get_gcc40_toolchain( toolchain )

        elif toolchain == 'gcc41':
            self.__get_gcc41_toolchain( toolchain )

        elif toolchain == 'gcc42':
            self.__get_gcc42_toolchain( toolchain )

        elif toolchain == 'gcc43':
            self.__get_gcc43_toolchain( toolchain )

        elif toolchain == 'gcc44':
            self.__get_gcc44_toolchain( toolchain )

        elif toolchain == 'gcc45':
            self.__get_gcc45_toolchain( toolchain )

        elif toolchain == 'gcc46':
            self.__get_gcc46_toolchain( toolchain )

        elif toolchain == 'gcc47':
            self.__get_gcc47_toolchain( toolchain )

        elif toolchain == 'gcc48':
            self.__get_gcc48_toolchain( toolchain )

        elif toolchain == 'gcc49':
            self.__get_gcc49_toolchain( toolchain )

        else:
            raise GccException("GCC toolchain [" + toolchain + "] not supported." )

        gcc_version = Popen(["gcc", "--version"], stdout=PIPE).communicate()[0]
        default_gcc = 'gcc' + re.search( r'(\d)\.(\d)', gcc_version ).expand(r'\1\2')

        self.values['CXX'] = 'g++'
        self.values['CC']  = 'gcc'

        if toolchain != default_gcc:
            major = toolchain[3:4]
            minor = toolchain[4:]

            self.values['CXX'] = 'g++-' + major + '.' + minor
            self.values['CC']  = 'gcc-' + major + '.' + minor

#            if not os.path.exists( self.values['CXX'] ):
#                self.values['CXX'] = 'g++' + major + minor
#                self.values['CC']  = 'gcc' + major + minor

        env = SCons.Script.DefaultEnvironment()

        SYSINCPATHS = '${_concat(\"' + self.values['sys_inc_prefix'] + '\", SYSINCPATH, \"'+ self.values['sys_inc_suffix'] + '\", __env__, RDirs, TARGET, SOURCE)}'

        self.values['_CPPINCFLAGS'] = '$( ' + SYSINCPATHS + ' ${_concat(INCPREFIX, INCPATH, INCSUFFIX, __env__, RDirs, TARGET, SOURCE)} $)'

        STATICLIBFLAGS  = self.values['static_link']   + ' ' + re.search( r'(.*)(,\s*LIBS\s*,)(.*)', env['_LIBFLAGS'] ).expand( r'\1, STATICLIBS,\3' )
        DYNAMICLIBFLAGS = self.values['dynamic_link']  + ' ' + re.search( r'(.*)(,\s*LIBS\s*,)(.*)', env['_LIBFLAGS'] ).expand( r'\1, DYNAMICLIBS,\3' )

        self.values['_LIBFLAGS'] = STATICLIBFLAGS + ' ' + DYNAMICLIBFLAGS


    def __getitem__( self, key ):
        return self.values.get( key )


    def name( self ):
        return self.values['name']


    def initialise_env( self, env ):
        env['CXX']          = self.values['CXX']
        env['CC']           = self.values['CC']
        env['_CPPINCFLAGS'] = self.values['_CPPINCFLAGS']
        env['_LIBFLAGS']    = self.values['_LIBFLAGS']
        env['SYSINCPATH']   = []
        env['INCPATH']      = [ '#.', '.' ]
        env['LIBPATH']      = []
        env['CPPDEFINES']   = []
        env['LIBS']         = []
        env['STATICLIBS']   = []
        env['DYNAMICLIBS']  = self.values['dynamic_libraries']
        env.AppendUnique( LINKFLAGS = self.values['link_cxx_flags'] )


    def variants( self ):
        pass


    def supports_coverage( self ):
        return 'coverage_cxx_flags' in self.values


    def version_file_builder( self, env, namespace, version, location ):
        return CreateVersionFileCpp( env, namespace, version, location )


    def version_file_emitter( self, env, namespace, version, location ):
        return CreateVersionHeaderCpp( env, namespace, version, location )


    def test_runner( self, tester, final_dir, expected ):
        if not tester or tester =='process':
            return RunProcessTest( expected ), RunProcessTestEmitter( final_dir )
        elif tester=='boost':
            return RunBoostTest( expected ), RunBoostTestEmitter( final_dir )


    def test_runners( self ):
        return [ 'process', 'boost' ]


    def coverage_runner( self, program, final_dir ):
        return RunGcovCoverageEmitter( program, final_dir ), RunGcovCoverage( program, final_dir )


    def __get_gcc34_toolchain( self, toolchain ):
        self.__get_gcc_toolchain( toolchain )


    def __get_gcc40_toolchain( self, toolchain ):
        self.__get_gcc_toolchain( toolchain )


    def __get_gcc41_toolchain( self, toolchain ):
        self.__get_gcc_toolchain( toolchain )


    def __get_gcc42_toolchain( self, toolchain ):
        self.__get_gcc_toolchain( toolchain )


    def __get_gcc43_toolchain( self, toolchain ):
        self.__get_gcc_toolchain( toolchain )


    def __get_gcc44_toolchain( self, toolchain ):
        self.__get_gcc_toolchain( toolchain )


    def __get_gcc45_toolchain( self, toolchain ):
        self.__get_gcc_toolchain( toolchain )


    def __get_gcc46_toolchain( self, toolchain ):
        self.__get_gcc_toolchain( toolchain )


    def __get_gcc47_toolchain( self, toolchain ):
        self.__get_gcc_toolchain( toolchain )


    def __get_gcc48_toolchain( self, toolchain ):
        self.__get_gcc_toolchain( toolchain )


    def __get_gcc49_toolchain( self, toolchain ):
        self.__get_gcc_toolchain( toolchain )


    def __get_gcc_toolchain( self, toolchain ):
        if toolchain == 'gcc34':
            self.values['sys_inc_prefix']  = '-I'
        else:
            self.values['sys_inc_prefix']  = '-isystem'

        self.values['sys_inc_suffix']  = ''
        self.values['static_link']     = '-Xlinker -Bstatic'
        self.values['dynamic_link']    = '-Xlinker -Bdynamic'

        CommonCxxFlags = [ '-Wall', '-fexceptions', '-g' ]
        CommonCFlags   = [ '-Wall', '-g' ]

        if re.match( 'gcc4[3-6]', toolchain ):
            CommonCxxFlags += [ '-std=c++0x' ]
        elif re.match( 'gcc47', toolchain ):
            CommonCxxFlags += [ '-std=c++11' ]
        elif re.match( 'gcc4[8-9]', toolchain ):
            CommonCxxFlags += [ '-std=c++1y' ]

        self.values['debug_cxx_flags']    = CommonCxxFlags + []
        self.values['release_cxx_flags']  = CommonCxxFlags + [ '-O3', '-DNDEBUG' ]
        self.values['coverage_cxx_flags'] = CommonCxxFlags + [ '-fprofile-arcs', '-ftest-coverage' ]
        self.values['coverage_libs']      = [ 'gcov' ]

        self.values['debug_c_flags']      = CommonCFlags + []
        self.values['release_c_flags']    = CommonCFlags + [ '-O3', '-DNDEBUG' ]
        self.values['coverage_c_flags']   = CommonCFlags + [ '-fprofile-arcs', '-ftest-coverage' ]

        LinkCxxFlags = ['-rdynamic', '-Wl,-rpath=.' ]
        self.values['link_cxx_flags'] = LinkCxxFlags

        DynamicLibraries = [ 'pthread', 'rt' ]
        self.values['dynamic_libraries'] = DynamicLibraries


    def __get_gcc_coverage( self, object_dir, source ):
        # -l = --long-file-names
        # -p = --preserve-paths
        # -b = --branch-probabilities
        return 'gcov -o ' + object_dir \
               + ' -l -p -b ' \
               + source + ' > ' + source + '_summary.gcov'


    def build_flags_for( self, library ):
        if library == 'boost':
            if re.match( 'gcc4[3-6]', self.values['name'] ):
                return 'cxxflags="-std=c++0x"'
            elif re.match( 'gcc47', self.values['name'] ):
                return 'cxxflags="-std=c++11"'
            elif re.match( 'gcc4[8-9]', self.values['name'] ):
                return 'cxxflags="-std=c++1y"'


    @classmethod
    def output_interpretors( cls ):
        return [
        {
            'title'     : "Fatal Error",
            'regex'     : r"(FATAL:[ \t]*(.*))",
            'meaning'   : 'error',
            'highlight' : set( [ 1 ] ),
            'display'   : [ 1 ],
            'file'      : None,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "In File Included From",
            'regex'     : r"(In file included\s+|\s+)(from\s+)([][{}() \t#%$~\w&_:+/\.-]+)(:([0-9]+)(:[0-9]+)?)([,:])",
            'meaning'   : 'info',
            'highlight' : set( [ 1, 3, 4 ] ),
            'display'   : [ 1, 2, 3, 4, 7 ],
            'file'      : 3,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "In Function Info",
            'regex'     : r"([][{}() \t#%$~\w&_:+/\.-]+)(:[ \t]+([iI]n ([cC]lass|[cC]onstructor|[dD]estructor|[fF]unction|[mM]ember [fF]unction|[sS]tatic [fF]unction|[sS]tatic [mM]ember [fF]unction).*))",
            'meaning'   : 'info',
            'highlight' : set( [ 1 ] ),
            'display'   : [ 1, 2 ],
            'file'      : 1,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Skipping Instantiation Contexts 2",
            'regex'     : r"([][{}() \t#%$~\w&_:+/\.-]+)(:([0-9]+):[0-9]+)(:[ \t]+(\[[ \t]+[Ss]kipping [0-9]+ instantiation contexts[, \t]+.*\]))",
            'meaning'   : 'info',
            'highlight' : set( [ 1, 2 ] ),
            'display'   : [ 1, 2, 4 ],
            'file'      : 1,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Skipping Instantiation Contexts",
            'regex'     : r"([][{}() \t#%$~\w&_:+/\.-]+)(:([0-9]+))(:[ \t]+(\[[ \t]+[Ss]kipping [0-9]+ instantiation contexts[ \t]+\]))",
            'meaning'   : 'info',
            'highlight' : set( [ 1, 2 ] ),
            'display'   : [ 1, 2, 4 ],
            'file'      : 2,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Instantiated From",
            'regex'     : r"([][{}() \t#%$~\w&_:+/\.-]+)(:([0-9]+))(:[ \t]+([iI]nstantiated from .*))",
            'meaning'   : 'info',
            'highlight' : set( [ 1, 2] ),
            'display'   : [ 1, 2, 4 ],
            'file'      : 1,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Instantiation of",
            'regex'     : r"([][{}() \t#%$~\w&_:+/\.-]+)(:[ \t]+(In instantiation of .*))",
            'meaning'   : 'info',
            'highlight' : set( [ 1 ] ),
            'display'   : [ 1, 2 ],
            'file'      : 1,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Required From",
            'regex'     : r"([][{}() \t#%$~\w&_:+/\.-]+)(:([0-9]+):[0-9]+)(:[ \t]+required from .*)",
            'meaning'   : 'info',
            'highlight' : set( [ 1, 2 ] ),
            'display'   : [ 1, 2, 4 ],
            'file'      : 1,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Compiler Warning 2",
            'regex'     : r"([][{}() \t#%$~\w&_:+/\.-]+)(:([0-9]+):([0-9]+))(:[ \t]([Ww]arning:[ \t].*))",
            'meaning'   : 'warning',
            'highlight' : set( [ 1, 2 ] ),
            'display'   : [ 1, 2, 5 ],
            'file'      : 1,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Compiler Note 2",
            'regex'     : r"([][{}() \t#%$~\w&_:+/\.-]+)(:([0-9]+):[0-9]+)(:[ \t]([Nn]ote:[ \t].*))",
            'meaning'   : 'info',
            'highlight' : set( [ 1, 2 ] ),
            'display'   : [ 1, 2, 4 ],
            'file'      : 1,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Compiler Note",
            'regex'     : r"([][{}() \t#%$~\w&_:+/\.-]+)(:([0-9]+))(:[ \t]([Nn]ote:[ \t].*))",
            'meaning'   : 'info',
            'highlight' : set( [ 1, 2 ] ),
            'display'   : [ 1, 2, 4 ],
            'file'      : 1,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "General Note",
            'regex'     : r"([Nn]ote:[ \t].*)",
            'meaning'   : 'info',
            'highlight' : set( [ 1 ] ),
            'display'   : [ 1 ],
            'file'      : None,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Compiler Error 2",
            'regex'     : r"([][{}() \t#%$~\w&_:+/\.-]+)(:([0-9]+):[0-9]+)(:[ \t](.*))",
            'meaning'   : 'error',
            'highlight' : set( [ 1, 2 ] ),
            'display'   : [ 1, 2, 4 ],
            'file'      : 1,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Compiler Warning",
            'regex'     : r"([][{}() \t#%$~\w&_:+/\.-]+)(:([0-9]+))(:[ \t]([Ww]arning:[ \t].*))",
            'meaning'   : 'warning',
            'highlight' : set( [ 1 ] ),
            'display'   : [ 1, 2, 4 ],
            'file'      : 1,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Undefined Reference 2",
            'regex'     : r"([][{}() \t#%$~\w&_:+/\.-]+\.o:([][{}() \t#%$~\w&_:+/\.-]+):([0-9]+))(:[ \t](undefined reference.*))",
            'meaning'   : 'warning',
            'highlight' : set( [ 1 ] ),
            'display'   : [ 1, 4 ],
            'file'      : 2,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Compiler Error",
            'regex'     : r"([][{}() \t#%$~\w&_:+/\.-]+)(:([0-9]+))(:[ \t](.*))",
            'meaning'   : 'error',
            'highlight' : set( [ 1, 2 ] ),
            'display'   : [ 1, 2, 4 ],
            'file'      : 1,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Linker Warning",
            'regex'     : r"([][{}() \t#%$~\w&_:+/\.-]+)(:\(\.text\+[0-9a-fA-FxX]+\))(:[ \t]([Ww]arning:[ \t].*))",
            'meaning'   : 'warning',
            'highlight' : set( [ 1, 2 ] ),
            'display'   : [ 1, 2, 4 ],
            'file'      : 1,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Linker Error",
            'regex'     : r"([][{}() \t#%$~\w&_:+/\.-]+)(:([0-9]+):[0-9]+)(:[ \t](.*))",
            'meaning'   : 'error',
            'highlight' : set( [ 1, 2 ] ),
            'display'   : [ 1, 2, 4 ],
            'file'      : 1,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Linker Error 2",
            'regex'     : r"([][{}() \t#%$~\w&_:+/\.-]+\(.text\+[0-9A-Za-z]+\):([ \tA-Za-z0-9_:+/\.-]+))(:[ \t](.*))",
            'meaning'   : 'error',
            'highlight' : set( [ 1 ] ),
            'display'   : [ 1, 4 ],
            'file'      : 1,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Linker Error 3",
            'regex'     : r"(([][{}() \t#%$~\w&_:+/\.-]+):\(\.text\+[0-9a-fA-FxX]+\))(:(.*))",
            'meaning'   : 'error',
            'highlight' : set( [ 1 ] ),
            'display'   : [ 1, 4 ],
            'file'      : 2,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Linker Error - lib not found",
            'regex'     : r"(.*(ld.*):[ \t](cannot find.*))",
            'meaning'   : 'error',
            'highlight' : set( [ 1 ] ),
            'display'   : [ 1 ],
            'file'      : None,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Linker Error - cannot open output file",
            'regex'     : r"(.*(ld.*):[ \t](cannot open output file.*))(:[ \t](.*))",
            'meaning'   : 'error',
            'highlight' : set( [ 1 ] ),
            'display'   : [ 1, 4 ],
            'file'      : None,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Linker Error - unrecognized option",
            'regex'     : r"(.*(ld.*))(:[ \t](unrecognized option.*))",
            'meaning'   : 'error',
            'highlight' : set( [ 1 ] ),
            'display'   : [ 1, 3 ],
            'file'      : None,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "No such File or Directory",
            'regex'     : r"(.*:(.*))(:[ \t](No such file or directory.*))",
            'meaning'   : 'error',
            'highlight' : set( [ 1 ] ),
            'display'   : [ 1, 3 ],
            'file'      : None,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Undefined Reference",
            'regex'     : r"([][{}() \t#%$~\w&_:+/\.-]+)(:[ \t](undefined reference.*))",
            'meaning'   : 'error',
            'highlight' : set( [ 1 ] ),
            'display'   : [ 1, 2 ],
            'file'      : None,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "General Warning",
            'regex'     : r"([Ww]arning:[ \t].*)",
            'meaning'   : 'warning',
            'highlight' : set( [ 1 ] ),
            'display'   : [ 1 ],
            'file'      : None,
            'line'      : None,
            'column'    : None,
        },
        {
            'title'     : "Auto-Import Info",
            'regex'     : r"(([Ii]nfo:[ \t].*)\(auto-import\))",
            'meaning'   : 'info',
            'highlight' : set( [ 1 ] ),
            'display'   : [ 1 ],
            'file'      : None,
            'line'      : None,
            'column'    : None,
        },
    ]
