#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	execnet
Summary:	Rapid multi-Python deployment
Name:		python-%{module}
Version:	1.3.0
Release:	2
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/e/execnet/%{module}-%{version}.tar.gz
# Source0-md5:	426c1a963cee5f671a3e8187b983c915
Patch0:		setup_deps.patch
URL:		http://codespeak.net/execnet
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
%if %{with python2}
BuildRequires:	python-setuptools >= 7.0
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools >= 7.0
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
execnet provides carefully tested means to ad-hoc interact with Python
interpreters across version, platform and network barriers. It
provides a minimal and fast API targetting the following uses:

- distribute tasks to local or remote processes
- write and deploy hybrid multi-process applications
- write scripts to administer multiple hosts

%package -n python3-%{module}
Summary:	Rapid multi-Python deployment
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
execnet provides carefully tested means to ad-hoc interact with Python
interpreters across version, platform and network barriers. It
provides a minimal and fast API targetting the following uses:

- distribute tasks to local or remote processes
- write and deploy hybrid multi-process applications
- write scripts to administer multiple hosts

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

sed -i -e's/get_version_from_scm=True/version="%{version}"/' setup.py

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

# no %%py_postclean !
# the source code might be run on a remote machine
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.txt ISSUES.txt CHANGELOG
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.txt ISSUES.txt CHANGELOG
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
