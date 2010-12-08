%define schemas		%{name}

%define svn		0
%define rel		2
%if %svn
%define release		%mkrel 0.%svn.%rel
%define distname	%name-%svn.tar.xz
%define	dirname		trayicon
%else
%define release		%mkrel %rel
%define distname	%name-%version.tar.gz
%define dirname		%name-%version
%endif

Name:		synce-trayicon
Summary:	SynCE tray icon for GNOME
Version:	0.15
Release:	%{release}
License:	MIT
Source0:	http://downloads.sourceforge.net/synce/%{distname}
# Use autoreconf rather than gnome-autogen.sh as it seems to fail on
# the buildsystem, even though it works in iurt... - AdamW 2008/07
Patch0:		synce-trayicon-3893-autogen.patch
Source10:	%{name}-16x16.png
Source11:	%{name}-32x32.png
Source12:	%{name}-48x48.png
URL:		http://synce.sourceforge.net/
Group:		Communications
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libsynce-devel
BuildRequires:	librapi-devel
#BuildRequires:	libglade2-devel
BuildRequires:	gtk2-devel
BuildRequires:	atk-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	libgtop2.0-devel
BuildRequires:	librra-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	hal-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libnotify-devel
BuildRequires:	liborange-devel
BuildRequires:	libgsf-devel
#BuildRequires:	gnome-common
BuildRequires:	intltool
BuildRequires:	desktop-file-utils

%description
Synce-trayicon is part of the SynCE project. This application provides
an icon in the system tray that shows when a device is connected and
lets you perform a variety of operations on connected devices.

%prep
%setup -q -n %{dirname}
%if %svn
%patch0 -p1 -b .autogen
%endif

%build

#use HAL by default
sed -i s/"<default>o<"/"<default>h<"/"" data/synce-trayicon.schemas.in

%if %svn
./autogen.sh
libtoolize --copy --force
aclocal -I m4
autoheader
autoconf -f
automake -fa
%endif
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

