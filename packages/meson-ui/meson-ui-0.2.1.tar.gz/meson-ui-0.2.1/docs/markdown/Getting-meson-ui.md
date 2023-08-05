# Getting meson-ui

Meson-ui is implemented in Python 3, and requires 3.6 or newer. If your operating
system provides a package manager, you should install it with that. For
platforms that don't have a package manager, you need to download it from
[Python's home page]. See below for [platform-specific Python3 quirks](#platformspecific-install-quirks).

## Downloading Meson-ui

Meson-ui releases can be downloaded from the [GitHub release page], and you can
run `./meson-ui.py` from inside a release or the git repository itself without
doing anything special.

On Windows, if you did not install Python with the installer options that make
Python scripts executable, you will have to run `python /path/to/meson-ui.py`,
where `python` is Python 3.6 or newer.

The newest development code can be obtained directly from [Git], and we strive
to ensure that it will always be working and usable. All commits go through
a pull-request process that runs CI and tests several platforms.

## Installing Meson-ui with pip

Meson is available in the [Python Package Index] and can be installed with
`pip3 install meson-ui` which requires root and will install it system-wide.

Alternatively, you can use `pip3 install --user meson-ui` which will install it
for your user and does not require any special privileges. This will install
the package in `~/.local/`, so you will have to add `~/.local/bin` to your
`PATH`.

# Platform-specific install quirks

## Windows Python3 quirks

When installing Python 3, it is highly recommended (but not required) that you
select the installer options as follows:

![installer step 1](images/py3-install-1.png "Enable 'Add Python 3.6 to PATH' and click 'Customize installation'")
![installer step 2](images/py3-install-2.png "Optional Features: ensure 'pip' is enabled")
![installer step 3](images/py3-install-3.png "Advanced Options: enable 'Install for all users'")

With this, you will have `python` and `pip` in `PATH`, and you can install
Meson-ui with pip. You will also be able to directly run `meson-ui` in any shell on
Windows instead of having to run `py -3` with the full path to the `meson-ui.py`
script.
