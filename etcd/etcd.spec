%ifarch x86_64
%define platform amd64
%define source_id 0
%endif
%ifarch aarch64
%define platform arm64
%define source_id 1
%endif

Name: etcd
Version: 3.4.34
Release: 1
License: ASL 2.0
URL: https://github.com/etcd-io/etcd
Source0: https://github.com/etcd-io/etcd/releases/download/v%{version}/etcd-v%{version}-linux-amd64.tar.gz
Source1: https://github.com/etcd-io/etcd/releases/download/v%{version}/etcd-v%{version}-linux-arm64.tar.gz
Source2: config.yml
Source3: etcd.service
Summary: Distributed reliable key-value store for the most critical data of a distributed system
ExclusiveArch: x86_64 aarch64
BuildRequires: systemd


%description
Distributed reliable key-value store for the most critical data of a distributed system.


%prep
%setup -T -n etcd-v%{version}-linux-%{platform} -q -b %{source_id}


%install
install -m 0755 -D etcd %{buildroot}%{_bindir}/etcd
install -m 0755 -D etcdctl %{buildroot}%{_bindir}/etcdctl
install -m 0644 -D -p %{SOURCE2} %{buildroot}%{_sysconfdir}/etcd/config.yml
install -m 0644 -D -p %{SOURCE3} %{buildroot}%{_unitdir}/etcd.service
install -m 0700 -d -p %{buildroot}%{_sharedstatedir}/etcd

%pre
getent group etcd >/dev/null || groupadd -r etcd
getent passwd etcd >/dev/null || \
  useradd -r -d /var/lib/etcd -g etcd \
  -s /sbin/nologin -c "etcd" etcd


%post
%systemd_post etcd.service


%preun
%systemd_preun etcd.service


%postun
%systemd_postun_with_restart etcd.service


%files
%config(noreplace) %attr(0640,root,etcd) %{_sysconfdir}/etcd/config.yml
%{_bindir}/etcd
%{_bindir}/etcdctl
%{_unitdir}/etcd.service
%dir %attr(0700,etcd,etcd) %{_sharedstatedir}/etcd
%doc README*
%doc Documentation


%changelog
* Wed Oct 23 2024 Michele Brodoloni <michele@exads.com> - 3.4.34-1
- Initial release v3.4.34


