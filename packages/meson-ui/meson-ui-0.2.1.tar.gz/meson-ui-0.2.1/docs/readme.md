# Meson-ui Documentation

## Build dependencies

Meson-ui uses Meson and [hotdoc](https://github.com/hotdoc/hotdoc) for generating 
documentation.  Minimum required version of hotdoc is *0.8.9*.  Instructions on 
how to install hotdoc are [here](https://hotdoc.github.io/installing.html).


## Building the documentation

From the Meson-ui repository root dir:
```
$ cd docs/
$ meson built_docs
$ ninja -C built_docs/ upload
```

Now you should be able to open the documentation locally
```
built_docs/Meson-ui docs/html/index.html
```