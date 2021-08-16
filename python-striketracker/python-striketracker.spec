%global pypi_name striketracker

%if 0%{?fedora}
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        0.5.2
Release:        2%{?dist}
Summary:        Command line interface to the Highwinds CDN

License:        MIT
URL:            https://github.com/Highwinds/striketracker
Source0:        https://files.pythonhosted.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Patch0:         %{name}-get_hosts.patch
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python-requests
Requires:       python-yaml

Provides:       python2-%{pypi_name}

%description
Python client and command line interface to the Highwinds CDN.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Python client and command line interface to the Highwinds CDN
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3-requests
Requires:       python3-yaml

%description -n python3-%{pypi_name}
Python client and command line interface to the Highwinds CDN.
%endif


%prep
%setup -qc -n %{pypi_name}-%{upstream_version}
%patch0 -p0
mv %{pypi_name}-%{upstream_version} python2

%if 0%{?with_python3}
cp -a python2 python3
%endif


%build
pushd python2
%{__python2} setup.py build
popd
%if 0%{?with_python3}
pushd python3
%{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python3}
pushd python3
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

pushd python2
%{__python2} setup.py install --skip-build --root %{buildroot}
popd


%files
%{_bindir}/striketracker
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.egg-info
%endif

%changelog
* Mon May 13 2019 Michał Lisowski <michal@exads.com> - 0.5.2-2
- Add patch that add support for getting all hosts

* Wed Apr 11 2018 Michał Lisowski <michal@exads.com> - 0.5.2-1
- Initial release

