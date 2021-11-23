Name:           docker-compose
Version:        1.29.2
Release:        1%{?dist}
Summary:        Define and run multi-container applications with Docker

License:        ASL 2.0
URL:            https://docs.docker.com/compose/
Source0:        https://github.com/docker/compose/releases/download/%{version}/docker-compose-Linux-x86_64

%description
Docker Compose relies on Docker Engine for any meaningful work, so make sure
you have Docker Engine installed either locally or remote, depending on your
setup.

%prep
cp %{SOURCE0} .

%build
# Nothing, just use the upstream binary build


%install
install -D -p -m 755 docker-compose-Linux-x86_64  %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}

%doc

%changelog
* Tue Nov 23 2021 David Castañeda <edupr91@gmail.com> - 1.29.2-1
- Initial RPM release
