%define gcj_support	0
%define base_name	standard
%define short_name	taglibs-%{base_name}

Summary:	An open-source implementation of the JSP Standard Tag Library
Name:		jakarta-taglibs-standard
Version:	1.1.2
Release:	12
License:	ASL 2.0
Group:		Development/Java
Url:		http://jakarta.apache.org/taglibs/
Source0:	http://archive.apache.org/dist/jakarta/taglibs/standard/source/jakarta-taglibs-standard-%{version}-src.tar.gz
Patch0:		jakarta-taglibs-standard-%{version}-build.patch
Patch1:		fix-1.6.0-build.patch
Patch2:		jakarta-taglibs-standard-jdbc-4.1.patch
%if !%{gcj_support}
BuildArch:	noarch
%else
BuildRequires:	java-gcj-compat-devel
Requires(post,postun):	java-gcj-compat
%endif
BuildRequires:	ant
BuildRequires:	java-1.6.0-openjdk-devel
BuildRequires:	jpackage-utils >= 0:1.5.30
BuildRequires:	tomcat-servlet-3.0-api
BuildRequires:	tomcat-jsp-2.2-api
BuildRequires:	xalan-j2 >= 2.6.0
Requires:	tomcat-servlet-3.0-api
Requires:	tomcat-jsp-2.2-api
Requires:	xalan-j2 >= 2.6.0

%description
This package contains Jakarta Taglibs's open-source implementation of the 
JSP Standard Tag Library (JSTL), version 1.1. JSTL is a standard under the
Java Community Process.

%package        javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java
BuildRequires:	java-javadoc

%description    javadoc
Javadoc for %{name}.

%prep
%setup  -qn %{name}-1.1.2-src
%patch0 -p0 -b .origA
%patch1 -p0
%patch2 -p1
#
rm -fr standard/src/org/apache/taglibs/standard/lang/jstl/test/PageContextImpl.java
rm -fr standard/src/org/apache/taglibs/standard/lang/jstl/test/EvaluationTest.java
cat > build.properties <<EOBP
build.dir=build
dist.dir=dist
servlet24.jar=$(build-classpath tomcat-servlet-3.0-api)
jsp20.jar=$(build-classpath tomcat-jsp-2.2-api)
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
mkdir -p %{buildroot}%{_javadir}
cp -p standard/dist/standard/lib/jstl.jar %{buildroot}%{_javadir}/jakarta-taglibs-core-%{version}.jar
cp -p standard/dist/standard/lib/standard.jar %{buildroot}%{_javadir}/jakarta-taglibs-standard-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr standard/dist/standard/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

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
%doc standard/README_src.txt standard/README_bin.txt standard/dist/doc/doc/standard-doc/*.html
%{_javadir}/*

%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/jakarta-taglibs-core-1.1.1.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/jakarta-taglibs-standard-1.1.1.jar.*
%endif

%files javadoc
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

