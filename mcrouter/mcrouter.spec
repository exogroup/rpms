%global commit 9ffd13e9ab6c2c02bd1f95a7169c9a69b1b6bc54
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary: Memcached protocol router for scaling memcached deployments
Name: mcrouter
Version: 0.41.0
Release: 1%{?shortcommit:.git.%{shortcommit}}%{?dist}
License: MIT
URL: https://github.com/facebook/mcrouter/
Source0: https://github.com/facebook/mcrouter/archive/%{commit}/mcrouter-%{shortcommit}.tar.gz
Source1: mcrouter.service
Source2: mcrouter.sysconfig
Source3: mcrouter.logrotate
Source4: mcrouter.json
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: git-core
BuildRequires: openssl-devel
BuildRequires: fbthrift-devel
BuildRequires: python3-devel
BuildRequires: libevent-devel
BuildRequires: boost-devel
BuildRequires: zlib-devel
BuildRequires: double-conversion-devel
BuildRequires: folly-devel
BuildRequires: libsodium-devel
BuildRequires: fizz-devel
BuildRequires: ragel
BuildRequires: systemd-rpm-macros
%{?systemd_requires}

%description
Mcrouter (pronounced mc router) is a memcached protocol router for scaling
memcached deployments. It's a core component of cache infrastructure at
Facebook and Instagram where mcrouter handles almost 5 billion requests per
second at peak.


%prep
%setup -q -n mcrouter-%{commit}


%build
cd mcrouter
unset LANG
autoreconf -fvi
export FBTHRIFT_BIN="%{_bindir}"
export PYTHON_VERSION="3"
%configure
make %{?_smp_mflags}


%install
cd mcrouter
make install DESTDIR=%{buildroot}
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/mcrouter.service
install -D -p -m 0644 %{SOURCE2} %{buildroot}/etc/sysconfig/mcrouter
install -D -p -m 0644 %{SOURCE3} %{buildroot}/etc/logrotate.d/mcrouter
install -D -p -m 0640 %{SOURCE4} %{buildroot}/etc/mcrouter/mcrouter.json
mkdir -p %{buildroot}/var/{log,spool}/mcrouter
mkdir -p %{buildroot}/var/mcrouter/{config,fifos,stats}


%pre
getent group mcrouter >/dev/null || groupadd -r mcrouter
getent passwd mcrouter >/dev/null || \
  useradd -r -d / -g mcrouter \
  -s /sbin/nologin -c "Mcrouter" mcrouter

%post
%systemd_post mcrouter.service

%preun
%systemd_preun mcrouter.service

%postun
%systemd_postun mcrouter.service


%files
%license LICENSE
%doc CODE_OF_CONDUCT.md CONTRIBUTING.md README.md
%config(noreplace) /etc/logrotate.d/mcrouter
%attr(0750,root,mcrouter) %dir /etc/mcrouter
%attr(0640,root,mcrouter) %config(noreplace) /etc/mcrouter/mcrouter.json
%attr(0640,root,mcrouter) %config(noreplace) /etc/sysconfig/mcrouter
%{_bindir}/mcpiper
%{_bindir}/mcrouter
%{_unitdir}/mcrouter.service
%attr(0770,root,mcrouter) %dir /var/log/mcrouter
%attr(0770,root,mcrouter) %dir /var/mcrouter
%attr(0770,root,mcrouter) %dir /var/spool/mcrouter


%changelog
* Wed Jul 29 2020 Matthias Saou <matthias@saou.eu> 0.41.0-1
- Initial RPM release.

