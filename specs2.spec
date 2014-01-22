%global specs2_version 1.12.3
%global scala_version 2.10

Name:           specs2
Version:        %{specs2_version}
Release:        1%{?dist}
Summary:        Library for writing executable software specifications

License:        MIT
URL:            https://github.com/etorrebore/specs2
Source0:        https://github.com/etorreborre/specs2/archive/v%{specs2_version}.tar.gz
Source1:	https://raw.github.com/willb/climbing-nemesis/master/climbing-nemesis.py

BuildArch:	noarch
BuildRequires:  sbt
BuildRequires:  scala
BuildRequires:	python
BuildRequires:	mvn(net.sourceforge.fmpp:fmpp)
BuildRequires:	mvn(org.beanshell:bsh)
BuildRequires:	mvn(xml-resolver:xml-resolver)
BuildRequires:	mvn(org.freemarker:freemarker)
BuildRequires:	maven-local
BuildRequires:	javapackages-tools
Requires:	javapackages-tools
Requires:       scala

%description

specs2 is a library for writing executable software specifications.

With specs2 you can write software specifications for one class (unit
specifications) or a full system (acceptance specifications).

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q

sed -i -e 's/2[.]10[.]2/2.10.3/g' project/

sed -i -e 's/0[.]13[.]0/0.13.1/g' project/build.properties || echo sbt.version=0.13.1 > project/build.properties

cp -r /usr/share/java/sbt/ivy-local .
mkdir boot

cp %{SOURCE1} .

chmod 755 climbing-nemesis.py

./climbing-nemesis.py --jarfile /usr/share/java/scalacheck.jar org.scalacheck scalacheck ivy-local --version 1.11.0 --scala %{scala_version}


%build

export SBT_BOOT_DIR=boot
export SBT_IVY_DIR=ivy-local
sbt package deliverLocal publishM2Configuration

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_javadir}
mkdir -p %{buildroot}/%{_mavenpomdir}

mkdir -p %{buildroot}/%{_javadocdir}/%{name}

cp core/target/scala-%{scala_version}/%{name}_%{scala_version}-%{version}.jar %{buildroot}/%{_javadir}/%{name}.jar
cp core/target/scala-%{scala_version}/%{name}_%{scala_version}-%{version}.pom %{buildroot}/%{_mavenpomdir}/JPP-%{name}.pom

cp -rp core/target/scala-%{scala_version}/api/* %{buildroot}/%{_javadocdir}/%{name}

%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%doc LICENSE README

%files javadoc
%{_javadocdir}/%{name}


%changelog

* Tue Jan 7 2014 William Benton <willb@redhat.com> - 0.4.2-1
- initial package
