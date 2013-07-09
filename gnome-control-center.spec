%define _disable_ld_no_undefined 1
%define url_ver %(echo %{version}|cut -d. -f1,2)

%define gstapi	1.0
%define major	1
%define libname	%mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Summary:	GNOME control center
Name:		gnome-control-center
Version:	3.8.3
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
Url:		http://www.gnome.org/softwaremap/projects/control-center/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	desktop-file-utils
BuildRequires:	docbook-style-xsl
BuildRequires:	gnome-common
BuildRequires:	intltool
BuildRequires:	cups-devel
BuildRequires:	pkgconfig(cheese-gtk) >= 2.91.91.1
BuildRequires:	pkgconfig(colord) >= 0.1.8
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0) >= 2.23.0
BuildRequires:	pkgconfig(glib-2.0) >= 2.29.14
BuildRequires:	pkgconfig(gnome-bluetooth-1.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 3.1.0
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gnome-settings-daemon) >= 3.3.91
BuildRequires:	pkgconfig(goa-backend-1.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gstreamer-%{gstapi})
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(ibus-1.0)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libcanberra-gtk3) >= 0.13
BuildRequires:	pkgconfig(libgnome-menu-3.0)
BuildRequires:	pkgconfig(libgnomekbd) >= 2.91.91
BuildRequires:	pkgconfig(libgnomekbdui) >= 2.91.91
BuildRequires:	pkgconfig(libgtop-2.0)
BuildRequires:	pkgconfig(libnm-glib) >= 0.8.992
BuildRequires:	pkgconfig(libnm-glib-vpn) => 0.8.992
BuildRequires:	pkgconfig(libnm-util) >= 0.8.992
BuildRequires:	pkgconfig(libnm-gtk) >= 0.8.992
BuildRequires:	pkgconfig(libnotify) >= 0.7.3
BuildRequires:	pkgconfig(libpulse) >= 0.9.16
BuildRequires:	pkgconfig(libpulse-mainloop-glib) >= 0.9.16
#BuildRequires:	pkgconfig(libsocialweb-client)
BuildRequires:	pkgconfig(libwacom)
BuildRequires:	pkgconfig(libxklavier) >= 5.1
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(NetworkManager) >= 0.8.992
BuildRequires:	pkgconfig(polkit-gobject-1) >= 0.97
BuildRequires:	pkgconfig(pwquality)
BuildRequires:	pkgconfig(shared-mime-info)
BuildRequires:	pkgconfig(upower-glib) >= 0.9.1
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi) >= 1.2

Requires:	gnome-settings-daemon >= 2.21.5
Requires(post,postun):	shared-mime-info desktop-file-utils

%description
GNOME Control-center is a configuration tool for easily
setting up your GNOME environment.

%package -n %{devname}
Summary:	Development libraries, include files for GNOME control center
Group:		Development/GNOME and GTK+
Obsoletes:	%{_lib}gnome-window-settings-devel < 3.6.3-1

%description -n %{devname}
Development libraries, include files for GNOME Control Center

%prep
%setup -q
%apply_patches

%build

# Build egg-list-box
pushd egg-list-box
%configure
make
popd

%configure2_5x \
	--disable-static \
	--disable-scrollkeeper

#	--with-libsocialweb \
%make

%install
%makeinstall_std
rm -f %{buildroot}%{_datadir}/applications/mimeinfo.cache

%find_lang %{name}-2.0 --with-gnome --all-name

desktop-file-install --vendor="" \
	--remove-category="Application" \
	--remove-category="PersonalSettings" \
	--add-category="X-MandrivaLinux-System-Configuration-GNOME" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

%files -f %{name}-2.0.lang
%doc AUTHORS NEWS README
%{_sysconfdir}/xdg/autostart/gnome-sound-applet.desktop
%{_sysconfdir}/xdg/menus/gnomecc.menu
%{_libdir}/control-center-1/panels/libbackground.so
%{_libdir}/control-center-1/panels/libbluetooth.so
%{_libdir}/control-center-1/panels/libcolor.so
%{_libdir}/control-center-1/panels/libdate_time.so
%{_libdir}/control-center-1/panels/libdisplay.so
%{_libdir}/control-center-1/panels/libinfo.so
%{_libdir}/control-center-1/panels/libkeyboard.so
%{_libdir}/control-center-1/panels/libmouse-properties.so
%{_libdir}/control-center-1/panels/libonline-accounts.so
%{_libdir}/control-center-1/panels/libpower.so
%{_libdir}/control-center-1/panels/libprinters.so
%{_libdir}/control-center-1/panels/libregion.so
%{_libdir}/control-center-1/panels/libscreen.so
%{_libdir}/control-center-1/panels/libsound.so
%{_libdir}/control-center-1/panels/libuniversal-access.so
%{_libdir}/control-center-1/panels/libuser-accounts.so
%{_libdir}/control-center-1/panels/libwacom-properties.so
%{_libdir}/control-center-1/panels/libnetwork.so
%{_bindir}/gnome-control-center
%{_bindir}/gnome-sound-applet
%{_datadir}/applications/*
%{_datadir}/desktop-directories/*
%{_datadir}/gnome-control-center/
%{_datadir}/sounds/gnome/default/*
%{_datadir}/pixmaps/faces
%{_datadir}/polkit-1/actions/org.gnome.controlcenter.datetime.policy
%{_datadir}/polkit-1/actions/org.gnome.controlcenter.user-accounts.policy
%{_datadir}/polkit-1/rules.d/gnome-control-center.rules
%{_iconsdir}/hicolor/*/*/*
%{_mandir}/man?/*

%files -n %{devname}
%{_datadir}/pkgconfig/*
