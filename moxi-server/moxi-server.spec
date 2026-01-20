# The debugsource is empty on RHEL9
%if 0%{?rhel} < 10
%global _debugsource_template %{nil}
%endif

%global gh_commit c460b9a75069538782d319d2e37c34a1a9f1a85b

Name: moxi-server
Version: 6.0.0
Release: 1%{?dist}
Summary: Memcached/CouchBase proxy with energy and pep
Group: System Environment/Daemons
License: BSD
URL: https://github.com/couchbase/moxi
Source0: https://github.com/andrewkendall/moxi/archive/%{gh_commit}.tar.gz
Source1: moxi.notactual
Source2: moxi-sysusers.conf
Source3: moxi-server.service
Source4: moxi-server.sysconfig
BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libevent-devel
BuildRequires: libcurl-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: cjson-devel
BuildRequires: systemd-rpm-macros
%{?sysusers_requires_compat}

%description
Moxi moxi is a proxy capable of handling many connections for client
applications, providing those clients simplified management and increased
performance.  It can be used with memcached servers or a CouchBase Cluster
hosting both CouchBase and Memcached type buckets.


%prep
%setup -q -n moxi-%{gh_commit}
mkdir build


%build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/opt/moxi ..
%make_build


%install
cd build
%make_install
install -d %{buildroot}/var/log/moxi
# Keep the same LD_LIBRARY_PATH hack script as the original
mv %{buildroot}/opt/moxi/bin/moxi %{buildroot}/opt/moxi/bin/moxi.actual
install -p -m 0755 %{SOURCE1} %{buildroot}/opt/moxi/bin/moxi
# User and service
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/moxi.conf
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/moxi-server.service
install -D -p -m 0640 %{SOURCE4} %{buildroot}/etc/sysconfig/moxi-server


%pre
%sysusers_create_compat %{SOURCE2}

%post
%systemd_post moxi-server.service

%preun
%systemd_preun moxi-server.service

%postun
%systemd_postun_with_restart moxi-server.service


%files
%license LICENSE
%doc README README.standalone.md
%dir /opt/moxi
%dir /opt/moxi/bin
/opt/moxi/bin/moxi
/opt/moxi/bin/moxi.actual
/opt/moxi/bin/vbucketkeygen
/opt/moxi/bin/vbuckettool
%dir /opt/moxi/lib
%exclude /opt/moxi/lib/*.so
/opt/moxi/lib/libconflate.so.*
/opt/moxi/lib/libhashkit.so.*
/opt/moxi/lib/libmcd.so.*
/opt/moxi/lib/libvbucket.so.*
%attr(0755,moxi,moxi) /var/log/moxi
# User and service
%{_sysusersdir}/moxi.conf
%{_unitdir}/moxi-server.service
%config(noreplace) %attr(0640,root,moxi) /etc/sysconfig/moxi-server


%changelog
* Tue Jan 20 2026 Matthias Saou <matthias@saou.eu> 6.0.0-1
- Update to 6.0.0 standalone fork by @andrewkendall.
- Keep package name and LD_LIBRARY_PATH hack to be drop-in replacement.
- Provide systemd service and use sysconfig file for setting command line.

* Wed Apr  4 2018 Matthias Saou <matthias@saou.eu> 5.0.0-1
- Write compatible spec file from scratch.

