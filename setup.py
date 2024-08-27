from setuptools import setup, Extension
import subprocess
import os
import sys
import platform
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = [
            f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}', 
            f'-DPYTHON_EXECUTABLE={sys.executable}',
            '-Dpybind11_DIR=' + os.path.join(sys.prefix, 'lib', 'python3.12', 'site-packages', 'pybind11', 'share', 'cmake', 'pybind11'),
        ]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += [f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE={extdir}']
            build_args += ['--', '/m']
        else:
            build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)


setup(
    name='html_generator',
    version='0.1',
    author='Your Name',
    author_email='your.email@example.com',
    description='HTML Generator using C++ and Pybind11',
    long_description='',
    ext_modules=[CMakeExtension('html_generator', 'bind_cpp/src/cpp')],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
)
