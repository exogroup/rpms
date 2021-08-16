%global pypi_name edgecast

%if 0%{?fedora}
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        1.0.2
Release:        2%{?dist}
Summary:        Convenient EdgeCast CDN management for Python

License:        Apache
URL:            https://github.com/iconfinder/edgecast
Source0:        https://files.pythonhosted.org/packages/source/e/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Patch0:         %{name}-get_origins.patch
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Provides:       python2-%{pypi_name}

%description
Convenient EdgeCast CDN management for Python.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Convenient EdgeCast CDN management for Python
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description -n python3-%{pypi_name}
Convenient EdgeCast CDN management for Python.
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
%doc python2/README.rst
%{python2_sitelib}/django_edgecast
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc python3/README.rst
%{python3_sitelib}/django_edgecast
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.egg-info
%endif

%changelog
* Mon May 13 2019 Michał Lisowski <michal@exads.com> - 1.0.2-2
- Add patch that add support for getting all origins

* Tue Apr 17 2018 Michał Lisowski <michal@exads.com> - 1.0.2-1
- Initial release

