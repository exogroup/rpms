# Fix "Empty %files file" debugsourcefiles.list (we have no sources, duh!)
%define _debugsource_template %{nil}
%global debug_package %{nil}
%global __strip /bin/true
%global _build_id_links none

Summary: Reverse proxy providing authentication with OAuth2 providers
Name: oauth2-proxy
Version: 7.15.6
Release: 1
License: MIT
URL: https://github.com/oauth2-proxy/oauth2-proxy
Source0: %{url}/releases/download/v%{version}/%{name}-v%{version}.linux-amd64.tar.gz
Source1: https://raw.githubusercontent.com/oauth2-proxy/oauth2-proxy/v%{version}/LICENSE
ExclusiveArch: x86_64

%description
oauth2-proxy is a reverse proxy and static file server that provides
authentication using providers such as Google or GitHub, to validate accounts
by email, domain or group. Prebuilt upstream release binary.


%prep
echo '91b3e86d9c2de679a516e6696704e3fd1acf67e8b8f7be77b618f086f72fb1f0  %{SOURCE0}' | sha256sum -c -
%setup -q -n %{name}-v%{version}.linux-amd64
cp -p %{SOURCE1} LICENSE


%build
# Nothing to see here...


%install
install -D -p -m 0755 %{name} %{buildroot}%{_bindir}/%{name}


%check
%{buildroot}%{_bindir}/%{name} --version | grep -qF 'v%{version} '


%files
%license LICENSE
%{_bindir}/%{name}


%changelog
* Tue Nov 24 2026 Diogo <diogo@exads.com> 7.15.6-1
- Initial RPM release.
