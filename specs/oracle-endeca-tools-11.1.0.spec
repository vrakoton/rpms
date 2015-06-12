#-----------------------------------------------------------------------------
# author: Vina RAKOTONDRAINIBE (RE ENTER SAS)
# 
# Description:
# 
# Spec file to build an Endeca Tools and Framework RPM for Oracle guided search 11.1.0
#
#-----------------------------------------------------------------------------

%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%global product    oracle-endeca-tools
%global productdir %{productprefix}/endeca

%global uid 240
%global gid 240


#-----------------------------------------------------------------------------
# Main package
#-----------------------------------------------------------------------------
Name:           %{product}
Version:        11.1.0
Release:        0
Summary:        Oracle Guided Search MDEX 11.1.0 

Group:          System Environment/Daemons
License:        Proprietary
URL:            http://www.oracle.com
Source0:        endeca-tools-%{version}-%{release}.zip
Source1:        tools_response_11.1.0.txt
Source2:        oraInventory.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

AutoReqProv:    no

%description
Oracle Guided Search Tools and Framework 11.1.0


#-----------------------------------------------------------------------------
%prep


#-----------------------------------------------------------------------------
%build


#-----------------------------------------------------------------------------
%install
export DONT_STRIP=1
rm -rf %{buildroot}

mkdir -p %{buildroot}%{productprefix}

pushd %{buildroot}%{productprefix}
  unzip %{SOURCE0} > /dev/null 2>&1
  cd cd/Disk1/install \
  && ./silent_install.sh %{SOURCE1} ToolsAndFrameworks_1 %{buildroot}%{productprefix}/endeca/ToolsAndFrameworks_1 admin

  find $RPM_BUILD_ROOT -type f -exec sed -i "s|${RPM_BUILD_ROOT}||g" {} \;
popd

pushd %{buildroot}%{productprefix}
  rm -rf cd
popd


#-----------------------------------------------------------------------------
%clean
rm -rf %{buildroot}


#-------------------------------------------------------------------------------
%pre
getent group oracle > /dev/null || \
  /usr/sbin/groupadd -r -g %{gid} oracle 2> /dev/null || :
getent passwd endeca > /dev/null || \
  /usr/sbin/useradd -c "Endeca" -s /bin/bash -r -m -u %{uid} -g oracle \
    -d /opt/endeca endeca 2> /dev/null || :


%files
%defattr(-, root, root, -)
%{productdir}


#-----------------------------------------------------------------------------
%changelog
* Fri Jun 12 2015 Vina Rakotondrainibe <vrakoton@re-enter.fr> - 11.1.0
- Initial package creation
