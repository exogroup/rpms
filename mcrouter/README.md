# rpm-mcrouter

Source files to build Facebook's
[Mcrouter](https://github.com/facebook/mcrouter) on RHEL8.

Check mcrouter's release content for the following files, and build them in
this order at the commit contained in these files:
* `FOLLY_COMMIT`
* `FIZZ_COMMIT`
* `WANGLE_COMMIT`
* `FBTHRIFT_COMMIT`

For version 41, it was all done in this commit:
https://github.com/facebook/mcrouter/commit/9ffd13e9ab6c2c02bd1f95a7169c9a69b1b6bc54

As for July 2020, Mcrouter master branch didn't build properly against all of
the other component's master branches.

Going back to version 41 from November 2019 did re-introduce the yarpl
requirement (and also rsocket-cpp entirely), which was taken from the same
date "just in case".

