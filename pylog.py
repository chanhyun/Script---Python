from distutils.core import setup,Extension

setup(name="spam",
        version="1.0",
      description="print log",
      author="Chanhyun",
      ext_modules=[Extension("spam",["spam.c"])]
      )
