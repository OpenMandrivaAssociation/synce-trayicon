Name:		synce-trayicon
Summary:	SynCE tray icon for GNOME
Version:	0.15
Release:	4
License:	MIT
Source0:	http://downloads.sourceforge.net/synce/%{name}-%{version}.tar.gz
Patch1:		synce-trayicon-0.15-libnotify0.7.patch
Source10:	%{name}-16x16.png
Source11:	%{name}-32x32.png
Source12:	%{name}-48x48.png
URL:		http://synce.sourceforge.net/
Group:		Communications
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libsynce-devel
BuildRequires:	librapi-devel
BuildRequires:	gtk2-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	libgtop2.0-devel
BuildRequires:	librra-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	hal-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libnotify-devel
BuildRequires:	liborange-devel
BuildRequires:	libgsf-devel
BuildRequires:	intltool
BuildRequires:	desktop-file-utils
BuildRequires:	libxml2-devel
BuildRequires:	unshield-devel
BuildRequires:	libGConf2-devel GConf2

%description
Synce-trayicon is part of the SynCE project. This application provides
an icon in the system tray that shows when a device is connected and
lets you perform a variety of operations on connected devices.

%prep
%setup -qn %{name}-%{version}
%patch1 -p0

#use HAL by default
sed -i s/"<default>o<"/"<default>h<"/"" data/synce-trayicon.schemas.in

%build
%configure2_5x --disable-schemas-install
%make

%install
rm -rf %{buildroot}
%makeinstall_std

#icons
install -m 644 -D %{SOURCE10} %{buildroot}/%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m 644 -D %{SOURCE11} %{buildroot}/%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m 644 -D %{SOURCE12} %{buildroot}/%{_iconsdir}/hicolor/48x48/apps/%{name}.png

desktop-file-install \
  --add-category="TelephonyTools" \
  --remove-key="Encoding" \
  --remove-key="Version" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# XDG autostart
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart
mv %{buildroot}%{_datadir}/gnome/autostart/synce-trayicon-autostart.desktop %{buildroot}%{_sysconfdir}/xdg/autostart/synce-trayicon-autostart.desktop

rm -f %{buildroot}%{_iconsdir}/hicolor/icon-theme.cache

%find_lang %{name}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%post_install_gconf_schemas %{schemas}
%endif

%preun
%preun_uninstall_gconf_schemas %{schemas}

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog 
%{_bindir}/%{name}
%{_datadir}/synce/synce_trayicon_properties.glade
%{_libdir}/%{name}
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%{_sysconfdir}/xdg/autostart/synce-trayicon-autostart.desktop
%{_mandir}/man1/*.1*
%{_iconsdir}/hicolor/*/apps/*.png
%{_datadir}/applications/%{name}.desktop

