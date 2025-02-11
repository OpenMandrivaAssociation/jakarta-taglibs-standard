%{?_javapackages_macros:%_javapackages_macros}
# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global base_name       standard
%global short_name      taglibs-%{base_name}

Name:           jakarta-taglibs-standard
Version:        1.1.2
Release:        11.0%{?dist}
Epoch:          0
Summary:        An open-source implementation of the JSP Standard Tag Library
License:        ASL 2.0
URL:            https://jakarta.apache.org/taglibs/
Source0:        http://archive.apache.org/dist/jakarta/taglibs/standard/source/jakarta-taglibs-standard-%{version}-src.tar.gz
Source1:        http://repo1.maven.org/maven2/jstl/jstl/%{version}/jstl-%{version}.pom
Source2:        http://repo1.maven.org/maven2/taglibs/standard/%{version}/standard-%{version}.pom

Patch0:         jakarta-taglibs-standard-1.1.1-build.patch
Patch1:         fix-1.6.0-build.patch
Patch2:         %{name}-jdbc-4.1.patch
# remove relocation use -a parameter with %%add_maven_depmap
# prevent maven/system overflow
Patch3:         jakarta-taglibs-standard-1.1.2-jstl-pom.patch
Patch4:         jakarta-taglibs-standard-1.1.2-standard-pom.patch

BuildArch:      noarch
BuildRequires:  jpackage-utils >= 0:1.5.30
BuildRequires:  ant
BuildRequires:  tomcat-servlet-3.0-api
BuildRequires:  tomcat-jsp-2.2-api
BuildRequires:  java-devel
BuildRequires:  java-javadoc
BuildRequires:  xalan-j2 >= 2.6.0
Requires:       tomcat-servlet-3.0-api
Requires:       tomcat-jsp-2.2-api
Requires:       xalan-j2 >= 2.6.0


Provides:       javax.servlet.jsp.jstl

%description
This package contains Jakarta Taglibs's open-source implementation of the
JSP Standard Tag Library (JSTL), version 1.1. JSTL is a standard under the
Java Community Process.

%package        javadoc
Summary:        Javadoc for %{name}

%description    javadoc
Javadoc for %{name}.


%prep
%setup -q -n %{name}-%{version}-src
%patch0
%patch1
%patch2
#
rm -fr standard/src/org/apache/taglibs/standard/lang/jstl/test/PageContextImpl.java
rm -fr standard/src/org/apache/taglibs/standard/lang/jstl/test/EvaluationTest.java
cat > build.properties <<EOBP
build.dir=build
dist.dir=dist
servlet24.jar=$(build-classpath tomcat-servlet-3.0-api)
jsp20.jar=$(build-classpath jsp)
jaxp-api.jar=$(build-classpath xalan-j2)
EOBP

cp -p %{SOURCE1} jstl-1.1.2.pom
%patch3 -p0
cp -p %{SOURCE2} standard-1.1.2.pom
%patch4 -p0


%build
ant \
  -Dfinal.name=%{short_name} \
  -Dj2se.javadoc=%{_javadocdir}/java \
  -f standard/build.xml \
  dist


%install
# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p standard/dist/standard/lib/jstl.jar $RPM_BUILD_ROOT%{_javadir}/jakarta-taglibs-core.jar
cp -p standard/dist/standard/lib/standard.jar $RPM_BUILD_ROOT%{_javadir}/jakarta-taglibs-standard.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in jakarta-*; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)

mkdir -p $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 jstl-1.1.2.pom $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-jakarta-taglibs-core.pom
%add_maven_depmap JPP-jakarta-taglibs-core.pom jakarta-taglibs-core.jar -a "javax.servlet:jstl,org.eclipse.jetty.orbit:javax.servlet.jsp.jstl"
install -pm 644 standard-1.1.2.pom $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar -a "org.eclipse.jetty.orbit:org.apache.taglibs.standard.glassfish"

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr standard/dist/standard/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# J2EE API dir
install -d -m 755 %{buildroot}%{_javadir}/javax.servlet.jsp.jstl/
ln -sf ../%{name}.jar %{buildroot}%{_javadir}/javax.servlet.jsp.jstl/
ln -sf ../jakarta-taglibs-core.jar %{buildroot}%{_javadir}/javax.servlet.jsp.jstl/

%files -f .mfiles
%doc LICENSE NOTICE
%doc standard/README_src.txt standard/README_bin.txt standard/dist/doc/doc/standard-doc/*.html
%{_javadir}/taglibs-core.jar
%{_javadir}/taglibs-standard.jar
%{_javadir}/javax.servlet.jsp.jstl/

%files javadoc
%doc LICENSE NOTICE
%doc %{_javadocdir}/%{name}


%changelog
* Mon Aug 12 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.1.2-11
- Add javax.servlet.jsp.jstl provides and directory

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.2-9
- Add depmaps for org.eclipse.jetty.orbit

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 20 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.2-7
- Install LICENSE and NOTICE files

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Hui Wang <huwang@redhat.com> 0:1.1.2-5
- Bug 829804

* Wed Feb 8 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.2-4
- Remove test classes that fail to build(non impl methods) with servlet 3/jsp 2.2.

* Tue Jan 24 2012 Deepak Bhole <dbhole@redhat.com> - 0:1.1.2-3
- Added patch to build with JDBC 4.1/Java 7

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.2-1
- Update to 1.1.2 upstream release - 7 years later!.

* Tue Jul 19 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.1-12.3
- Adapt to current guidelines.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.1-12.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.1-11.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.1-10.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.1.1-9.2
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.1.1-9jpp.1
- Autorebuild for GCC 4.3

* Wed Mar 21 2007 Matt Wringe <mwringe@redhat.com> 0:1.1.1-8jpp.1
- Merge with latest jpp version
- Fix various rpmlint warnings

* Wed Mar 21 2007 Matt Wringe <mwringe@redhat.com> 0:1.1.1-8jpp
- Fix empty javadoc post and postun rpmlint warnings
- Update copyright year

* Thu Aug 10 2006 Matt Wringe <mwringe at redhat.com> 0:1.1.1-7jpp.1
- Merge with upstream version
 - Add missing javadoc postun
 - Add missing javadoc requires

* Thu Aug 10 2006 Karsten Hopp <karsten@redhat.de> 1.1.1-6jpp_3fc
- Requires(post): coreutils

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.1.1-6jpp_2fc
- Rebuilt

* Thu Jul 20 2006 Matt Wringe <mwringe at redhat.com> 0:1.1.1-6jpp_1fc
- Merge with upstream version
- Natively compile package

* Thu Jul 20 2006 Matt Wringe <mwringe at redhat.com> 0:1.1.1-6jpp
- Add conditional native compilation
- Add missing BuildRequires and Requires for tomcat5-jsp-2.0-api and xalan-j2
  (from Deepak Bhole <dbhole at redhat.com>)

* Thu Apr 27 2006 Fernando Nasser <fnasser@redhat.com> 0:1.1.1-5jpp
- First JPP 1.7 build

* Fri Oct 22 2004 Fernando Nasser <fnasser@redhat.com> 0:1.1.1-4jpp
- Rebuild to replace incorrect patch file

* Fri Oct 22 2004 Fernando Nasser <fnasser@redhat.com> 0:1.1.1-3jpp
- Remove hack for 1.3 Java that would break building with an IBM SDK.

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:1.1.1-2jpp
- Rebuild with ant-1.6.2

* Tue Jul 27 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.1.1-1jpp
- 1.1.1

* Tue Feb 17 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.1.0-1jpp
- 1.1.0 final

* Wed Jan 22 2004 David Walluck <david@anti-microsoft.org> 0:1.1.0-0.B1.2jpp
- change URL
- fix description

* Fri Jan  9 2004 Kaj J. Niemi <kajtzu@fi.basen.net> - 0:1.1.0-0.B1.1jpp
- First build for JPackage

* Mon Dec 22 2003 Kaj J. Niemi <kajtzu@fi.basen.net> - 0:1.1.0-0.B1.1
- First build
- Skip examples for now
