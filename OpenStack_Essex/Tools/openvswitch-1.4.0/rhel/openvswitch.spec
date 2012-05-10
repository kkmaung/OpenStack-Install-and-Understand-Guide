# Generated automatically -- do not modify!    -*- buffer-read-only: t -*-
# Spec file for Open vSwitch on Red Hat Enterprise Linux.

# Copyright (C) 2009, 2010, 2011 Nicira Networks, Inc.
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without warranty of any kind.

Name: openvswitch
Summary: Open vSwitch daemon/database/utilities
Group: System Environment/Daemons
URL: http://www.openvswitch.org/
Vendor: Nicira Networks, Inc.
Version: 1.4.0

License: ASL 2.0
Release: 1
Source: openvswitch-%{version}.tar.gz
Buildroot: /tmp/openvswitch-rpm
Requires: openvswitch-kmod, logrotate, python

%description
Open vSwitch provides standard network bridging functions and
support for the OpenFlow protocol for remote per-flow control of
traffic.

%prep
%setup -q

%build
./configure --prefix=/usr --sysconfdir=/etc --localstatedir=%{_localstatedir} --enable-ssl %{?build_number}
make %{_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rhel_cp() {
 base=$1
 mode=$2
 dst=$RPM_BUILD_ROOT/$(echo $base | sed 's,_,/,g')
 install -D -m $mode rhel/$base $dst
}
rhel_cp etc_init.d_openvswitch 0755
rhel_cp etc_logrotate.d_openvswitch 0644
rhel_cp etc_sysconfig_network-scripts_ifup-ovs 0755
rhel_cp etc_sysconfig_network-scripts_ifdown-ovs 0755
rhel_cp usr_share_openvswitch_scripts_sysconfig.template 0644

docdir=$RPM_BUILD_ROOT/usr/share/doc/openvswitch-%{version}
install -d -m755 "$docdir"
install -m 0644 rhel/README.RHEL "$docdir"
install python/compat/uuid.py $RPM_BUILD_ROOT/usr/share/openvswitch/python
install python/compat/argparse.py $RPM_BUILD_ROOT/usr/share/openvswitch/python

# Get rid of stuff we don't want to make RPM happy.
rm \
    $RPM_BUILD_ROOT/usr/bin/ovs-controller \
    $RPM_BUILD_ROOT/usr/share/man/man8/ovs-controller.8 \
    $RPM_BUILD_ROOT/usr/bin/ovs-test \
    $RPM_BUILD_ROOT/usr/share/man/man8/ovs-test.8 \
    $RPM_BUILD_ROOT/usr/sbin/ovs-vlan-bug-workaround \
    $RPM_BUILD_ROOT/usr/share/man/man8/ovs-vlan-bug-workaround.8

install -d -m 755 $RPM_BUILD_ROOT/var/lib/openvswitch

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Create default or update existing /etc/sysconfig/openvswitch.
SYSCONFIG=/etc/sysconfig/openvswitch
TEMPLATE=/usr/share/openvswitch/scripts/sysconfig.template
if [ ! -e $SYSCONFIG ]; then
    cp $TEMPLATE $SYSCONFIG
else
    for var in $(awk -F'[ :]' '/^# [_A-Z0-9]+:/{print $2}' $TEMPLATE)
    do
        if ! grep $var $SYSCONFIG >/dev/null 2>&1; then
            echo >> $SYSCONFIG
            sed -n "/$var:/,/$var=/p" $TEMPLATE >> $SYSCONFIG
        fi
    done
fi

# Ensure all required services are set to run
/sbin/chkconfig --add openvswitch
/sbin/chkconfig openvswitch on

%preun
if [ "$1" = "0" ]; then     # $1 = 0 for uninstall
    /sbin/service openvswitch stop
    /sbin/chkconfig --del openvswitch
fi

%postun
if [ "$1" = "0" ]; then     # $1 = 0 for uninstall
    rm -f /etc/openvswitch/conf.db
    rm -f /etc/sysconfig/openvswitch
    rm -f /etc/openvswitch/vswitchd.cacert
fi

exit 0

%files
%defattr(-,root,root)
/etc/init.d/openvswitch
%config(noreplace) /etc/logrotate.d/openvswitch
/etc/sysconfig/network-scripts/ifup-ovs
/etc/sysconfig/network-scripts/ifdown-ovs
/usr/bin/ovs-appctl
/usr/bin/ovs-benchmark
/usr/bin/ovs-dpctl
/usr/bin/ovs-ofctl
/usr/bin/ovs-parse-leaks
/usr/bin/ovs-pcap
/usr/bin/ovs-pki
/usr/bin/ovs-tcpundump
/usr/bin/ovs-vlan-test
/usr/bin/ovs-vsctl
/usr/bin/ovsdb-client
/usr/bin/ovsdb-tool
/usr/sbin/ovs-brcompatd
/usr/sbin/ovs-bugtool
/usr/sbin/ovs-vswitchd
/usr/sbin/ovsdb-server
/usr/share/man/man1/ovs-benchmark.1.gz
/usr/share/man/man1/ovs-pcap.1.gz
/usr/share/man/man1/ovs-tcpundump.1.gz
/usr/share/man/man1/ovsdb-client.1.gz
/usr/share/man/man1/ovsdb-server.1.gz
/usr/share/man/man1/ovsdb-tool.1.gz
/usr/share/man/man5/ovs-vswitchd.conf.db.5.gz
/usr/share/man/man8/ovs-appctl.8.gz
/usr/share/man/man8/ovs-brcompatd.8.gz
/usr/share/man/man8/ovs-bugtool.8.gz
/usr/share/man/man8/ovs-ctl.8.gz
/usr/share/man/man8/ovs-dpctl.8.gz
/usr/share/man/man8/ovs-ofctl.8.gz
/usr/share/man/man8/ovs-parse-leaks.8.gz
/usr/share/man/man8/ovs-pki.8.gz
/usr/share/man/man8/ovs-vlan-test.8.gz
/usr/share/man/man8/ovs-vsctl.8.gz
/usr/share/man/man8/ovs-vswitchd.8.gz
/usr/share/openvswitch/bugtool-plugins/
/usr/share/openvswitch/python/
/usr/share/openvswitch/scripts/ovs-bugtool-*
/usr/share/openvswitch/scripts/ovs-ctl
/usr/share/openvswitch/scripts/ovs-lib
/usr/share/openvswitch/scripts/ovs-save
/usr/share/openvswitch/scripts/sysconfig.template
/usr/share/openvswitch/vswitch.ovsschema
/usr/share/doc/openvswitch-%{version}/README.RHEL
/var/lib/openvswitch
