Summary:	Cross Mingw64 GNU binary utility development utilities - binutils
Summary(es):	Utilitarios para desarrollo de binarios de la GNU - Mingw64 binutils
Summary(fr):	Utilitaires de d�veloppement binaire de GNU - Mingw64 binutils
Summary(pl):	Skro�ne narz�dzia programistyczne GNU dla Mingw64 - binutils
Summary(pt_BR):	Utilit�rios para desenvolvimento de bin�rios da GNU - Mingw64 binutils
Summary(tr):	GNU geli�tirme ara�lar� - Mingw64 binutils
Name:		crossmingw64-binutils
Version:	2.17.50.0.4
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	ftp://ftp.kernel.org/pub/linux/devel/binutils/binutils-%{version}.tar.bz2
# Source0-md5:	a05a19fb80254ed66c87e7fd69c680bb
Patch0:		%{name}-configure.patch
URL:		http://sources.redhat.com/binutils/
BuildRequires:	automake
BuildRequires:	bash
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel
# not necessary unless we patch .texi docs; but they are not packaged here anyway
#BuildRequires:	texinfo >= 4.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		x86_64-mingw64
%define		arch		%{_prefix}/%{target}

%description
crossmingw64 is a complete cross-compiling development system for
building stand-alone Microsoft Windows applications under Linux using
the Mingw64 build libraries. This includes a binutils, gcc with g++
and objc, and libstdc++, all cross targeted to x86_64-mingw64, along
with supporting Win32 libraries in 'coff' format from free sources.

This package contains cross targeted binutils.

%description -l pl
crossmingw64 jest kompletnym systemem do kroskompilacji, pozwalaj�cym
budowa� aplikacje MS Windows pod Linuksem u�ywaj�c bibliotek mingw64.
System sk�ada si� z binutils, gcc z g++ i objc, libstdc++ - wszystkie
generuj�ce kod dla platformyx86_64-mingw64, oraz z bibliotek w formacie
COFF.

Ten pakiet zawiera binutils generuj�ce skro�nie binaria dla Win32.

%prep
%setup -q -n binutils-%{version}
%patch0 -p1

%build
# Because of a bug in binutils-2.9.1, a cross libbfd.so* is not named
# lib<target>bfd.so*. To prevent confusion with native binutils, we
# forget about shared libraries right now, and do not install libbfd.a
# [the same applies to binutils 2.10.1.0.4]

# ldscripts won't be generated properly if SHELL is not bash...
CFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags}" \
CONFIG_SHELL="/bin/bash" \
./configure \
	--disable-shared \
	--disable-nls \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--host=%{_target_platform} \
	--build=%{_target_platform} \
	--target=%{target}

%{__make} all \
	tooldir=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL='$$s/install-sh -c' \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

# remove this man page unless we cross-build for netware platform.
# however, this should be done in Makefiles.
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/*nlmconv.1

# libiberty.a is ELF not PE
rm -f $RPM_BUILD_ROOT%{arch}/lib/libiberty.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%dir %{arch}
%dir %{arch}/lib
%dir %{arch}/bin
%attr(755,root,root) %{arch}/bin/*
%{arch}/lib/ldscripts
%attr(755,root,root) %{_bindir}/%{target}-*
%{_mandir}/man1/%{target}-*