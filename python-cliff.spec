#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	Command Line Interface Formulation Framework
Summary(pl.UTF-8):	Command Line Interface Formulation Framework - szkielet formułowania linii poleceń
Name:		python-cliff
# keep 2.x here for python2 support
Version:	2.18.0
Release:	5
License:	Apache
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/c/cliff/cliff-%{version}.tar.gz
# Source0-md5:	66490f2c437f543f32afe9e518e3c080
Patch0:		%{name}-prettytable.patch
Patch1:		%{name}-mock.patch
Patch2:		%{name}-py310.patch
Patch3:		%{name}-py2-test.patch
URL:		https://pypi.org/project/cliff/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-pbr >= 2.0.0
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-PyYAML >= 3.12
BuildRequires:	python-cmd2 >= 0.8.0
BuildRequires:	python-coverage >= 4.0
BuildRequires:	python-mock >= 2.0
BuildRequires:	python-openstackdocstheme >= 1.11.0
BuildRequires:	python-prettytable >= 0.7.2
BuildRequires:	python-pyparsing >= 2.1.0
BuildRequires:	python-six >= 1.10.0
BuildRequires:	python-stevedore >= 1.20.0
BuildRequires:	python-subunit >= 1.0.0
BuildRequires:	python-testrepository >= 0.0.18
BuildRequires:	python-testscenarios >= 0.4
BuildRequires:	python-testtools >= 2.2.0
BuildRequires:	python-unicodecsv >= 0.8.0
BuildRequires:	sphinx-pdg-2 >= 1.7.0
%endif
BuildRequires:	sed >= 4.0
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cliff is a framework for building command line programs. It uses
setuptools entry points to provide subcommands, output formatters, and
other extensions.

%description -l pl.UTF-8
cliff to szkielet do budowania programów działających z linii poleceń.
Wykorzystuje punkty wejściowe setuptools do zapewnienia podpoleceń,
funkcje formatujące wyjścia i inne rozszerzenia.

%prep
%setup -q -n cliff-%{version}
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1

%build
export PYTHON="%{__python}"
%py_build %{?with_tests:test}

%if %{with tests}
%{__rm} -r .testrepository
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%py_postclean

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/cliff/tests

install -d $RPM_BUILD_ROOT%{_examplesdir}/python-cliff-%{version}
cp -a demoapp/* $RPM_BUILD_ROOT%{_examplesdir}/python-cliff-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python-cliff-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python}|'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%{py_sitescriptdir}/cliff
%{py_sitescriptdir}/cliff-%{version}-py*.egg-info
%{_examplesdir}/python-cliff-%{version}
