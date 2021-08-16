%global commit 5ac483f9613430b4aa9d5a93877b346eff23b57e
%global gittag HEAD
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:             python-limelight
Version:          1.1.0
Release:          1.%{shortcommit}%{?dist}
Summary:          Python bindings for LimeLight API
License:          MIT
URL:              https://github.com/kenial/limelight_rest_wrapper
Source0:          https://github.com/kenial/limelight_rest_wrapper/archive/%{commit}.tar.gz
Patch0:           limelight_get_params_fix.patch
BuildArch:        noarch

%description
%{summary}.

%package -n python2-limelight
Summary:          %{summary}
BuildRequires:    python2-devel
Requires:         python2-requests

%description -n python2-limelight
%{summary}.

%package -n python3-limelight
Summary:          %{summary}
BuildRequires:    python3-devel
Requires:         python3-requests

%description -n python3-limelight
%{summary}.

%prep
%setup -q -n limelight_rest_wrapper-%{commit}
%patch0 -p0

%build
# Nothing to do...

%install
mv limelight_rest_wrapper.py __init__.py
mkdir -p %{buildroot}%{python3_sitelib}
cp -a . %{buildroot}%{python3_sitelib}/limelight
mkdir -p %{buildroot}%{python2_sitelib}
cp -a . %{buildroot}%{python2_sitelib}/limelight

%files -n python2-limelight
%license LICENSE
%doc README.md example.py
%{python2_sitelib}/limelight/

%files -n python3-limelight
%license LICENSE
%doc README.md example.py
%{python3_sitelib}/limelight/

%changelog
* Mon Aug 16 2021 Michele Brodoloni <michele@exads.com> - 1.1.0-1.5ac483f
- Initial release

