Summary:	rsync for cloud storage
Name:		rclone
Version:	1.55.0
Release:	1
License:	MIT
Group:		Networking/Utilities
#Source0Download: https://github.com/rclone/rclone/releases
Source0:	https://github.com/rclone/rclone/releases/download/v%{version}/%{name}-v%{version}.tar.gz
# Source0-md5:	16389b8398ecf5c0b9942dbfc956ff88
# cd rclone-%{version}
# go mod vendor
# cd ..
# tar cJf rclone-vendor-%{version}.tar.xz rclone-v%{version}/vendor
Source1:	%{name}-vendor-%{version}.tar.xz
# Source1-md5:	9de5b2c00f12d4f082c0c24f7e3e01d4
URL:		https://rclone.org/
BuildRequires:	golang >= 1.14
BuildRequires:	rpmbuild(macros) >= 2.005
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%{ix86} %{x8664} %{arm} aarch64 mips64 mips64le ppc64 ppc64le s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_debugsource_packages	0

%description
Rclone is a command line program to sync files and directories to and
from different cloud storage providers.

%prep
%setup -q -b1 -n %{name}-v%{version}

%{__mkdir_p} .go-cache

%build
GOCACHE="$(pwd)/.go-cache" go build -v -mod=vendor --ldflags "-X github.com/rclone/rclone/fs.Version=%{version}" -o bin/rclone

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}

cp -p bin/rclone $RPM_BUILD_ROOT%{_bindir}
cp -p rclone.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTING.md MAINTAINERS.md MANUAL.md README.md
%attr(755,root,root) %{_bindir}/rclone
%{_mandir}/man1/rclone.1*
