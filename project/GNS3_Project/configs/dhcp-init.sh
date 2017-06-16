#!/bin/sh

start() {
    echo 'Starting service…' >&2
    sudo dhcpd -6 -d -cf /etc/dhcp/dhcpd6.conf eth0
}

stop() {
  echo 'Stopping service…' >&2
}


case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  retart)
    stop
    start
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|uninstall}"
esac
