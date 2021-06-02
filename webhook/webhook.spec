# Work around 'ERROR: No build ID note found in ...'
%undefine _missing_build_ids_terminate_build

Summary: Lightweight incoming webhook server to run shell commands
Name: webhook
Version: 2.8.0
Release: 2
License: MIT
URL: https://github.com/adnanh/webhook
Source0: https://github.com/adnanh/webhook/releases/download/%{version}/webhook-linux-amd64.tar.gz
Source1: webhook.service
Source2: webhook.sysconfig
ExclusiveArch: x86_64
BuildRequires: systemd
%{?systemd_requires}

%description
Lightweight configurable tool written in Go, that allows you to easily create
HTTP endpoints (hooks) on your server, which you can use to execute configured
commands. You can also pass data from the HTTP request (such as headers,
payload or query variables) to your commands. webhook also allows you to
specify rules which have to be satisfied in order for the hook to be triggered.


%prep
%setup -q -n webhook-linux-amd64


%build
# Nothing, we are naughty and just use the upstream binary build


%install
install -D -p -m 0755 webhook %{buildroot}%{_bindir}/webhook
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/webhook.service
install -D -p -m 0644 %{SOURCE2} %{buildroot}/etc/sysconfig/webhook
mkdir -p %{buildroot}/etc/webhook
touch %{buildroot}/etc/webhook/hooks.json
mkdir -p %{buildroot}/var/{lib,log}/webhook


%check
# Source file name doesn't contain the version, so prevent using the wrong one
./webhook -version | grep -E '^webhook version %{version}$'


%pre
getent group webhook >/dev/null || groupadd -r webhook
getent passwd webhook >/dev/null || \
  useradd -r -d /var/lib/webhook -g webhook \
  -s /sbin/nologin -c "webhook" webhook

%post
%systemd_post webhook.service

%preun
%systemd_preun webhook.service

%postun
%systemd_postun_with_restart webhook.service


%files
%{_bindir}/webhook
%config(noreplace) /etc/sysconfig/webhook
%attr(0750,root,webhook) %dir /etc/webhook
%ghost %config /etc/webhook/hooks.json
%{_unitdir}/webhook.service
%attr(0770,webhook,webhook) %dir /var/lib/webhook
%attr(0770,webhook,webhook) %dir /var/log/webhook


%changelog
* Wed Jun  2 2021 Matthias Saou <matthias@saou.eu> 2.8.0-2
- Update lib dir so that webhook user can write to it, add log dir.

* Mon May 31 2021 Matthias Saou <matthias@saou.eu> 2.8.0-1
- Initial RPM release.

