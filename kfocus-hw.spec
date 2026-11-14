%global commit 536acf3b28c0a68dff9c5573cb48541c84dff657

Name:           kfocus-hw
Version:        26.04.6
Release:        1%{?dist}
Summary:        Kubuntu Focus hardware configuration files
License:        GPL-2.0-or-later
URL:            https://github.com/eeickmeyer/kfocus-source
Source0:        https://github.com/eeickmeyer/kfocus-source/archive/%{commit}.tar.gz
BuildArch:      noarch
Requires:       kfocus-common >= 22.04.9

%description
Hardware configuration files and system hints for Kubuntu Focus systems.

%prep
%autosetup -n kfocus-source-%{commit}

%build

%install
install -d %{buildroot}%{_prefix}/lib/kfocus
cp -a package-hw/usr/lib/kfocus/conf \
    %{buildroot}%{_prefix}/lib/kfocus/
install -d %{buildroot}%{_datadir}
cp -a package-hw/usr/share/kfocus-hints \
    %{buildroot}%{_datadir}/

%files
%license COPYING
%{_prefix}/lib/kfocus/conf/
%{_datadir}/kfocus-hints/

%changelog
* Sat Nov 14 2026 Kubuntu Focus Team <support@kfocus.org> - 26.04.6-1
- Package hardware configuration and hint assets for Fedora
