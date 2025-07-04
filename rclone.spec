%define		vendor_ver	1.70.1

Summary:	rsync for cloud storage
Name:		rclone
Version:	1.70.1
Release:	1
License:	MIT
Group:		Networking/Utilities
#Source0Download: https://github.com/rclone/rclone/releases
Source0:	https://github.com/rclone/rclone/releases/download/v%{version}/%{name}-v%{version}.tar.gz
# Source0-md5:	661c92815aedc9aa1c742f3ab77ab92b
# cd rclone-%{version}
# go mod vendor
# cd ..
# tar cJf rclone-vendor-%{version}.tar.xz rclone-v%{version}/vendor
Source1:	%{name}-vendor-%{vendor_ver}.tar.xz
# Source1-md5:	2340de7e25acef76189bd1df064d0d03
Patch0:		webdav-modtime.patch
URL:		https://rclone.org/
BuildRequires:	golang >= 1.23.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.009
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	_debugsource_packages

%description
Rclone is a command line program to sync files and directories to and
from different cloud storage providers.

%package -n bash-completion-rclone
Summary:	bash-completion for rclone
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-rclone
This package provides bash-completion for rclone.

%package -n fish-completion-rclone
Summary:	Fish completion for rclone command
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-rclone
Fish completion for rclone command.

%package -n zsh-completion-rclone
Summary:	Zsh completion for rclone command
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-rclone
Zsh completion for rclone command.

%prep
%setup -q -a1 -n %{name}-v%{version}
%patch -P0 -p1

%{__mv} %{name}-v%{vendor_ver}/vendor .

%{__mkdir_p} .go-cache

%build
%__go build -v -mod=vendor --ldflags "-X github.com/rclone/rclone/fs.Version=%{version}" -o bin/rclone

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{bash_compdir},%{fish_compdir},%{zsh_compdir}}

cp -p bin/rclone $RPM_BUILD_ROOT%{_bindir}
cp -p rclone.1 $RPM_BUILD_ROOT%{_mandir}/man1

$RPM_BUILD_ROOT%{_bindir}/rclone genautocomplete bash $RPM_BUILD_ROOT%{bash_compdir}/rclone
$RPM_BUILD_ROOT%{_bindir}/rclone genautocomplete fish $RPM_BUILD_ROOT%{fish_compdir}/rclone.fish
$RPM_BUILD_ROOT%{_bindir}/rclone genautocomplete zsh $RPM_BUILD_ROOT%{zsh_compdir}/_rclone

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTING.md MAINTAINERS.md MANUAL.md README.md
%attr(755,root,root) %{_bindir}/rclone
%{_mandir}/man1/rclone.1*

%files -n bash-completion-rclone
%defattr(644,root,root,755)
%{bash_compdir}/rclone

%files -n fish-completion-%{name}
%defattr(644,root,root,755)
%{fish_compdir}/rclone.fish

%files -n zsh-completion-%{name}
%defattr(644,root,root,755)
%{zsh_compdir}/_rclone
