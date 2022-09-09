# Fix for wrong dist macro on el7
%if 0%{?rhel} == 7
  %define dist .el7
%endif

Name:             docker-distribution-auth
Version:          1.9.0
Release:          1%{?dist}
Summary:          Docker Registry 2 Authentication Server
License:          ASL 2.0
URL:              https://github.com/cesanta/docker_auth
# Created by prep-packages.sh
Source0:          docker-distribution-auth-%{version}.tar.gz
Source1:          docker-distribution-auth.service
Source99:         prep-packages.sh
BuildRequires:    golang >= 1.15
BuildRequires:    glibc-static


%description
Authentication server implementing the Docker Registry 2.0 token-based
authentication and authorization protocol.


%prep
%setup -q


%build
export GOPATH=$(pwd)
export GO111MODULE=on
function gobuild { go build -a -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -v -x "$@"; }
gobuild -a -o src/github.com/cesanta/docker_auth/auth_server


%install
install -m 0755 -D src/github.com/cesanta/docker_auth/auth_server/auth_server \
  %{buildroot}/usr/sbin/docker-distribution-auth
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/docker-distribution-auth.service
mkdir -p %{buildroot}/%{_sysconfdir}/docker-distribution/auth
cat > %{buildroot}/%{_sysconfdir}/docker-distribution/auth/config.yml << EOF
# See /usr/share/doc/docker-distribution-auth-*/examples/ files.
EOF


%pre
/usr/bin/getent group dockauth >/dev/null || /usr/sbin/groupadd -r dockauth
if ! /usr/bin/getent passwd dockauth >/dev/null; then
  /usr/sbin/useradd -r -g dockauth -M -N -d / -s /sbin/nologin -c "Docker Distribution Auth" dockauth
fi


%post
%systemd_post docker-distribution-auth.service


%preun
%systemd_preun docker-distribution-auth.service


%postun
%systemd_postun docker-distribution-auth.service


%files
%license LICENSE
%doc README.md examples docs/Backend_MongoDB.md docs/Labels.md docs/auth-methods.md
%{_bindir}/docker-distribution-auth
%{_unitdir}/docker-distribution-auth.service
%dir %{_sysconfdir}/docker-distribution
%dir %{_sysconfdir}/docker-distribution/auth
%ghost %config(noreplace) %{_sysconfdir}/docker-distribution-auth/config.yaml


%changelog
* Tue Jul 05 2022 Michele Brodoloni <michele@exads.com> - 1.9.0-1
- New version 1.9.0

