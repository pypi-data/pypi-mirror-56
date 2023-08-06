# blister

Conventions-over-configuration C++/modules project manager.

This is a simple approach to deal with C++ modules. By using a bunch of
conventions, this Python module scans for all files and generates a
`build.ninja` to compile the code.

Currently, it is personal endeavor to use C++ modules with some dependency
management, which (as of 2019) is not provided by existing building systems.
Hacks and non-sense may be included.

Requires a folder structure like this:

* root
  * includes
    * h-files and subfolders
  * sources
    * common
      * cppm-files and subfolders
    * osx-metal
      * cppm-files
      * mm-files
    * ...
  * tests
    * app-folder-1
      * cppm-files
      * cpp-files
    * app-folder-2
    * ...
  * tools
    * cpp-files
  * unit-tests
    * cpp-files
  * bli.yaml

`includes` is added as part of the include path.

`sources/common` contains CPP modules (using `cppm` as extension). They will
be scanned, with all `cppm` files added to the build. The module name is
independent of the file name, being extracted from the `export module`
statement.

`sources/osx-metal` is a hack to build Apple-compatible folders. It also
compiles `metal` files.

`tests` creates one standalone application per folder. Every linked application
will contains all objects from `sources` folders.

`unit-tests` are compiled independently and liked with `sources/common` objects
and run as part of the `test` target.

Dependencies are calculated from both `cppm` and `cpp` files, by parsing the
`import` statements.

`bli.yaml` identifies the root folder and contains configuration to override
global and per-file flags.
