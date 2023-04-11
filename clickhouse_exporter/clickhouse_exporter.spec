%global commit 638809a48ff43b63bae006f63d2d8387743b8d90
%global gittag HEAD
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global daemon_name clickhouse_exporter

Name:             clickhouse_exporter
Version:          0
Release:          0.2.%{shortcommit}%{?dist}
Summary:          Prometheus exporter for the metrics available in ClickHouse
Group:            Applications/System
License:          MIT
URL:              https://github.com/f1yegor/clickhouse_exporter
Source0:          %{name}-%{shortcommit}.tar.gz
Source1:          clickhouse_exporter.service
Patch0:           fix_metrics_values_atoi.patch
BuildRequires:    golang
%{?systemd_requires}

%description
This is a simple server that periodically scrapes ClickHouse stats and exports
them via HTTP for Prometheus consumption.


%prep
%setup -n clickhouse_exporter-%{shortcommit}
%patch0 -p1 -d src/github.com/f1yegor/clickhouse_exporter

%build
export GOPATH=$(pwd):%{gopath}
cd src/github.com/f1yegor/clickhouse_exporter
# Workaround for missing build id which makes debuginfo extraction fail
function gobuild { go build -a -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -v -x "$@"; }
gobuild -a -o clickhouse_exporter .


%install
install -m 0755 -D src/github.com/f1yegor/clickhouse_exporter/clickhouse_exporter %{buildroot}/usr/sbin/clickhouse_exporter
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{daemon_name}.service


%pre
getent group clickhouse_exporter >/dev/null || groupadd -r clickhouse_exporter
getent passwd clickhouse_exporter >/dev/null || \
  useradd -r -d /run/clickhouse_exporter -g clickhouse_exporter \
  -s /sbin/nologin -c "Clickhouse Exporter" clickhouse_exporter


%post
%systemd_post %{daemon_name}.service


%preun
%systemd_preun %{daemon_name}.service


%postun
%systemd_postun %{daemon_name}.service


%files
%{_sbindir}/clickhouse_exporter
%{_unitdir}/%{daemon_name}.service


%changelog
* Mon Feb 15 2021 Michele Brodoloni <michele@exads.com> - 0-0.2.638809a
- Compatibility patch for CH v20+

* Fri Jan 25 2019 Michał Lisowski <michal@exads.com> - 0-0.1.638809a
- Bump to the most recent GH commit

* Mon Aug 20 2018 Michał Lisowski <michal@exads.com> - 0-0.1.8c9e82d
- Initial RPM release

