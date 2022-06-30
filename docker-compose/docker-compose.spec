Name:           docker-compose
Version:        2.6.1
Release:        1
Summary:        Define and run multi-container applications with Docker

License:        ASL 2.0
URL:            https://docs.docker.com/compose/
Source0:        https://github.com/docker/compose/releases/download/v%{version}/docker-compose-Linux-%{_arch}
ExclusiveArch:  x86_64 aarch64

%description
Docker Compose relies on Docker Engine for any meaningful work, so make sure
you have Docker Engine installed either locally or remote, depending on your
setup.

%prep
# Nothing, just use the upstream binary build

%build
# Nothing, just use the upstream binary build

%install
install -D -p -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}

%doc

%changelog
* Thu Jun 30 2022 Matthias Saou <matthias@saou.eu> 2.6.1-1
- Update to 2.6.1.
- Add aarch64 arch.

* Tue Nov 23 2021 David Castañeda <edupr91@gmail.com> - 1.29.2-1
- Initial RPM release
