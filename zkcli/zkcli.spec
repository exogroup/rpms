# Repository commit id
%define commit 1fb450f29d6072d3686ed430ab8c79c98dd32191
%define shortcommit %(c=%{commit}; echo ${c:0:7})

Name: zkcli
Version: 0.4.1
Release: 0.1.%{shortcommit}
License: MIT
URL: https://github.com/maxjustus/zkcli
# Fetching the source from a specific commit ID
Source0: zkcli-%{shortcommit}.tar.gz
Summary: An interactive Zookeeper client written in Go
ExclusiveArch: x86_64 aarch64
BuildRequires: golang


%description
An interactive Zookeeper client written in Go


%prep
# Setup for a specific commit
%autosetup -n zkcli-%{shortcommit}


%build
%gobuild -o zkcli


%install
# Install the binary into the build root
install -m 0755 -D zkcli %{buildroot}%{_bindir}/zkcli


%files
%{_bindir}/zkcli


%changelog
* Wed Mar 11 2026 Michele Brodoloni <michele@exads.com> - 0.4.1-1fb450f.1
- Update to v0.4.1, with recursive deleteall support

* Mon Apr 17 2023 Michele Brodoloni <michele@exads.com> - 0.4.0-1
- Initial release

