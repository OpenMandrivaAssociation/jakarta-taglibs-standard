%define gcj_support	1
%define base_name       standard
%define short_name      taglibs-%{base_name}
%define section         free
%define jversion	1.1.2

Name:           jakarta-%{short_name}
Version:        1.1.2
Release:        %mkrel 6
Epoch:          0
Summary:        An open-source implementation of the JSP Standard Tag Library
License:        Apache License
Group:          Development/Java
#Vendor:         JPackage Project
#Distribution:   JPackage
URL:            http://jakarta.apache.org/taglibs/
Source:         http://www.apache.org/dist/jakarta/taglibs/standard/source/jakarta-taglibs-standard-%{jversion}-src.tar.bz2
Patch0:		jakarta-taglibs-standard-%{version}-build.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%if %{gcj_support}
BuildRequires:	java-gcj-compat
%else
BuildArch:      noarch
%endif
BuildRequires:  ant
BuildRequires:  jpackage-utils >= 0:1.5.30
BuildRequires:  jsp
BuildRequires:  servletapi5 >= 0:5.0.16
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
Requires:       servletapi5 >= 0:5.0.16
Requires:       xalan-j2
Requires:       xerces-j2

%description
This directory contains releases for the 1.1.x versions of the Standard
Tag Library, Jakarta Taglibs's open-source implementation of the JSP
Standard Tag Library (JSTL), version 1.1. JSTL is a standard under the
Java Community Process.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
BuildRequires:  java-javadoc

%description    javadoc
Javadoc for %{name}.


%prep
%setup -q -n %{name}-%{jversion}-src
%patch0
cat > build.properties <<EOBP
build.dir=build
dist.dir=dist
servlet24.jar=$(build-classpath servletapi5)
jsp20.jar=$(build-classpath jspapi)
xalan.jar=$(build-classpath xalan-j2)
xercesImpl.jar=$(build-classpath xerces-j2)
EOBP

%build

%ant \
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
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}


%files
%defattr(0644,root,root,0755)
%doc standard/README_src.txt standard/README_bin.txt standard/dist/doc/doc/standard-doc/*.html
%{_javadir}/*
%if %{gcj_support}
%{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}


