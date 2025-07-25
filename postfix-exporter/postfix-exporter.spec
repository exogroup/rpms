Name: postfix-exporter
Version: 0.11.0
Release: 2
Summary: Prometheus metrics exporter for Postfix
License: ASL 2.0
URL: https://github.com/Hsn723/postfix_exporter
Source0: https://github.com/Hsn723/postfix_exporter/releases/download/v%{version}/postfix_exporter_systemd_%{version}_linux_amd64.tar.gz
Source1: postfix-exporter.service
Source2: postfix-exporter.sysconfig
BuildRequires: systemd
ExclusiveArch: x86_64


%description
Prometheus metrics exporter for the Postfix mail server. This exporter provides
histogram metrics for the size and age of messages stored in the mail queue.
It extracts these metrics from Postfix by connecting to a UNIX socket under
/var/spool. It also counts events by parsing Postfix's log entries, using
regular expression matching. The log entries are retrieved from the systemd
journal, the Docker logs, or from a log file.


%prep
%setup -q -c


%install
install -m 0755 -D postfix_exporter %{buildroot}%{_bindir}/postfix-exporter
install -m 0644 -D -p %{SOURCE1} %{buildroot}%{_unitdir}/postfix-exporter.service
install -m 0644 -D -p %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/postfix-exporter


%pre
getent group postfix-exporter >/dev/null || groupadd -r postfix-exporter
getent passwd postfix-exporter >/dev/null || \
  useradd -r -d /dev/null -g postfix-exporter \
  -s /sbin/nologin -c "Postfix Prometheus Exporter" postfix-exporter


%post
%systemd_post postfix-exporter.service


%preun
%systemd_preun postfix-exporter.service


%postun
%systemd_postun postfix-exporter.service


%files
%doc README.md
%doc CHANGELOG.md
%license LICENSE
%config(noreplace) %{_sysconfdir}/sysconfig/postfix-exporter
%{_bindir}/postfix-exporter
%{_unitdir}/postfix-exporter.service


%changelog
* Fri Jul 25 2025 Michele Brodoloni <michele@exads.com> - 0.11.0-2
- Use package with systemd support

* Mon Jul 21 2025 Michele Brodoloni <michele@exads.com> - 0.11.0-1
- Initial release

