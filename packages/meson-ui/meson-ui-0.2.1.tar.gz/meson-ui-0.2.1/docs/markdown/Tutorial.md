---
short-description: Simplest tutorial
...

# Tutorial

This page shows from the ground up how to create a Meson build
project.

To make it easier for new developers to start working, Meson ships
a tool to generate the basic setup of different kinds of projects.
This functionality can be accessed with the meson init command. A
typical project setup would go like this:

```console
mkdir project_name
cd project_name
meson init --language=c --name=demo --version=0.1
```

The humble beginning
-----

Let's start with the most basic of programs, the classic hello
example. First we create a file `main.c` which holds the source. It
looks like this.

```c
#include <stdio.h>

#define PROJECT_NAME "demo"

int main(int argc, char **argv) {
    if(argc != 1) {
        printf("%s takes no arguments.\n", argv[0]);
        return 1;
    }
    printf("This is project %s.\n", PROJECT_NAME);
    return 0;
}
```

```meson
project('demo', 'c',
  version : '0.1',
  default_options : ['warning_level=3'])

exe = executable('demo', 'demo.c',
  install : true)

test('basic', exe)
```

That is all. We are now ready to build our application. First we need
to initialize the build by going into the source directory and issuing
the following commands.

```console
$ meson builddir
```

If you launched the app from the command line, you will see the 
application.  It looks somthing like this.

![tutorial](images/tutorial-1.png)

Now to use **Meson-ui** for a simple build.  First enter the 
paths for source and build directory to your Meson project 
or click on open directory button with the pickture of a folder
on the lower right of the user interface.

Meson is different from some other build systems in that it
does not permit in-source builds. You must always create a separate build directory. Common convention is to put the default build directory in a subdirectory of your top level source directory.

![tutorial](images/tutorial-2.png)

Now we are ready to build our code.  Just click **Build** to build the project.

![tutorial](images/tutorial-3.png)

Optionally you can run the test for the project by clicking **test** button.

![tutorial](images/tutorial-4.png)

And assuming you navigated to your project root directory you 
can run the resulting binary from the command line.

```

Once that is done we can run the resulting binary.

```console
$ ./demo
```

This produces the expected output.

    This is project demo.
