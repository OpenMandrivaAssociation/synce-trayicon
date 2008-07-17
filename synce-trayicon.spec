%define schemas		%{name}

%define svn		3510
%define rel		1
%if %svn
%define release		%mkrel 0.%svn.%rel
%define distname	%name-%svn.tar.lzma
%define	dirname		trayicon
%else
%define release		%mkrel %rel
%define distname	%name-%version.tar.gz
%define dirname		%name-%version
%endif

Name:           synce-trayicon
Summary: 	SynCE tray icon for GNOME
Version:        0.12
Release:        %{release}
License:        MIT
Source0: 	%{distname}
Source10:	%{name}-16x16.png
Source11:	%{name}-32x32.png
Source12:	%{name}-48x48.png
URL: 		http://synce.sourceforge.net/
Group:          Communications
Buildroot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libsynce-devel
BuildRequires:	librapi-devel
BuildRequires:	libglade2-devel
BuildRequires:	gtk2-devel
BuildRequires:	atk-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	libgtop2.0-devel
BuildRequires:	librra-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	hal-devel
BuildRequires:	gnome-keyring-devel
BuildRequires:	libnotify-devel
BuildRequires:	liborange-devel
BuildRequires:	gnome-common
BuildRequires:	intltool

%description
Synce-trayicon is part of the SynCE project. This application provides
an icon in the system tray that shows when a device is connected and
lets you perform a variety of operations on connected devices.

%prep
%setup -q -n %{dirname}

%build
%if %svn
./autogen.sh
%endif
%configure2_5x --with-librapi2=%{buildroot}%{_prefix} --disable-schemas-install --enable-notify
%make

%install
rm -rf %{buildroot}
%makeinstall

#icons
install -m 644 -D %{SOURCE10} %{buildroot}/%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m 644 -D %{SOURCE11} %{buildroot}/%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m 644 -D %{SOURCE12} %{buildroot}/%{_iconsdir}/hicolor/48x48/apps/%{name}.png

#menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Synce-trayicon
Comment=SynCE tray icon for GNOME
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=TelephonyTools;Utility;GTK;GNOME;
EOF

# XDG autostart
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart
cat > %{buildroot}%{_sysconfdir}/xdg/autostart/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Exec=synce-trayicon
Name=SynCE tray icon (GNOME)
Terminal=false
Type=Application
StartupNotify=false
X-KDE-autostart-phase=2
X-KDE-autostart-after=panel
EOF

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
%{_sysconfdir}/xdg/autostart/mandriva-%{name}.desktop
%{_mandir}/man1/*.1*
%{_iconsdir}/hicolor/*/apps/*.png
%{_datadir}/applications/mandriva-%{name}.desktop

