#-----------------------------------------------------------------------------
# author: Vina RAKOTONDRAINIBE (RE ENTER SAS)
# 
# Description:
# 
# Spec file to build an Endeca Platform Services RPM for Oracle guided search 11.1.0
#
#-----------------------------------------------------------------------------

%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%global product    oracle-endeca-platformservices
%global productdir %{mbsprefix}/endeca

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
Source0:        endeca-platformservices-%{version}-%{release}.zip
Source1:        platform_silent_11.1.0.txt
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

AutoReqProv:    no

%description
Oracle Guided Search Platform Services 11.1.0


#-----------------------------------------------------------------------------
%prep


#-----------------------------------------------------------------------------
%build


#-----------------------------------------------------------------------------
%install
export DONT_STRIP=1
rm -rf %{buildroot}

mkdir -p %{buildroot}%{mbsprefix}

pushd %{buildroot}%{mbsprefix}
  unzip %{SOURCE0}
  chmod +x OCplatformservices11.1.0-Linux64.bin \
    && ./OCplatformservices11.1.0-Linux64.bin --silent --target %{buildroot}%{mbsprefix} < %{SOURCE1}\
    && rm OCplatformservices11.1.0-Linux64.bin
  find $RPM_BUILD_ROOT -type f -exec sed -i "s|${RPM_BUILD_ROOT}||g" {} \;
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
