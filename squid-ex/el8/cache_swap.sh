#!/bin/bash
if [ -f /etc/sysconfig/squid ]; then
	. /etc/sysconfig/squid
fi

SQUID_CONF=${SQUID_CONF:-"/etc/squid/squid.conf"}

CACHE_SWAP=`sed -e 's/#.*//g' $SQUID_CONF | \
	grep cache_dir | awk '{ print $3 }'`

for adir in $CACHE_SWAP; do
	if [ ! -d $adir/00 ]; then
		echo -n "init_cache_dir $adir... "
		squid -N -z -F -f $SQUID_CONF >> /var/log/squid/squid.out 2>&1
	fi
done
