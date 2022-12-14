%ifarch x86_64
%define platform amd64
%define source_id 0
%endif
%ifarch aarch64
%define platform arm64
%define source_id 1
%endif

Name: frp
Version: 0.45.0
Release: 1
License: ASL 2.0
URL: https://github.com/fatedier/frp
Source0: https://github.com/fatedier/frp/releases/download/v%{version}/frp_%{version}_linux_amd64.tar.gz
Source1: https://github.com/fatedier/frp/releases/download/v%{version}/frp_%{version}_linux_arm64.tar.gz
Source2: frps.service
Source3: frps.ini
Source4: frpc.ini
Summary: Fast reverse proxy to expose a server behind NAT/firewall to the internet
ExclusiveArch: x86_64 aarch64
BuildRequires: systemd


%description
FRP is a fast reverse proxy which allows exposing a server behind NAT/firewall
to the internet. It supports TCP and UDP, as well as HTTP and HTTPS protocols,
where requests can be forwarded to internal services by domain name.


%package server
Summary: %{summary}


%description server
FRP is a fast reverse proxy which allows exposing a server behind NAT/firewall
to the internet. It supports TCP and UDP, as well as HTTP and HTTPS protocols,
where requests can be forwarded to internal services by domain name.
This is the server package.


%package client
Summary: %{summary}


%description client
FRP is a fast reverse proxy which allows exposing a server behind NAT/firewall
to the internet. It supports TCP and UDP, as well as HTTP and HTTPS protocols,
where requests can be forwarded to internal services by domain name.
This is the client package.


%prep
%setup -T -n frp_%{version}_linux_%{platform} -q -b %{source_id}


%install
mkdir -p %{buildroot}%{_sysconfdir}/frp
mkdir -p %{buildroot}%{_var}/log/frp
install -m 0755 -D frps %{buildroot}%{_bindir}/frps
install -m 0755 -D frpc %{buildroot}%{_bindir}/frpc
install -m 0644 -D %{SOURCE2} %{buildroot}%{_unitdir}/frps.service
install -m 0644 -D %{SOURCE3} %{buildroot}%{_sysconfdir}/frp/frps.ini
install -m 0644 -D %{SOURCE4} %{buildroot}%{_sysconfdir}/frp/frpc.ini


%pre server
getent group frp >/dev/null || groupadd -r frp
getent passwd frp >/dev/null || \
  useradd -r -d /dev/null -g frp \
  -s /sbin/nologin -c "Fast Reverse Proxy" frp


%files server
%doc frps.ini frps_full.ini
%license LICENSE
%dir %{_sysconfdir}/frp/
%dir %attr(0755,frp,frp) %{_var}/log/frp/
%config(noreplace) %{_sysconfdir}/frp/frps.ini
%{_bindir}/frps
%{_unitdir}/frps.service


%files client
%doc frpc.ini frpc_full.ini
%license LICENSE
%dir %{_sysconfdir}/frp/
%config(noreplace) %{_sysconfdir}/frp/frpc.ini
%{_bindir}/frpc


%post server
%systemd_post frps.service


%preun server
%systemd_preun frps.service


%postun server
%systemd_postun frps.service


%changelog
* Tue Dec 13 2022 Michele Brodoloni <michele@exads.com> - 0.45.0-1
- Initial release 0.45.0


