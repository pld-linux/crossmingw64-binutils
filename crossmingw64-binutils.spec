Summary:	Cross Mingw64 GNU binary utility development utilities - binutils
Summary(es.UTF-8):	Utilitarios para desarrollo de binarios de la GNU - Mingw64 binutils
Summary(fr.UTF-8):	Utilitaires de développement binaire de GNU - Mingw64 binutils
Summary(pl.UTF-8):	Skrośne narzędzia programistyczne GNU dla Mingw64 - binutils
Summary(pt_BR.UTF-8):	Utilitários para desenvolvimento de binários da GNU - Mingw64 binutils
Summary(tr.UTF-8):	GNU geliştirme araçları - Mingw64 binutils
Name:		crossmingw64-binutils
Version:	2.23.51.0.1
Release:	1
License:	GPL v3+
Group:		Development/Tools
Source0:	http://www.kernel.org/pub/linux/devel/binutils/binutils-%{version}.tar.bz2
# Source0-md5:	a6328eafc6bfc59fe555a4e50b3c3055
URL:		http://sources.redhat.com/binutils/
BuildRequires:	automake
BuildRequires:	bash
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	zlib-devel
# not necessary unless we patch .texi docs; but they are not packaged here anyway
#BuildRequires:	texinfo >= 4.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		x86_64-w64-mingw32
%define		arch		%{_prefix}/%{target}

%description
crossmingw64 is a complete cross-compiling development system for
building stand-alone Microsoft Windows applications under Linux using
the Mingw64 build libraries. This includes a binutils, gcc with g++
and objc, and libstdc++, all cross targeted to x86_64-mingw32, along
with supporting Win64 libraries in 'coff' format from free sources.

This package contains cross targeted binutils.

%description -l pl.UTF-8
crossmingw64 jest kompletnym systemem do kroskompilacji, pozwalającym
budować aplikacje MS Windows pod Linuksem używając bibliotek mingw64.
System składa się z binutils, gcc z g++ i objc, libstdc++ - wszystkie
generujące kod dla platformy x86_64-mingw32, oraz z bibliotek w formacie
COFF.

Ten pakiet zawiera binutils generujące skrośnie binaria dla Win64.

%prep
%setup -q -n binutils-%{version}

%build
# ldscripts won't be generated properly if SHELL is not bash...
CFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags}" \
CONFIG_SHELL="/bin/bash" \
./configure \
	--disable-shared \
	--disable-nls \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--with-sysroot=%{arch} \
	--host=%{_target_platform} \
	--build=%{_target_platform} \
	--target=%{target}

%{__make} all

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# remove this man page unless we cross-build for netware platform.
# however, this should be done in Makefiles.
rm $RPM_BUILD_ROOT%{_mandir}/man1/*nlmconv.1

# libiberty.a is ELF not PE
rm $RPM_BUILD_ROOT%{_libdir}/libiberty.a

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
