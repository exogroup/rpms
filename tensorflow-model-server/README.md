# Overview

https://github.com/tensorflow/serving

_"The easiest and most straight-forward way of using TensorFlow Serving is with
Docker images. We highly recommend this route unless you have specific needs
that are not addressed by running in a container."_

_"The recommended approach to building from source is to use Docker. The
TensorFlow Serving Docker development images encapsulate all the dependencies
you need to build your own version of TensorFlow Serving."_

So Docker or Docker. There's also deb packages, but those seem to be built
using Docker.

As of 2024/01 no rpm packages seem to exist for TensorFlow Serving, which
isn't that surprising since a proper src.rpm for offline building would weigh
close to 6GB.

* https://github.com/tensorflow/serving/issues/1052 (2018, closed in 2019)
* https://superuser.com/questions/1431525/installing-tensorflow-model-server-on-centos-rhel (2019, no replies)

Don't expect one to be submitted to Fedora anytime soon: It statically links
everything using Bazel, which is a java app (~2GB RAM footprint during build!)
that downloads everything on the fly but the kitchen sink. And no mechanism
seems to be provided to dynamically link any of those (boost, libevent,
rapidjson...), even the ones with no changes, so justifying exceptions to
packaging rules would be impossible.

This is basically C++ built similarly to Go or Rust.

## Bazel

https://bazel.build/docs/user-manual

The only rpm package I've found of bazel is the following:
https://copr.fedorainfracloud.org/coprs/vbatts/bazel/

The `bazel6` package for `el9` worked to build TensorFlow Serving 2.14.1.

## Build

This is what docs say to use for manual build:
```
bazel build -c opt tensorflow_serving/...
```

But it's not what the project itself uses to build. The build options have
been extracted from `tensorflow_serving/tools/docker/Dockerfile.devel` and
adapted further:

* Change `--color=yes` to `no` to avoid polluting the logs.
* Keep `--curses=yes` because without it the logs end up being too short.
* `--compilation_mode [-c] (fastbuild, dbg or opt; default: "fastbuild")`

See also `bazel help build` for details on the generic options used.

## CPU Instructions

From `tensorflow_serving/g3doc/setup.md`:
```
Instruction Set            | Flags
-------------------------- | ----------------------
AVX                        | `--copt=-mavx`
AVX2                       | `--copt=-mavx2`
FMA                        | `--copt=-mfma`
SSE 4.1                    | `--copt=-msse4.1`
SSE 4.2                    | `--copt=-msse4.2`
All supported by processor | `--copt=-march=native`
```

The `tensorflow_serving/model_servers/BUILD` for the deb build uses:
```
'-c opt --copt=-mavx --copt=-msse4.2'
```

Which results in runtime messages:
```
I external/org_tensorflow/tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
```

Given both AVX2 and FMA have been present in processors for a while now, they
are enabled by default in this package. Use the following build options if
needed:
```
--without avx
--without avx2
--without fma
--without sse4_1
--without sse4_2
```

## Notes and random stuff

My first problem was that trying to build on my i9-13900H Fedora workstation
(6+8 cores, 20 threads) with 32GB RAM resuled in the oomkiller going nuts
and killing my desktop session. The hungry `cc1plus` processes had too much
parallelism. This was easily solved with the `--jobs=` build option, which
gets passed onto make `-j`.

But after that, and once I got the output less noisy, my build was repeatedly
failing on a timeout fetching boost, which was done using git with 150+
sub-modules even though it was for a stable release. I wasn't able to find the
correct way to increase the 609s timeout, so I patched the `workspace.bzl`
to use the boost tarball of the same version instead (`1_75_0`).

```
external/org_boost/boost/math/distributions/binomial.hpp:82:10: fatal error: boost/math/distributions/fwd.hpp: No such file or directory
```

I tried using boost tarball instead, but that didn't work because it has a
different file structure for some reason. I tried various timeout related
settings, and the one that worked was `--experimental_scale_timeouts=`.

Questions:

* Where are the deb build files? https://www.tensorflow.org/tfx/serving/setup#installing_using_apt
* Need to build 2 different packages: tensorflow-model-server & tensorflow-model-server-universal ... meh, recent CPUs support all of those extensions (`--copt=-mavx --copt=-mavx2 --copt=-mfma --copt=-msse4.1 --copt=-msse4.2`)

Building fun:

* Building is only documented using Docker :-(
* Build requires https://bazel.build/ which is a Java thingy
  https://copr.fedorainfracloud.org/coprs/vbatts/bazel/ -> bazel6 6.4.0-0.el9
  https://download.copr.fedorainfracloud.org/results/vbatts/bazel/
* Bazel tries to download stuff at build time... mock offline breaks.
* Need to check what to do to build offline with bazel https://stackoverflow.com/questions/68104949/build-c-project-with-bazel-offline-without-internet-connection ... not worth it given the size ... will be lazy and go with `mock --enable-network` instead.

