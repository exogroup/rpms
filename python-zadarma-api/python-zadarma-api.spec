%global commit 9e7a6d709ab097f3784a8301ce77b3ec45af6f32
%global gittag HEAD
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%if 0%{?rhel} == 7
%define dist .el7
%endif

Name:             python-zadarma-api
Version:          1.1.0
Release:          1.%{shortcommit}%{?dist}
Summary:          Python bindings for the Zadarma API
License:          MIT
URL:              https://github.com/zadarma/user-api-py-v1
Source0:          https://github.com/zadarma/user-api-py-v1/archive/%{commit}/user-api-py-v1-%{version}-%{shortcommit}.tar.gz
BuildArch:        noarch

%description
%{summary}.

%if 0%{?rhel} == 7
%package -n python2-zadarma-api
Summary:          %{summary}
BuildRequires:    python2-devel
Requires:         python2-requests

%description -n python2-zadarma-api
%{summary}.
%endif

%package -n python3-zadarma-api
Summary:          %{summary}
BuildRequires:    python3-devel
Requires:         python3-requests

%description -n python3-zadarma-api
%{summary}.

%prep
%setup -q -n user-api-py-v1-%{commit}

%build
# Nothing to do...

%install
%if 0%{?rhel} == 7
mkdir -p %{buildroot}%{python2_sitelib}
cp -a zadarma %{buildroot}%{python2_sitelib}/
%endif
mkdir -p %{buildroot}%{python3_sitelib}
cp -a zadarma %{buildroot}%{python3_sitelib}/

%if 0%{?rhel} == 7
%files -n python2-zadarma-api
%license LICENSE
%doc README.md examples/example.py
%{python2_sitelib}/zadarma/
%endif

%files -n python3-zadarma-api
%license LICENSE
%doc README.md examples/example.py
%{python3_sitelib}/zadarma/
