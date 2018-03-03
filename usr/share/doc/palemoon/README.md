# Readme for Palemoon rpm
Package source is the official Pale Moon source.
See its changelog.txt for updates to the actual software.
Package maintainer: bgstack15@gmail.com

# Unique things about this package
My packages tend to wrap the whole application inside the /usr/share/%{name}/app directory. I like to keep it all self-contained on my filesystem.

# How to build this package
A build dependency is my [bgscripts](https://github.com/bgstack15/bgscripts) package.

Download this wrapper package source and run the pack utility.

    package=palemoon
    thisver=27.8.0-1
    mkdir -p ~/rpmbuild/{SOURCES,RPMS,BUILD,BUILDROOT,SPECS}
    cd ~/rpmbuild/SOURCES
    git clone https://github.com/bgstack15/palemoon-rpm "${package}-${thisver}"
    cd "${package}-${thisver}"
    usr/share/${package}/build/pack

The build script will fetch the official source from its [github location](https://github.com/MoonchildProductions/Pale-Moon/) and check its sha256sum against [usr/share/palemoon/inc/sha256sum.txt](usr/share/palemoon/inc/sha256sum.txt).

# How to maintain this package
For a new release from upstream, you have to derive the sha256sum and add it to the sha256sum.txt file.

When updating the version number, you can quickly pull up the list of files to edit:

    cd ~/rpmbuild/SOURCES/palemoon-27.7.1-1/usr/share/palemoon
    vi $( cat build/files-for-versioning.txt )

# References
1. PCLinuxOS package [http://ftp.nluug.nl/pub/os/Linux/distr/pclinuxos/pclinuxos/srpms/SRPMS.pclos/palemoon-27.0.3-1pclos2017.src.rpm](http://ftp.nluug.nl/pub/os/Linux/distr/pclinuxos/pclinuxos/srpms/SRPMS.pclos/palemoon-27.0.3-1pclos2017.src.rpm) which was linked from [https://pclinuxos.pkgs.org/rolling/pclinuxos-x86_64/palemoon-27.0.3-1pclos2017.x86_64.rpm.html](https://pclinuxos.pkgs.org/rolling/pclinuxos-x86_64/palemoon-27.0.3-1pclos2017.x86_64.rpm.html)
2. OpenSUSE package [https://build.opensuse.org/package/show/network/palemoon](https://build.opensuse.org/package/show/network/palemoon)
3. Fedora 27 Firefox package
4. Official developer info for GNU/Linux [https://developer.palemoon.org/Developer_Guide:Build_Instructions/Pale_Moon/Linux](https://developer.palemoon.org/Developer_Guide:Build_Instructions/Pale_Moon/Linux)
5. Countless searches for rpm spec advice and gcc.
6. Fedora 27 gcc 4.9 package by Davidva [https://copr.fedorainfracloud.org/coprs/davidva/gcc49/](https://copr.fedorainfracloud.org/coprs/davidva/gcc49/)
7. [https://bgstack15.wordpress.com/2018/02/01/gcc-4-9-for-fedora-27/](https://bgstack15.wordpress.com/2018/02/01/gcc-4-9-for-fedora-27/)

# Changelog
2018-01-31 palemoon 27.7.1-1
Initial rpm built.

* Mar  2 2018 B Stack <bgstack15@gmail.com> 27.8.0-1
- Rebase to upstream
