from distutils.core import setup, Extension

keyword_list = [
    'finance',
    'stocks',
    'modeling',
    'stock market',
    'ML'
]

classifers_list = [
    'Development Status :: 2 - Pre-Alpha',
    'Operating System :: MacOS',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: Unix'
]

module1 = Extension('_royal',
                    define_macros = [('USE_PRINTER', '1')],
                    include_dirs = ['include'],
                    sources = ['src/pymain.c'])

setup (name = 'royal',
       version = '0.0.2',
       description = 'A financial market modeling library',
       author = 'Joshua Weinstein',
       author_email = 'jweinst1@berkeley.edu',
       url = 'https://github.com/jweinst1/Royal',
       long_description = open('README.md').read(),
       license = "MIT",
       keyowrds = keyword_list,
       classifiers = classifers_list,
       packages = ["royal"],
       ext_modules = [module1])