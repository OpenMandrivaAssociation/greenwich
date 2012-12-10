%define version	0.8.2
%define release  %mkrel 3

Name: 	 	greenwich
Summary: 	A graphical whois client
Version: 	%{version}
Release: 	%{release}
Source:		http://jodrell.net/files/greenwich/%{name}-%{version}.tar.gz
URL:		http://jodrell.net/projects/greenwich/
License:	GPLv2+
Group:		Networking/Other
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	imagemagick
# may be used but not crucial (according to author)
Suggests:	perl-IP-Country
Requires(post,preun):	GConf2 >= 2.3.3
BuildArch:	noarch

%description
Greenwich is a graphical whois client for GNOME. It is written in Perl
and makes use of the GNOME bindings for Perl.

Greenwich transparently handles almost all gTLDs, first- and
second-level ccTLDs and whois servers run by private domain registries
(like CentralNic).  It can also do lookups against IP addresses.

%prep
%setup -q

# fix file permissions
find -type f -perm +0111 -print0 | xargs -0 -r file | grep -v executable | cut -d: -f1 | xargs -r chmod -x

%build
./configure --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall mandir=$RPM_BUILD_ROOT%{_mandir}/man1

%find_lang %name

#menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{name}
Icon=%{name}
Name=Greenwich
Comment=Whois client
Categories=Network;
EOF

#icons
mkdir -p $RPM_BUILD_ROOT%{_iconsdir} \
         $RPM_BUILD_ROOT%{_miconsdir}
install -m 644 -D       share/greenwich.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
convert -geometry 32x32 share/greenwich.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert -geometry 16x16 share/greenwich.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

#install schemas into gconf later
install -m 644 -D share/greenwich.schema $RPM_BUILD_ROOT%{_sysconfdir}/gconf/schemas/greenwich.schemas

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%post_install_gconf_schemas greenwich
%endif

%preun
%preun_uninstall_gconf_schemas "$1"

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files -f %name.lang
%defattr(-,root,root)
%doc ChangeLog LICENSE README
%{_sysconfdir}/gconf/schemas/*.schemas
%{_bindir}/*
/usr/lib/greenwich
%{_datadir}/%name
%{_datadir}/applications/*
#%{_datadir}/pixmaps/*
%{_mandir}/man1/*
%{_iconsdir}/*/*/apps/%name.png
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png



%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0.8.2-3mdv2011.0
+ Revision: 619254
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0.8.2-2mdv2010.0
+ Revision: 429322
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Tue Jul 01 2008 Austin Acton <austin@mandriva.org> 0.8.2-1mdv2009.0
+ Revision: 230497
- new version
- add icons
- fix license
- drop patch
- suggests perl IP

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - use %%post_install_gconf_schemas/%%preun_uninstall_gconf_schemas

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Dec 19 2007 Thierry Vignaud <tv@mandriva.org> 0.8.1-1mdv2008.1
+ Revision: 133083
- further fix file list for x86_64
- fix file list on x86_64
- auto-convert XDG menu entry
- fix prereq on gconf2
- kill re-definition of %%buildroot on Pixel's request
- use %%mkrel
- import greenwich


* Wed Aug 24 2005 Austin Acton <austin@mandriva.org> 0.8.1-1mdk
- 0.8.1
- source URL

* Mon Oct 26 2004 Austin Acton <austin@mandrake.org> 0.8.0-1mdk
- 0.8.0

* Wed Jun 30 2004 Austin Acton <austin@mandrake.org> 0.7.1-1mdk
- 0.7.1
- add language files
- new menu

* Sun Dec 14 2003 Abel Cheung <deaddog@deaddog.org> 0.6.2-1mdk
- New version
- Convert icon with ImageMagick
- Use description from original spec
- TODO: mark localized files

* Sat Jun 7 2003 Austin Acton <aacton@yorku.ca> 0.5.2-2mdk
- fix requires perl(the) (Michael Reinsch)

* Thu Jun 5 2003 Austin Acton <aacton@yorku.ca> 0.5.2-1mdk
- 0.5.2

* Tue Apr 1 2003 Austin Acton <aacton@yorku.ca> 0.5.1-1mdk
- initial package
