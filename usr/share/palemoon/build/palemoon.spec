%define dummy_package   0
Name:		palemoon
Version:	27.7.1
Release:	1
Summary:	A file synchronization utility

Group:	Networking/Web
License:	GPL 3.0 
URL:		http://bgstack15.wordpress.com/
Source0: palemoon.tgz
Source1:	https://github.com/MoonchildProductions/Pale-Moon/archive/%{version}_Release.tar.gz

Packager:	Bgstack15 <bgstack15@gmail.com>
Buildarch:	x86_64
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf213
BuildRequires:	bzip2-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	gcc49
BuildRequires:	gtk2-devel
BuildRequires:	libXt-devel
BuildRequires:	mesa-libGL-devel
BuildRequires:	nspr-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	sqlite-devel
BuildRequires:	yasm
BuildRequires:	zlib-devel
BuildRequires: pkgconfig(gtk+-2.0)
BuildRequires: pkgconfig(vpx)
BuildRoot:     %{_tmppath}/%{name}-%{version}
Requires:   hicolor-icon-theme
Provides:   mimehandler(application/x-xpinstall)

# Reference:
#    https://math-linux.com/linux/rpm/article/how-to-turn-off-avoid-brp-python-bytecompile-script-in-a-spec-file
#    https://build.opensuse.org/package/show/network/palemoon
#    http://ftp.nluug.nl/pub/os/Linux/distr/pclinuxos/pclinuxos/srpms/SRPMS.pclos/palemoon-27.0.3-1pclos2017.src.rpm

%description
Pale Moon offers you a browsing experience in a browser completely built
from its own, independently developed source that has been forked off from
Firefox/Mozilla code, with carefully selected features and optimizations to
improve the browser's speed*, resource use, stability and user experience,
while offering full customization and a growing collection of extensions
and themes to make the browser truly your own.

# %global debug_package %{nil}
%global __os_install_post %( echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g' )

%prep
#%setup -q -n Pale-Moon-%{version}_Release
%setup -q -b0
pushd .%{_datarootdir}/%{name}/source
td=Pale-Moon-%{version}_Release
%if !%{dummy_package}
tar -zxf "%{SOURCE1}" ; { mv "${td:-NOTHINGTOMOVE}"/{.*,*} . 2>&1 ||: ; } | grep -vE "cannot move.*\/\.' to '\.\/\." ; rmdir "${td}"
%endif
popd

# the one from build.opensuse.org has all sorts of interesting actions but I do not want to use them

%build
source /usr/bin/gcc49
pushd .%{_datarootdir}/%{name}/source
%if !%{dummy_package}
cp -p ${RPM_SOURCE_DIR}/%{name}-%{version}-%{release}%{_datarootdir}/%{name}/build/mozconfig ./.mozconfig
./mach build
%endif

popd

%install
source /usr/bin/gcc49
rm -rf %{buildroot}
rsync -a ./ %{buildroot}/ --exclude='**/.*.swp' --exclude='**/.git'
pushd .%{_datarootdir}/%{name}/source
%if !%{dummy_package}
make -f client.mk \
        DESTDIR=%{buildroot}%{_datadir}/%{name}/app \
        idldir=%{_datadir}/idl/%{name} \
        includedir=%{_includedir}/%{name} \
        installdir=%{_libdir}/%{name} \
        sdkdir=%{_libdir}/%{name}-devel \
        install
%endif

popd

rm -rf %{buildroot}%{_datadir}/%{name}/pmbuild \
       .%{_datadir}/%{name}/pmbuild
# this is basically like a make_clean I guess. If you want the source code provided in the package, comment this line.
find %{buildroot}%{_datadir}/%{name}/source -mindepth 1 ! -regex '.*.patch' -exec rm -rf {} \; 2>/dev/null || :
find %{buildroot} -maxdepth 1 -name 'README.md' -exec rm -f {} \; 2>/dev/null || :

%clean
rm -rf %{buildroot}
exit 0

%post
# rpm post 2018-01-30

# Deploy icons
which xdg-icon-resource 1>/dev/null 2>&1 && {

   # Deploy default application icons
   for theme in hicolor ;
   do

      # NONE for palemoon
      ## Deploy scalable application icons
      #cp -p %{_datarootdir}/%{name}/inc/icons/%{name}-${theme}-scalable.svg %{_datarootdir}/icons/${theme}/scalable/apps/palemoon.svg

      # Deploy size application icons
%if !%{dummy_package}
      /usr/share/palemoon/inc/icon_helper.sh install
%endif

   done

   # Deploy custom application icons
   # none

   # Update icon caches
   xdg-icon-resource forceupdate &
   for word in hicolor ;
   do
      touch --no-create %{_datarootdir}/icons/${word}
      gtk-update-icon-cache %{_datarootdir}/icons/${word} &
   done

} 1>/dev/null 2>&1

# Deploy desktop file
desktop-file-install --rebuild-mime-info-cache %{_datarootdir}/%{name}/%{name}.desktop 1>/dev/null 2>&1

# Add mimetype and set default application
for user in root ${SUDO_USER} bgstack15 ;
do
{
   while read line;
   do
      which xdg-mime && {
         su "${user}" -c "xdg-mime install %{_datarootdir}/%{name}/inc/palemoon-mimeinfo.xml &"
         su "${user}" -c "xdg-mime default %{name}.desktop ${line} &"
      }
      which gio && {
         su "${user}" -c "gio mime ${line} %{name}.desktop &"
      }
      which update-mime-database && {
         case "${user}" in
            root) update-mime-database %{_datarootdir}/mime & ;;
            *) su "${user}" -c "update-mime-database ~${user}/.local/share/mime &";;
         esac
      }
   done <<'EOW'
application/x-xpinstall
EOW
} 1>/dev/null 2>&1 &
done

exit 0

%preun
# rpm preun 2018-01-31
if test "$1" = "0";
then
{
   # total uninstall

   # Remove mimetype definitions
   for user in root ${SUDO_USER} bgstack15 ;
   do
      getent passwd "${user}" && which xdg-mime && {
         su "${user}" -c "xdg-mime uninstall %{_datarootdir}/%{name}/inc/palemoon-mimeinfo.xml &"
      }
      # gio uninstall is not implemented?
      which update-mime-database && {
         case "${user}" in
            root) update-mime-database %{_datarootdir}/mime & ;;
            *) su "${user}" -c "update-mime-database ~${user}/.local/share/mime &";;
        esac
      }
   done

   # Remove systemd files
   # NONE

   # Remove desktop file
   rm -f %{_datarootdir}/applications/%{name}.desktop
   which update-desktop-database && update-desktop-database -q %{_datarootdir}/applications &

   # Remove icons
   which xdg-icon-resource && {

      # Remove default application icons
      for theme in hicolor ;
      do

         ## Remove scalable application icons
         # NONE
         #rm -f %{_datarootdir}/icons/${theme}/scalable/apps/palemoon.svg

         # Remove size application icons
         /usr/share/palemoon/inc/icon_helper.sh remove

      done

      # Remove custom application icons
      # NONE

      # Remove default mimetype icons
      # NONE

      # Remove custom mimetype icons
      # NONE

      # Update icon caches
      xdg-icon-resource forceupdate &
      for word in hicolor ;
      do
         touch --no-create %{_datarootdir}/icons/${word}
         gtk-update-icon-cache %{_datarootdir}/icons/${word} &
      done
   }

} 1>/dev/null 2>&1
fi 
exit 0

%postun
# rpm postun 2018-01-31
exit 0

%files
%dir /usr/share/palemoon
%dir /usr/share/palemoon/build
%dir /usr/share/palemoon/inc
/usr/bin/palemoon
%attr(666, -, -) /usr/share/palemoon/palemoon.desktop
/usr/share/palemoon/source
/usr/share/palemoon/build/files-for-versioning.txt
/usr/share/palemoon/build/get-sources
/usr/share/palemoon/build/get-files
/usr/share/palemoon/build/palemoon.spec
/usr/share/palemoon/build/mozconfig
/usr/share/palemoon/build/pack
/usr/share/palemoon/doc
/usr/share/palemoon/inc/palemoon_ver.txt
/usr/share/palemoon/inc/icon_helper.sh
/usr/share/palemoon/inc/sha256sum.txt
%config %attr(666, -, -) /usr/share/palemoon/inc/palemoon-mimeinfo.xml
/usr/share/palemoon/app
%doc %attr(444, -, -) /usr/share/doc/palemoon/README.md

%changelog
* Tue Jan 30 2018 B Stack <bgstack15@gmail.com> 27.7.1-1
- Initial rpm built.
