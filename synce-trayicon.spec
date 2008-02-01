%define name	synce-trayicon
%define version 0.9.0
%define release %mkrel 8

Name:           %{name}
Summary: 	SynCE: Tray icon for GNOME 2
Version:        %{version}
Release:        %{release}

License:        MIT
Source: 	%{name}-%{version}.tar.bz2
Source10:	%{name}-16x16.png
Source11:	%{name}-32x32.png
Source12:	%{name}-48x48.png
URL: 		http://synce.sourceforge.net/
Group:          Communications

Buildroot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	libsynce-devel >= 0.9.0
BuildRequires:	librapi-devel
BuildRequires:	gtk2-devel atk-devel libgnomeui2-devel libgtop2.0-devel

%description
Synce-trayicon is part of the SynCE project:
  http://synce.sourceforge.net/

This application shows when a device is connected.

%prep
%setup -q

%build
%configure2_5x --with-librapi2=$RPM_BUILD_ROOT%{_prefix}
%make

%install
rm -fr %buildroot
%makeinstall

#menu
install -m 644 -D %{SOURCE10} $RPM_BUILD_ROOT/%{_miconsdir}/%{name}.png
install -m 644 -D %{SOURCE11} $RPM_BUILD_ROOT/%{_iconsdir}/%{name}.png
install -m 644 -D %{SOURCE12} $RPM_BUILD_ROOT/%{_liconsdir}/%{name}.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Synce-trayicon
Comment=SynCE: Tray icon for GNOME 2
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=TelephonyTools;Utility;GTK;GNOME;
EOF

%find_lang %name

%clean
rm -fr %buildroot

%post
%update_menus

%postun
%clean_menus

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog 
%{_bindir}/synce-trayicon
%{_datadir}/pixmaps/synce/synce-color-small.png
%{_datadir}/pixmaps/synce/synce-gray-small.png
%{_datadir}/synce/synce_trayicon_properties.glade
%{_miconsdir}/%name.png
%{_iconsdir}/%name.png
%{_liconsdir}/%name.png
%{_datadir}/applications/mandriva-%{name}.desktop

