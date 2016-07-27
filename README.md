# clicombine
CLI-Combine is a command-line tool to do quick and dirty image combination for ALMA data.  It hooks in with [CASA](https://casaguides.nrao.edu/) or can be used to generate CASA scripts to be run later.  The current functionality is fairly limited, but the tool simplifies the process of making an initial pass at a combined image.

## Requirements and Installation
CLI-Combine should work on mac or on other unix flavored systems.  It has not been tested on Windows.  

### Requirements
* Casa
* Python
* drivecasa (install via pip)

### Installation
CLI-Combine is available on [PyPi](https://pypi.python.org/pypi/clicombine/0.1.113).  It is installable via pip.
~~~~bash
$ pip install clicombine
~~~~
This will also automatically install drivecasa.
To test the installation, try
~~~~
$ cli-combine --help
usage: cli-combine [-h] [-v] [-o] [-r] [-g | -e | -n | -c] [input_fname]

positional arguments:
  input_fname      The name of your configuration file.

optional arguments:
  -h, --help       show this help message and exit
  -v, --verbose    Increase output verbosity. Log to stderr.
  -o, --overwrite  Overwrite old combined images and create new ones with the
                   same filename.
  -r, --raw        Disable error checking of the configuration file which
                   allows you to pass arbitrary input to the clean task. Only
                   use this option if you know what you're doing.
  -g, --generate   Generate CASA code and write to a file.
  -e, --example    Create an example config file.
  -n, --new        Create an empty config file.
  -c, --combine    Combine images as specified in the config file. Default to
                   true.
~~~~

## Basic Usage
You should run cli-combine in a directory with the data sets you want to combine.  To create a new empty configuration file,
run
~~~
$ cli-combine --new [project_name]
~~~
Then go ahead and edit the configuration file.
~~~
$ [my_favorite_editor] [project_name].json
~~~
You can tell cli-combine to run combination scripts in a casa environment by running
~~~
$ cli-combine --combine [project_name]
~~~
Or you can generate scripts to use later by running
~~~
$ cli-combine --generate [project_name]
~~~

## Detailed Documentation
Todo
