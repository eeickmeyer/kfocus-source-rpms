%global commit 536acf3b28c0a68dff9c5573cb48541c84dff657

Name:           kfocus-hw
Version:        26.04.6
Release:        4%{?dist}
Summary:        Kubuntu Focus hardware configuration files
License:        GPL-2.0-or-later
URL:            https://github.com/eeickmeyer/kfocus-source
Source0:        https://github.com/eeickmeyer/kfocus-source/archive/%{commit}.tar.gz
Source1:        kfocus-fand-setup
Source2:        kfocus-sleep-setup
BuildArch:      noarch
Requires:       kfocus-common >= 26.04.12~beta1-2
Requires(post): kfocus-common >= 26.04.12~beta1-2

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
install -Dpm 0755 %{SOURCE1} \
    %{buildroot}%{_prefix}/lib/kfocus/bin/kfocus-fand-setup
install -Dpm 0755 %{SOURCE2} \
    %{buildroot}%{_prefix}/lib/kfocus/bin/kfocus-sleep-setup

%post
%{_prefix}/lib/kfocus/bin/kfocus-fand-setup
%{_prefix}/lib/kfocus/bin/kfocus-sleep-setup

%postun
if [ "$1" -eq 0 ]; then
    profile=%{_datadir}/kfocus/kfocus_fand.d/fan_profile_db
    if [ -L "$profile" ]; then
        case "$(readlink "$profile")" in
            %{_prefix}/lib/kfocus/conf/dflt-usr_share_kfocus_kfocus_fand.d_fan_profile_db|\
            %{_prefix}/lib/kfocus/conf/m2g6-usr_share_kfocus_kfocus_fand.d_fan_profile_db)
                rm -f "$profile"
                ;;
        esac
    fi
fi

%files
%license COPYING
%{_prefix}/lib/kfocus/conf/
%{_prefix}/lib/kfocus/bin/kfocus-fand-setup
%{_prefix}/lib/kfocus/bin/kfocus-sleep-setup
%ghost %{_prefix}/lib/systemd/system-sleep/zsleep-kfocus
%{_datadir}/kfocus-hints/

%changelog
* Sat Nov 14 2026 Kubuntu Focus Team <support@kfocus.org> - 26.04.6-4
- Install the sleep hook that disables XHCI wake on supported models, which
  fixes s2idle failing to wake

* Sat Nov 14 2026 Kubuntu Focus Team <support@kfocus.org> - 26.04.6-3
- Require the corrected hardware-detection library before configuration

* Sat Nov 14 2026 Kubuntu Focus Team <support@kfocus.org> - 26.04.6-2
- Select the fan profile for supported hardware

* Sat Nov 14 2026 Kubuntu Focus Team <support@kfocus.org> - 26.04.6-1
- Package hardware configuration and hint assets for Fedora
