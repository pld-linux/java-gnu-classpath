#
# TODO:
#		- classpathx (spec or source1+subpkg?)
#
Summary:	GNU Classpath (Essential Libraries for Java)
Summary(pl):	GNU Classpath (Najważniejsze biblioteki dla Javy)
Name:		classpath
Version:	0.10
Release:	0.2
License:	GPL v2
Group:		Libraries
Source0:	ftp://ftp.gnu.org/gnu/classpath/%{name}-%{version}.tar.gz
# Source0-md5:	a59a5040f9c1237dbf27bfc668919943
URL:		http://www.gnu.org/software/classpath/classpath.html
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1.7
BuildRequires:	jikes >= 1.18
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	gtk+2-devel >= 2.2
BuildRequires:	libart_lgpl-devel >= 2.1.0
BuildRequires:	libtool >= 1.4.2
BuildRequires:	texinfo >= 4.2
BuildRequires:	unzip
BuildRequires:	zip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU Classpath (Essential Libraries for Java) is a project to create
free core class libraries for use with virtual machines and compilers
for the Java language. It includes all native methods and core classes
necessary for a completely functional Java runtime.

%description -l pl
GNU Classpath (Najważniejsze biblioteki javy) to projekt stworzenia
wolnego jądra klas bibliotek do wykorzystania z wirtualnymi maszynami
i kompilatorami dla języka Java. Zawiera wszystkie natywne metody i
główne klasy niezbędne dla kompletnej funkcjonalności środowiska Javy.

%prep
%setup -q

%build
%configure \
	--with-jikes \
	--enable-java \
	--enable-jni \
	--disable-cni \
	--enable-gtk-peer \
	--enable-load-library \
	--disable-debug

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

unzip	$RPM_BUILD_ROOT%{_datadir}/classpath/glibj.zip -d $RPM_BUILD_ROOT%{_datadir}/classpath
rm -rf	$RPM_BUILD_ROOT%{_datadir}/classpath/{api,glibj.zip}
mv -f	$RPM_BUILD_ROOT%{_libdir}{/classpath/*,}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKYOU TODO
%{_libdir}/libgtkpeer.la
%attr(755,root,root) %{_libdir}/libgtkpeer.so.*.*.*
%{_libdir}/libjavaawt.la
%attr(755,root,root) %{_libdir}/libjavaawt.so.*.*.*
%{_libdir}/libjavaio.la
%attr(755,root,root) %{_libdir}/libjavaio.so.*.*.*
%{_libdir}/libjavalang.la
%attr(755,root,root) %{_libdir}/libjavalang.so.*.*.*
%{_libdir}/libjavalangreflect.la
%attr(755,root,root) %{_libdir}/libjavalangreflect.so.*.*.*
%{_libdir}/libjavanet.la
%attr(755,root,root) %{_libdir}/libjavanet.so.*.*.*
%{_libdir}/libjavanio.la
%attr(755,root,root) %{_libdir}/libjavanio.so.*.*.*
%{_libdir}/libjavautil.la
%attr(755,root,root) %{_libdir}/libjavautil.so.*.*.*
%{_datadir}/classpath
%{_infodir}/*
