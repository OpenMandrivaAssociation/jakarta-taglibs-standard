%define gcj_support 0
 

%define base_name       standard
%define short_name      taglibs-%{base_name}

Name:           jakarta-taglibs-standard
Version:        1.1.2
Release:        10
Summary:        An open-source implementation of the JSP Standard Tag Library
License:        ASL 2.0
Group:          Development/Java
URL:            http://jakarta.apache.org/taglibs/
Source:         http://archive.apache.org/dist/jakarta/taglibs/standard/source/jakarta-taglibs-standard-1.1.1-src.tar.gz
Patch0:         jakarta-taglibs-standard-%{version}-build.patch
Patch1:         jakarta-taglibs-standard-1.1.1-remove-enums.patch

%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRequires:	java-1.6.0-openjdk-devel
BuildRequires:  jpackage-utils >= 0:1.5.30
BuildRequires:  ant
BuildRequires:  servletapi5 >= 0:5.0.16
BuildRequires:  tomcat5-jsp-2.0-api >= 0:5.0.16
BuildRequires:  xalan-j2 >= 2.6.0
Requires:       servletapi5 >= 0:5.0.16
Requires:       tomcat5-jsp-2.0-api >= 0:5.0.16
Requires:       xalan-j2 >= 2.6.0

%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
Requires(post):         java-gcj-compat
Requires(postun):       java-gcj-compat
%endif

%description
This package contains Jakarta Taglibs's open-source implementation of the 
JSP Standard Tag Library (JSTL), version 1.1. JSTL is a standard under the
Java Community Process.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
BuildRequires:  java-javadoc

%description    javadoc
Javadoc for %{name}.


%prep
%setup  -q -n %{name}-1.1.1-src
%patch0 -p0 -b .orig
%patch1 -p0
cat > build.properties <<EOBP
build.dir=build
dist.dir=dist
servlet24.jar=$(build-classpath servletapi5)
jsp20.jar=$(build-classpath jspapi)
jaxp-api.jar=$(build-classpath xalan-j2)
EOBP

%build

ant \
  -Dfinal.name=%{short_name} \
  -Dj2se.javadoc=%{_javadocdir}/java \
  -f standard/build.xml \
  dist


%install
# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p standard/dist/standard/lib/jstl.jar $RPM_BUILD_ROOT%{_javadir}/jakarta-taglibs-core-%{version}.jar
cp -p standard/dist/standard/lib/standard.jar $RPM_BUILD_ROOT%{_javadir}/jakarta-taglibs-standard-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr standard/dist/standard/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}


%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%doc standard/README_src.txt standard/README_bin.txt standard/dist/doc/doc/standard-doc/*.html
%{_javadir}/*

%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/jakarta-taglibs-core-1.1.1.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/jakarta-taglibs-standard-1.1.1.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}



%changelog
* Sun Nov 27 2011 Guilherme Moro <guilherme@mandriva.com> 1.1.2-9
+ Revision: 733987
- rebuild
- imported package jakarta-taglibs-standard

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - fix no-buildroot-tag
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sun Sep 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.1.2-6mdv2008.0
+ Revision: 87985
- use macros for rebuild-gcj-db

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.1.2-5mdv2008.0
+ Revision: 87421
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sun Sep 09 2007 Pascal Terjan <pterjan@mandriva.org> 0:1.1.2-4mdv2008.0
+ Revision: 82792
- update to new version


* Thu Mar 15 2007 Christiaan Welvaart <spturtle@mandriva.org> 1.1.2-3mdv2007.1
+ Revision: 144224
- rebuild for 2007.1

  + Per Øyvind Karlsen <pkarlsen@mandriva.com>
    - Import jakarta-taglibs-standard

* Thu Aug 24 2006 David Walluck <walluck@mandriva.org> 0:1.1.2-2mdv2007.0
- BuildRequires: jsp

* Fri Nov 11 2005 David Walluck <walluck@mandriva.org> 0:1.1.1-4.2mdk
- aot compile

* Sun May 22 2005 David Walluck <walluck@mandriva.org> 0:1.1.1-4.1mdk
- release

* Sat Oct 23 2004 Fernando Nasser <fnasser@redhat.com> 0:1.1.1-4jpp
- Rebuild to replace incorrect patch file

* Sat Oct 23 2004 Fernando Nasser <fnasser@redhat.com> 0:1.1.1-3jpp
- Remove hack for 1.3 Java that would break building with an IBM SDK.

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 0:1.1.1-2jpp
- Rebuild with ant-1.6.2

* Wed Jul 28 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.1.1-1jpp
- 1.1.1

