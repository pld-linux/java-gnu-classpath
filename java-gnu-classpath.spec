#
# TODO:
#		- classpathx (spec or source1+subpkg?)
#
Summary:	GNU Classpath (Essential Libraries for Java)
Summary(pl):	GNU Classpath (Najwa¿niejsze biblioteki dla Javy)
Name:		classpath
Version:	0.10
Release:	0.1
License:	GPL v2
Group:		Libraries
Source0:	ftp://ftp.gnu.org/gnu/classpath/%{name}-%{version}.tar.gz
# Source0-md5:	a59a5040f9c1237dbf27bfc668919943
URL:		http://www.gnu.org/software/classpath/classpath.html
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1.7
BuildRequires:	jikes
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	gtk+2-devel >= 2.2
BuildRequires:	libart_lgpl-devel >= 2.1.0
BuildRequires:	libtool >= 1.4.2
BuildRequires:	texinfo >= 4.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU Classpath (Essential Libraries for Java) is a project to create
free core class libraries for use with virtual machines and compilers
for the Java language. It includes all native methods and core classes
necessary for a completely functional Java runtime.

%description -l pl
GNU Classpath (Najwa¿niejsze biblioteki javy) to projekt stworzenia
wolnego j±dra klas bibliotek do wykorzystania z wirtualnymi maszynami
i kompilatorami dla jêzyka Java. Zawiera wszystkie natywne metody i
g³ówne klasy niezbêdne dla kompletnej funkcjonalno¶ci ¶rodowiska Javy.

%prep
%setup -q

%build
#%%{__gettextize}
#%%{__aclocal}
#%%{__autoconf}
#%%{__autoheader}
#%%{__automake}
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so.*.*.*
%{_libdir}/%{name}/*.la
%{_libdir}/awt/
%{_datadir}/%{name}
# what about?
# /usr/lib/security/classpath.security ? it conflicts with gcc-java-tools
