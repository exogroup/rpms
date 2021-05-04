Name:          composer
Version:       2.0.13
Summary:       Dependency Management for PHP
Release:       1%{?dist}
License:       MIT
URL:           https://getcomposer.org/
Source0:       https://github.com/composer/composer/releases/download/%{version}/composer.phar
BuildArch:     noarch

%description
Dependency Management for PHP.


%prep
# Nothing to do here


%build
# Nothing to do here


%install
install -D -p -m 755 %{SOURCE0} %{buildroot}%{_bindir}/%{name}


%files
%{_bindir}/%{name}


%changelog
* Tue May 04 2021 Michał Lisowski <michal@exads.com> - 2.0.13-1
- Initial RPM release

