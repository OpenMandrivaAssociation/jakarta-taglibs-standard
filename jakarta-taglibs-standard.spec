%define gcj_support 0
 

%define base_name       standard
%define short_name      taglibs-%{base_name}

Name:           jakarta-taglibs-standard
Version:        1.1.2
Release:        9
Summary:        An open-source implementation of the JSP Standard Tag Library
License:        ASL 2.0
Group:          Development/Java
URL:            http://jakarta.apache.org/taglibs/
Source:         http://archive.apache.org/dist/jakarta/taglibs/standard/source/jakarta-taglibs-standard-1.1.1-src.tar.gz
Patch0:         jakarta-taglibs-standard-%{version}-build.patch
Patch1:         jakarta-taglibs-standard-1.1.1-remove-enums.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%if ! %{gcj_support}
BuildArch:      noarch
%endif
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
rm -rf $RPM_BUILD_ROOT

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

%clean
rm -rf $RPM_BUILD_ROOT

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

