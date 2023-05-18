# openssl11

See https://src.fedoraproject.org/rpms/openssl11 for all files.
This "fork" just includes the OpenResty patch from:
https://github.com/openresty/openresty/blob/master/patches/

```
git clone https://src.fedoraproject.org/rpms/openssl11.git
cd openssl11
git checkout ea9bec71fae72888bec4284f0a522ea0b52b124d
fedpkg sources
wget https://github.com/openresty/openresty/raw/master/patches/openssl-1.1.1f-sess_set_get_cb_yield.patch
patch -p0 < ~/git/exogroup-rpms/openssl11/openssl11.spec.patch
```
...then build as usual.

