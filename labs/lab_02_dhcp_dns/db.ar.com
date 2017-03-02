$TTL 604800
$ORIGIN ar.com.
@       IN      SOA     ns1.ar.com. adm.ar.com. (
                                2           ; Serial
                           604800           ; Refresh
                            86400           ; Retry
                          2419200           ; Expire
                           604800 )  ; Negative Cache TTL
        IN      NS      ns1.ar.com.
        IN      A       10.0.100.1
v1sw1   IN      A       10.0.1.1
v1sw1   IN      AAAA    2001:0:1::1
        IN      MX      10      server1
ns1     IN      A       10.0.100.1
server1 IN      A       10.0.100.1
server2 IN      CNAME   server1

