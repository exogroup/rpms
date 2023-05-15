# nginx

This is a fork of the [Fedora nginx](https://src.fedoraproject.org/rpms/nginx)
package with a few additions:

 * [GeoIP2 module](https://github.com/leev/ngx_http_geoip2_module/)
 * [Naxsi module](https://github.com/wargio/naxsi/)
 * [Phusion Passenger module](https://www.phusionpassenger.com/)
 * [Brotli module](https://github.com/google/ngx_brotli)
 * [51Degrees module](https://github.com/51Degrees/Device-Detection/)

For building the 51Degrees module on RHEL7 aarch64, this manual workaround
is required:
```
ln -s libatomic.so.1 /usr/lib64/libatomic.so
```

