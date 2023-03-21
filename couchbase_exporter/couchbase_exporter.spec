# Workaround for 'error: Empty %files file debugsourcefiles.list' on RHEL8
# Breaks build on RHEL9, so disable
#define _debugsource_template %{nil}
%global daemon_name couchbase_exporter

Name:             couchbase_exporter
Version:          1.0.8
Release:          1%{?dist}
Summary:          Prometheus exporter for the metrics available in CouchBase
Group:            Applications/System
License:          ASL 2.0
URL:              https://github.com/couchbase/couchbase-exporter
# Created by prep-packages.sh
Source0:          %{name}-%{version}.tar.gz
Source1:          couchbase_exporter.service
Source11:         couchbase_exporter_sysconfig
BuildRequires:    golang
BuildRequires:    systemd
%{?systemd_requires}

%description
The Couchbase Prometheus Exporter is an official Prometheus Exporter which
supplies Couchbase Server metrics to Prometheus. These include, but are not
limited to, CPU and Memory usage, Ops per second, read and write rates, and
queue sizes. Metrics can be refined to a per node and also a per bucket basis.


%prep
%setup -q -n couchbase_exporter-%{version}

%build
export GOPATH=$(pwd)
export GO111MODULE=off
cd src/github.com/couchbase/couchbase-exporter
# Workaround for missing build id which makes debuginfo extraction fail
function gobuild { go build -a -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -v -x "$@"; }
gobuild -a -o couchbase_exporter .

%install
install -m 0755 -D src/github.com/couchbase/couchbase-exporter/couchbase_exporter \
  %{buildroot}%{_sbindir}/couchbase_exporter
install -D -p -m 0644 %{SOURCE1} \
  %{buildroot}%{_unitdir}/%{daemon_name}.service
install -D -p -m 0644 %{SOURCE11} \
  %{buildroot}%{_sysconfdir}/sysconfig/couchbase_exporter


%pre
getent group couchbase_exporter >/dev/null || groupadd -r couchbase_exporter
getent passwd couchbase_exporter >/dev/null || \
  useradd -r -d /run/couchbase_exporter -g couchbase_exporter \
  -s /sbin/nologin -c "CouchBase Exporter" couchbase_exporter

%post
%systemd_post %{daemon_name}.service

%preun
%systemd_preun %{daemon_name}.service

%postun
%systemd_postun_with_restart %{daemon_name}.service


%files
%license src/github.com/couchbase/couchbase-exporter/LICENSE
%doc src/github.com/couchbase/couchbase-exporter/README.md
%config(noreplace) %{_sysconfdir}/sysconfig/couchbase_exporter
%{_sbindir}/couchbase_exporter
%{_unitdir}/%{daemon_name}.service


%changelog
* Tue Mar 21 2023 Matthias Saou <matthias@saou.eu> 1.0.8-1
- Update to 1.0.8.

* Mon Oct 12 2020 Michele Brodoloni <michele@exads.com> - 1.0.2-1
- Update to 1.0.2

* Mon Apr 20 2020 Matthias Saou <matthias@saou.eu> 0-0.2.2b7765b
- Set config as noreplace.
- Restart service upon update.
- Include LICENSE and README.md.
- Minor spec file fixes.

* Fri Apr 17 2020 Michał Lisowski <michal@exads.com> - 0-0.1.2b7765b
- Initial RPM release

