# remirepo spec file for php-pecl-couchbase4
#
# Copyright (c) 2013-2024 Remi Collet
# License: CC-BY-SA-4.0
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

# NOTICE: mock requires --enable-network

# Disable RPATH check (no more needed)
#global __arch_install_post /bin/true
#global __brp_check_rpaths  /bin/true

%{?scl:%scl_package php-pecl-couchbase4}

%global pecl_name   couchbase
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
# After 20-tokenizer.ini, 40-igbinary and 40-json
%global ini_name    50-%{pecl_name}.ini
#global prever      beta4
%global sources     %{pecl_name}-%{version}%{?prever}
%global _configure  ../%{sources}/configure


Summary:       Couchbase Server PHP extension
Name:          %{?scl_prefix}php-pecl-couchbase4
Version:       4.2.4
Release:       1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}.ex1
# Apache-2.0
# src
# src/deps/cache/json/LICENSE.ryu
# src/deps/cache/boringssl
## BOOST
# asio/asio/include/asio.hpp
## BSD-3-Clause
# src/deps/cache/snappy/COPYING
# src/deps/cache/json/LICENSE.double-conversion
## BSD-2-Clause
# src/deps/cache/hdr_histogram_c/LICENSE.txt
# src/deps/cache/hdr_histogram_c/COPYING.txt
## MIT
# src/cpm
# src/deps/cache/gsl/LICENSE
# src/deps/cache/llhttp/LICENSE-MIT
# src/deps/cache/json/external/PEGTL/LICENSE
# src/deps/cache/json/LICENSE
# src/deps/cache/json/LICENSE.itoa
# src/deps/cache/spdlog/LICENSE
License:       Apache-2.0 AND BSD-3-Clause AND BSD-2-Clause AND MIT AND BSL-1.0
URL:           https://pecl.php.net/package/couchbase
Source0:       https://pecl.php.net/get/%{sources}.tgz
Patch0:        couchbase-4.2.4-PCBC-975.patch

BuildRequires: git
BuildRequires: make
BuildRequires: cmake >= 3.19
BuildRequires: %{?dtsprefix}gcc
BuildRequires: %{?dtsprefix}gcc-c++
BuildRequires: %{?scl_prefix}php-devel >= 8.1
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: %{?scl_prefix}php-json
BuildRequires: %{?scl_prefix}php-tokenizer
BuildRequires: zlib-devel

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
Requires:      %{?scl_prefix}php-json%{?_isa}
Requires:      %{?scl_prefix}php-tokenizer%{?_isa}

Provides:      %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Obsoletes:     %{?scl_prefix}php-pecl-couchbase          < 4
Provides:      %{?scl_prefix}php-pecl-couchbase          = %{version}
Provides:      %{?scl_prefix}php-pecl-couchbase%{?_isa}  = %{version}
%if 0%{?fedora} >= 37 || 0%{?rhel} >= 10 || "%{php_version}" > "8.2"
Obsoletes:     %{?scl_prefix}php-pecl-couchbase2         < 4
Provides:      %{?scl_prefix}php-pecl-couchbase2         = %{version}
Provides:      %{?scl_prefix}php-pecl-couchbase2%{?_isa} = %{version}
Obsoletes:     %{?scl_prefix}php-pecl-couchbase3         < 4
Provides:      %{?scl_prefix}php-pecl-couchbase3         = %{version}
Provides:      %{?scl_prefix}php-pecl-couchbase3%{?_isa} = %{version}
%else
# Only 1 version can be installed
Conflicts:     %{?scl_prefix}php-pecl-couchbase2         < 4
Conflicts:     %{?scl_prefix}php-pecl-couchbase3         < 4
%endif

Provides: bundled(hdr_histogram_c)
Provides: bundled(snappy)
Provides: bundled(fmt)
Provides: bundled(gsl)
Provides: bundled(http_parser)
Provides: bundled(json)
Provides: bundled(boringssl)
Provides: bundled(spdlog)


%description
The PHP client library provides fast access to documents stored
in a Couchbase Server.

* %{?scl_prefix}php-pecl-couchbase  provides API version 1.
* %{?scl_prefix}php-pecl-couchbase2 provides API version 2.
* %{?scl_prefix}php-pecl-couchbase3 provides API version 3.
* this package provides API version 4.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
%patch -P 0 -b .PCBC-975
sed -e '/LICENSE/s/role="doc"/role="src"/;/COPYING/s/role="doc"/role="src"/' -i package.xml

: Collect license files
mkdir lic
cd %{sources}
cp src/deps/cache/hdr_histogram/*/hdr_histogram/COPYING.txt ../lic/hdr_histogram_c_COPYING.txt
cp src/deps/cache/hdr_histogram/*/hdr_histogram/LICENSE.txt ../lic/hdr_histogram_c_LICENSE.txt
cp src/deps/cache/snappy/*/snappy/COPYING                   ../lic/snappy_COPYING
cp src/deps/cache/gsl/*/gsl/LICENSE                         ../lic/gsl_LICENSE
cp src/deps/cache/llhttp/*/llhttp/LICENSE-MIT               ../lic/http_parser_LICENSE-MIT
cp src/deps/cache/json/*/json/external/PEGTL/LICENSE        ../lic/PEGTL_LICENSE
cp src/deps/cache/json/*/json/LICENSE                       ../lic/json_LICENSE
cp src/deps/cache/json/*/json/LICENSE.double-conversion     ../lic/json_LICENSE.double-conversion
cp src/deps/cache/json/*/json/LICENSE.itoa                  ../lic/json_LICENSE.itoa
cp src/deps/cache/json/*/json/LICENSE.ryu                   ../lic/json_LICENSE.ryu
cp src/deps/cache/spdlog/*/spdlog/LICENSE                   ../lic/spdlog_LICENSE
cp src/deps/cache/boringssl/*/boringssl/LICENSE             ../lic/boringssl_LICENSE
cp src/deps/couchbase-cxx-client/LICENSE.txt                ../lic/LICENSE.txt

: Parallel build
sed -e 's/--verbose/%{?_smp_mflags} --verbose/' -i Makefile.frag

: Sanity check as really often broken
extver=$(sed -n '/#define PHP_COUCHBASE_VERSION/{s/.* "//;s/".*$//;p}' src/php_couchbase.hxx)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}
   exit 1
fi
cd ..

: Configuration file
cat << 'EOF' | tee %{ini_name}
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; Configuration
;couchbase.max_persistent = 1
;couchbase.persistent_timeout = -1
;couchbase.log_level =
;couchbase.log_php_log_err = 1
;couchbase.log_stderr = 0
;couchbase.log_path =
EOF

mkdir NTS
%if %{with_zts}
mkdir ZTS
%endif


%build
%{?dtsenable}

cd %{sources}
%{__phpize}
# fix for make_install, notice make_build is broken
sed -e 's/INSTALL_ROOT/DESTDIR/' -i build/Makefile.global

cd ../NTS
%configure --with-php-config=%{__phpconfig}
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%configure --with-php-config=%{__ztsphpconfig}
make %{?_smp_mflags}
%endif


%install
%{?dtsenable}

# Install the NTS stuff
%make_install -C NTS
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install the ZTS stuff
%if %{with_zts}
%make_install -C ZTS
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
: minimal NTS load test
%{__php} -n \
   -d extension=tokenizer.so \
   -d extension=json.so \
   -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
   -m | grep '^%{pecl_name}$'

%if %{with_zts}
: minimal ZTS load test
%{__ztsphp} -n \
   -d extension=tokenizer.so \
   -d extension=json.so \
   -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
   -m | grep '^%{pecl_name}$'
%endif


%files
%license lic/*
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Wed Oct 23 2024 Remi Collet <remi@remirepo.net> - 4.2.4-1
- update to 4.2.4

* Wed Aug 28 2024 Remi Collet <remi@remirepo.net> - 4.2.3-1
- update to 4.2.3

* Thu Jul 25 2024 Remi Collet <remi@remirepo.net> - 4.2.2-1
- update to 4.2.2

* Wed Apr 24 2024 Remi Collet <remi@remirepo.net> - 4.2.1-1
- update to 4.2.1

* Tue Mar 19 2024 Remi Collet <remi@remirepo.net> - 4.2.0-1
- update to 4.2.0
- raise dependency on PHP 8.1
- not buildable offline, reported upstream

* Wed Oct 11 2023 Remi Collet <remi@remirepo.net> - 4.1.6-1
- update to 4.1.6
- drop patch merged upstream

* Thu Aug 31 2023 Remi Collet <remi@remirepo.net> - 4.1.5-2
- add patch for PHP 8.3 from
  https://github.com/couchbase/couchbase-php-client/pull/130

* Mon Aug 21 2023 Remi Collet <remi@remirepo.net> - 4.1.5-1
- update to 4.1.5

* Fri May 26 2023 Remi Collet <remi@remirepo.net> - 4.1.4-1
- update to 4.1.4

* Thu Apr 13 2023 Remi Collet <remi@remirepo.net> - 4.1.3-1
- update to 4.1.3

* Wed Mar 22 2023 Remi Collet <remi@remirepo.net> - 4.1.2-2
- build out of sources tree

* Mon Mar 20 2023 Remi Collet <remi@remirepo.net> - 4.1.2-1
- update to 4.1.2

* Mon Feb 27 2023 Remi Collet <remi@remirepo.net> - 4.1.1-1
- update to 4.1.1
- raise dependency on PHP 8.0
- drop patch merged upstream

* Fri Feb 17 2023 Remi Collet <remi@remirepo.net> - 4.1.0-2
- fix GCC 13 build using patch from
  https://github.com/couchbase/couchbase-php-client/pull/63

* Mon Jan 23 2023 Remi Collet <remi@remirepo.net> - 4.1.0-1
- update to 4.1.0
- drop patch merged upstream

* Wed May 11 2022 Remi Collet <remi@remirepo.net> - 4.0.0-1
- update to 4.0.0
- drop dependency on libcouchbase
- License is ASL 2.0 and BSD and MIT

* Thu Dec  9 2021 Remi Collet <remi@remirepo.net> - 3.2.2-1
- update to 3.2.2
- raise dependency on libcouchbase 3.2.4

* Thu Oct 14 2021 Remi Collet <remi@remirepo.net> - 3.2.1-1
- update to 3.2.1
- raise dependency on libcouchbase 3.2.2

* Wed Sep 01 2021 Remi Collet <remi@remirepo.net> - 3.2.0-2
- rebuild for 8.1.0RC1

* Wed Jul 28 2021 Remi Collet <remi@remirepo.net> - 3.2.0-1
- update to 3.2.0
- drop patch merged upstream
- raise dependency on libcouchbase 3.2

* Wed Jul 21 2021 Remi Collet <remi@remirepo.net> - 3.1.2-2
- add patch for PHP 8.1.0beta1 from
  https://github.com/couchbase/php-couchbase/pull/33

* Fri May 14 2021 Remi Collet <remi@remirepo.net> - 3.1.2-1
- update to 3.1.2

* Fri Mar  5 2021 Remi Collet <remi@remirepo.net> - 3.1.1-1
- update to 3.1.1
- raise dependency on libcouchbase 3.1

* Thu Jan 21 2021 Remi Collet <remi@remirepo.net> - 3.1.0-1
- update to 3.1.0

* Mon Dec  7 2020 Remi Collet <remi@remirepo.net> - 3.0.5-1
- update to 3.0.5
- drop patches merged upstream
- add patch for PHP 7.2 from
  https://github.com/couchbase/php-couchbase/pull/32

* Fri Nov 13 2020 Remi Collet <remi@remirepo.net> - 3.0.4-2
- add patch for PHP 8 from
  https://github.com/couchbase/php-couchbase/pull/31
- open https://github.com/couchbase/php-couchbase/pull/30 min PHP version
- open https://github.com/couchbase/php-couchbase/pull/29 pkg-config

* Thu Nov 12 2020 Remi Collet <remi@remirepo.net> - 3.0.4-1
- update to 3.0.4
- rename to php-pecl-couchbase3
- raise dependency on PHP 7.1
- raise dependency on libcouchbase 3.0
- drop dependency on igbinary extension

* Tue Feb  4 2020 Remi Collet <remi@remirepo.net> - 2.6.2-1
- update to 2.6.2

* Tue Jan 28 2020 Remi Collet <remi@remirepo.net> - 2.6.1-4
- add upstream patch to fix segfault in timeout

* Fri Jan 17 2020 Remi Collet <remi@remirepo.net> - 2.6.1-3
- rebuild against libcouchase 2.10.5 for
  https://github.com/remicollet/remirepo/issues/136

* Tue Sep 03 2019 Remi Collet <remi@remirepo.net> - 2.6.1-2
- rebuild for 7.4.0RC1

* Mon Jun  3 2019 Remi Collet <remi@remirepo.net> - 2.6.1-1
- update to 2.6.1

* Sat Oct  6 2018 Remi Collet <remi@remirepo.net> - 2.6.0-1
- update to 2.6.0
- raise dependency on libcouchbase 2.9.5

* Thu Aug 16 2018 Remi Collet <remi@remirepo.net> - 2.5.0-3
- rebuild for 7.3.0beta2 new ABI

* Tue Jul 17 2018 Remi Collet <remi@remirepo.net> - 2.5.0-2
- rebuld for 7.3.0alpha4 new ABI

* Thu Jul  5 2018 Remi Collet <remi@remirepo.net> - 2.5.0-1
- update to 2.5.0
- raise dependency on libcouchbase 2.9.2

* Fri Jun 22 2018 Remi Collet <remi@remirepo.net> - 2.4.7-2
- add patch for PHP 7.3 from
  https://github.com/couchbase/php-couchbase/pull/22

* Fri Jun  8 2018 Remi Collet <remi@remirepo.net> - 2.4.7-1
- update to 2.4.7
- raise dependency on libcouchbase 2.9.0

* Mon Apr 16 2018 Remi Collet <remi@remirepo.net> - 2.4.6-1
- update to 2.4.6
- raise dependency on libcouchbase 2.8.6

* Sun Mar 11 2018 Remi Collet <remi@remirepo.net> - 2.4.5-1
- update to 2.4.5

* Tue Feb 13 2018 Remi Collet <remi@remirepo.net> - 2.4.4-1
- Update to 2.4.4

* Fri Jan  5 2018 Remi Collet <remi@remirepo.net> - 2.4.3-1
- Update to 2.4.3
- raise dependency on libcouchbase 2.8.4

* Tue Nov 14 2017 Remi Collet <remi@remirepo.net> - 2.4.2-1
- Update to 2.4.2

* Thu Oct  5 2017 Remi Collet <remi@remirepo.net> - 2.4.1-1
- Update to 2.4.1
- update provided configuration for couchbase.pool.max_idle_time_sec

* Wed Sep 20 2017 Remi Collet <remi@remirepo.net> - 2.4.0-2
- rebuild with libcouchbase 2.8.1

* Tue Sep  5 2017 Remi Collet <remi@remirepo.net> - 2.4.0-1
- Update to 2.4.0
- raise minimal PHP version to 5.6
- raise dependency on libcouchbase 2.8

* Tue Aug  1 2017 Remi Collet <remi@remirepo.net> - 2.3.4-1
- Update to 2.3.4

* Tue Jul 18 2017 Remi Collet <remi@remirepo.net> - 2.3.3-3
- rebuild for PHP 7.2.0beta1 new API

* Wed Jun 21 2017 Remi Collet <remi@remirepo.net> - 2.3.3-2
- rebuild for 7.2.0alpha2

* Thu Jun  1 2017 Remi Collet <remi@remirepo.net> - 2.3.3-1
- Update to 2.3.3
- raise dependency on libcouchbase 2.7.5

* Tue May  2 2017 Remi Collet <remi@remirepo.net> - 2.3.2-1
- Update to 2.3.2

* Wed Apr  5 2017 Remi Collet <remi@remirepo.net> - 2.3.1-1
- Update to 2.3.1

* Wed Mar  8 2017 Remi Collet <remi@remirepo.net> - 2.3.0-1
- Update to 2.3.0
- drop dependency on pcs extension
- add dependency on igbinary extension
- raise dependency on libcouchbase 2.7.2
- update default configuration with new options

* Tue Dec 27 2016 Remi Collet <remi@fedoraproject.org> - 2.2.4-1
- Update to 2.2.4
- add dependency on pcs extension

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 2.2.3-2
- rebuild with PHP 7.1.0 GA

* Wed Oct 05 2016 Remi Collet <remi@fedoraproject.org> - 2.2.3-1
- Update to 2.2.3
- open https://issues.couchbase.com/browse/PCBC-437 - visibility error

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 2.2.2-2
- rebuild for PHP 7.1 new API version

* Wed Sep 07 2016 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2

* Mon Aug 08 2016 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Thu Jul  7 2016 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0 (php 5 and 7, stable)

* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.3.beta4
- Update to 2.2.0beta4 (php 5 and 7, beta)

* Thu May 26 2016 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.2.beta3
- Update to 2.2.0beta3 (php 5 and 7, beta)

* Sun Mar 20 2016 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.1.beta1
- Update to 2.2.0beta2 (php 5 and 7, beta)

* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 2.1.0-2
- adapt for F24

* Thu Nov 05 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0
- add patch to use system fastlz library
  from https://github.com/couchbase/php-couchbase/pull/10

* Wed Apr 22 2015 Remi Collet <remi@fedoraproject.org> - 2.0.7-1
- Update to 2.0.7

* Wed Apr 08 2015 Remi Collet <remi@fedoraproject.org> - 2.0.6-1
- Update to 2.0.6 (stable)

* Wed Mar 04 2015 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5 (stable)

* Mon Feb 09 2015 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4 (stable)
- drop runtime dependency on pear, new scriptlet

* Wed Jan 07 2015 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 2.0.2-1.1
- Fedora 21 SCL mass rebuild

* Wed Dec 03 2014 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2

* Wed Nov 05 2014 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1

* Sat Sep 20 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- rename to php-pecl-couchbase2 for new API
- update to 2.0.0
- open http://www.couchbase.com/issues/browse/PCBC-292 license
- open http://www.couchbase.com/issues/browse/PCBC-293 fastlz
- open http://www.couchbase.com/issues/browse/PCBC-294 xdebug

* Sat Sep  6 2014 Remi Collet <remi@fedoraproject.org> - 1.2.2-3
- test build with system fastlz

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 1.2.2-2
- improve SCL build

* Mon May 12 2014 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-4
- add numerical prefix to extension configuration file

* Sun Mar 16 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-2
- install doc in pecl_docdir

* Sat Oct 05 2013 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1
- add patch to fix ZTS build
  https://github.com/couchbase/php-ext-couchbase/pull/9

* Mon May 13 2013 Remi Collet <remi@fedoraproject.org> - 1.1.15-2
- fix dependency on php-pecl-igbinary

* Thu May  9 2013 Remi Collet <remi@fedoraproject.org> - 1.1.15-1
- update to 1.1.15 (no change)

* Fri Mar 22 2013 Remi Collet <remi@fedoraproject.org> - 1.1.14-1
- initial package

