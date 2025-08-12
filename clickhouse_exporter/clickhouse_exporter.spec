%global commit 2263a68c67ddb3cc9cbda3f7caba6681742225aa
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global daemon_name clickhouse_exporter

Name:             clickhouse_exporter
Version:          0
Release:          0.4.%{shortcommit}
Summary:          Prometheus exporter for the metrics available in ClickHouse
Group:            Applications/System
License:          MIT
URL:              https://github.com/ClickHouse/clickhouse_exporter
Source0:          %{name}-%{shortcommit}.tar.gz
Source1:          clickhouse_exporter.service
BuildRequires:    golang
BuildRequires:    systemd
%{?systemd_requires}

%description
This is a simple server that periodically scrapes ClickHouse stats and exports
them via HTTP for Prometheus consumption.


%prep
%setup -n clickhouse_exporter-%{shortcommit}


%build
export GOPATH=$(pwd):%{gopath}
export GO111MODULE=on
cd src/github.com/ClickHouse/clickhouse_exporter
# Workaround for missing build id which makes debuginfo extraction fail
function gobuild { go build -a -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -v -x "$@"; }
gobuild -a -o clickhouse_exporter .


%install
install -m 0755 -D src/github.com/ClickHouse/clickhouse_exporter/clickhouse_exporter %{buildroot}/usr/sbin/clickhouse_exporter
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
* Tue Aug 12 2025 Matthias Saou <matthias@saou.eu> 0.0-4.2263a68c
- Update to the latest upstream code, despite being obsolete, as it still
  provides parts per table metrics.

* Tue Apr 11 2023 Matthias Saou <matthias@saou.eu> 0.0-3.7ab68be4
- Update to the latest upstream code from ClickHouse org to fix v23+ errors.
- Switch to using go modules.
- Drop no longer needed patch.

* Mon Feb 15 2021 Michele Brodoloni <michele@exads.com> - 0-0.2.638809a
- Compatibility patch for CH v20+

* Fri Jan 25 2019 Michał Lisowski <michal@exads.com> - 0-0.1.638809a
- Bump to the most recent GH commit

* Mon Aug 20 2018 Michał Lisowski <michal@exads.com> - 0-0.1.8c9e82d
- Initial RPM release

