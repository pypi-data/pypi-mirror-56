---
title: Release 0.2.1
short-description: Release notes for 0.2.1
...

# New features

## Added new options for Meson build `errorlog` and `stdstrip`
Meson-ui now supports `errorlog` and `stdstrip` for test.

## Added `--version` option for printing the version number
Meson-ui now has `-v` and `--version` for printing the current version
number.

```console
meson-ui --version
```

## Fixed several bugs with ui
There where several bugs with the table view in both introspection view
and main activity target table.  Scrollbar and better table component.

## Added new auto directory filler
Meson-ui now has a new auto directory filler for source and build
directory.  whenever you call `meson-ui` the path values will fill.

