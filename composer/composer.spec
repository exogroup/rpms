Name:          composer
Version:       2.5.5
Summary:       Dependency Management for PHP
Release:       1
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
* Fri May 19 2023 Matthias Saou <matthias@saou.eu> 2.5.5-1
- Update to 2.5.5 for PHP 8 compatibility.

* Tue May 04 2021 Michał Lisowski <michal@exads.com> - 2.0.13-1
- Initial RPM release

