# Use of Python

Meson-ui is implemented in Python. This has both positive and negative sides. The main thing people seem to be mindful about is the dependency on Python to build source code. This page discusses various aspects of this problem.

# Dependency hell

There have been many Python programs that are difficult to maintain on multiple platforms. The reasons come mostly from dependencies. The program may use dependencies that are hard to compile on certain platforms, are outdated, conflict with other dependencies, not available on a given Python version and so on.

Meson-ui currently uses PyQt5 as it's only dependency: Meson-ui is not allowed to have more than one dependency outside the Python basic library. The only things you need at this time is Python 3 and PyQt5 (and possibly Ninja).


## Reimplementability

Meson-ui has been designed in such a way that the implementation uses both MVC and REPO design patterns. This makes it possible (and maybe even easy) to reimplement Meson-ui in any other programming language like Kotlin
Dlang for example. There are currently no plans to reimplement Meson-ui, but we will make sure that Meson-ui
keeps it's MVC, REPO design patterns.
