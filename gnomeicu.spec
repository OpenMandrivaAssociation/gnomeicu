%define version 0.99.16

%define enable_applet 1
%{?_with_applet: %define enable_applet 1}

%define enable_socks 0
#{?_with_plf: #define enable_socks 1}

Name:		gnomeicu
Version:	%{version}
Release:	%mkrel 1
License:	GPL
Summary:	Gnome ICQ communications program 
Group:		Networking/Instant messaging
URL:		http://gnomeicu.sourceforge.net
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

Source:		http://prdownloads.sourceforge.net/gnomeicu/%{name}-%{version}.tar.bz2
# Icon themes from http://gnomeicu.sf.net/themes/
Source10:	%{name}-eureka.tar.bz2
Source11:	%{name}-mugz.tar.bz2
Source12:	%{name}-penguin.tar.bz2

# (fc) 0.98.126-2mdk use DTD compliant OMF file
Patch0:		gnomeicu-0.98.126-omffix.patch
Patch2:		gnomeicu-0.99.14-fix-str-fmt.patch
Requires(pre):		scrollkeeper >= 0.3.5
Requires(pre):		GConf2 >= 2.3.3
BuildRequires:	imagemagick
BuildRequires:	gdbm-devel
BuildRequires:	scrollkeeper >= 0.3.5
BuildRequires:	libgnomeui2-devel
BuildRequires:	libglade2.0-devel
BuildRequires:	gtkspell-devel >= 2.0.4
BuildRequires:	perl-XML-Parser
BuildRequires:	automake
BuildRequires:	intltool
%if %enable_applet
BuildRequires: gnome-panel-devel
%endif

%if %enable_socks
BuildRequires:	socks5-devel
%endif

%description
GnomeICU is a clone of Mirabilis' popular ICQ.
The original source was taken from Matt Smith's mICQ.

This GTK2 version includes:
- server-side storage
- file send
- contact history
- invisible and ignore lists
- command line interface capability
- icon themes

%if 0
*** Build Options:
--with plf    Enable SOCKSv5 support (default disabled)
                (Get it from PLF: http://plf.zarb.org/)
%endif

%if %enable_applet
%package applet
Summary: Applet for GnomeICU ICQ client
Group: %{group}
Requires: %{name} = %{version}-%{release}

%description applet
GnomeICU is a clone of Mirabilis' popular ICQ.

This package allows GnomeICU to be embedded in GNOME panel.
%endif


%prep
%setup -q
%patch0 -p1 -b .omffix
%patch2 -p0

%build
%configure2_5x --disable-schemas-install \
%if %enable_applet
	--enable-applet \
%endif
%if %enable_socks
	--enable-socks5 \
%endif

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# convert source icon into mdk menu icons
mkdir -p $RPM_BUILD_ROOT%{_iconsdir} \
	 $RPM_BUILD_ROOT%{_liconsdir} \
	 $RPM_BUILD_ROOT%{_miconsdir}
install -m 0644         %name.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
convert -geometry 32x32 %name.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert -geometry 16x16 %name.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

# icon themes
echo 'Default icons' > $RPM_BUILD_ROOT%{_datadir}/gnomeicu/icons/Default/gnomeicu-info
tar --bzip2 -xf %{SOURCE10} -C $RPM_BUILD_ROOT%{_datadir}/gnomeicu/icons/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnomeicu/icons/mugz
tar --bzip2 -xf %{SOURCE11} -C $RPM_BUILD_ROOT%{_datadir}/gnomeicu/icons/mugz
tar --bzip2 -xf %{SOURCE12} -C $RPM_BUILD_ROOT%{_datadir}/gnomeicu/icons/
find $RPM_BUILD_ROOT%{_datadir}/gnomeicu/icons/ -type d -print0 | xargs -0 chmod 0755
find $RPM_BUILD_ROOT%{_datadir}/gnomeicu/icons/ -type f -print0 | xargs -0 chmod 0644

%find_lang %name --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%update_scrollkeeper
%post_install_gconf_schemas gnomeicu
%endif

%preun
%preun_uninstall_gconf_schemas gnomeicu

%if %mdkversion < 200900
%postun
%clean_menus
%clean_scrollkeeper
%endif

%files -f %name.lang
%defattr(-,root,root,755)
%doc AUTHORS ChangeLog COPYING CREDITS INSTALL MAINTAINERS NEWS README* TODO
%config(noreplace) %{_sysconfdir}/sound/events/GnomeICU.soundlist
%{_sysconfdir}/gconf/schemas/gnomeicu.schemas
%{_bindir}/%name
%{_bindir}/%name-client
%{_datadir}/applications/*.desktop
%{_datadir}/%name
%{_datadir}/omf/*
%{_datadir}/pixmaps/*
%{_datadir}/sounds/*
%{_iconsdir}/%name.png
%{_liconsdir}/%name.png
%{_miconsdir}/%name.png

%if %enable_applet
%files applet
%defattr(-,root,root,755)
%{_libdir}/bonobo/servers/*.server
%{_libexecdir}/gnomeicu-applet
%{_datadir}/gnome-2.0/ui/*.xml
%endif
