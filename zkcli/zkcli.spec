%ifarch x86_64
%define platform amd64
%define source_id 0
%endif
%ifarch aarch64
%define platform arm64
%define source_id 1
%endif

Name: zkcli
Version: 0.4.0
Release: 1
License: MIT
URL: https://github.com/let-us-go/zkcli
Source0: https://github.com/let-us-go/zkcli/releases/download/v%{version}/zkcli-%{version}-linux-amd64.tar.gz
Source1: https://github.com/let-us-go/zkcli/releases/download/v%{version}/zkcli-%{version}-linux-arm64.tar.gz
Summary: An interactive Zookeeper client written in Go
ExclusiveArch: x86_64 aarch64


%description
An interactive Zookeeper client written in Go


%prep
%setup -T -n zkcli-%{version}-linux-%{platform} -q -b %{source_id}


%install
install -m 0755 -D zkcli %{buildroot}%{_bindir}/zkcli


%files
%{_bindir}/zkcli


%changelog
* Mon Apr 17 2023 Michele Brodoloni <michele@exads.com> - 0.4.0-1
- Initial release

