# Fix "Empty %files file" debugsourcefiles.list (we have no sources, duh!)
%define _debugsource_template %{nil}
# Work around 'ERROR: No build ID note found in ...'
%undefine _missing_build_ids_terminate_build

%global daemon_name kafka_exporter

Name:             kafka_exporter
Version:          1.9.0
Release:          1
Summary:          Kafka exporter for Prometheus
Group:            Applications/System
License:          ASL 2.0
URL:              https://github.com/danielqsj/kafka_exporter
Source0:          https://github.com/danielqsj/kafka_exporter/releases/download/v%{version}/kafka_exporter-%{version}.linux-amd64.tar.gz
Source1:          kafka_exporter@.service
%{?systemd_requires}
BuildRequires:    systemd
ExclusiveArch:    x86_64

%description
Kafka exporter for Prometheus.


%prep
%setup -q -n kafka_exporter-%{version}.linux-amd64


%build


%install
install -m 0755 -D kafka_exporter %{buildroot}/usr/sbin/kafka_exporter
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{daemon_name}@.service


%pre
getent group kafka_exporter >/dev/null || groupadd -r kafka_exporter
getent passwd kafka_exporter >/dev/null || \
  useradd -r -d /run/kafka_exporter -g kafka_exporter \
  -s /sbin/nologin -c "Kafka Exporter" kafka_exporter


%post
%systemd_post %{daemon_name}.service


%preun
%systemd_preun %{daemon_name}.service


%postun
%systemd_postun %{daemon_name}.service


%files
%license LICENSE
%{_sbindir}/kafka_exporter
%{_unitdir}/%{daemon_name}@.service


%changelog
* Wed Aug 13 2025 Matthias Saou <matthias@saou.eu> 1.9.0-1
- Update to 1.9.0.

* Wed Aug 11 2021 Matthias Saou <matthias@saou.eu> 1.3.1-1
- Update to 1.3.1.
- Use binary release as source, pulling prometheus was now 800MB for .src.rpm.

* Fri Sep 07 2018 Michał Lisowski <michal@exads.com> - 1.2.0-1
- Initial RPM release

