Summary: Command to speed up a subsequent "swapoff" command
Name: deswappify
Version: 0.0
Release: 1
License: Public Domain
URL: https://gist.github.com/salehi/d49490e17b03d8544689f1645a99d062
Source0: https://gist.github.com/salehi/d49490e17b03d8544689f1645a99d062/raw/0a9f48a2cbf4b4af33eec38a6a6d9e9d98f7509c/deswappify.pl
Source1: deswappify-off-on
BuildArch: noarch

%description
Command to speed up a subsequent "swapoff" command.


%prep
# Nope


%build
# Also nope


%install
install -D -p -m 0755 %{SOURCE0} %{buildroot}%{_sbindir}/deswappify
install -D -p -m 0755 %{SOURCE1} %{buildroot}%{_sbindir}/deswappify-off-on


%files
%{_sbindir}/deswappify
%{_sbindir}/deswappify-off-on


%changelog
* Thu Apr 10 2025 Matthias Saou <matthias@saou.eu> 0.0-1
- Initial RPM release.

