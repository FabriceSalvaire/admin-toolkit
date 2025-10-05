

```
uname -a
Linux isis.home 6.16.8-200.fc42.x86_64 #1 SMP PREEMPT_DYNAMIC Fri Sep 19 17:47:18 UTC 2025 x86_64 GNU/Linux

/etc/redhat-release -> fedora-release
/etc/system-release -> fedora-release

/etc/redhat-release
Fedora release 42 (Adams)

/etc/system-release-cpe
cpe:/o:fedoraproject:fedora:42

import socket
socket.gethostname()

os.uname()
posix.uname_result(sysname='Linux', nodename='isis.home', release='6.16.8-200.fc42.x86_64', version='#1 SMP PREEMPT_DYNAMIC Fri Sep 19 17:47:18 UTC 2025', machine='x86_64')
```

```
ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
        valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute
        valid_lft forever preferred_lft forever
2: enp0s25: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000
    link/ether 50:7b:9d:88:84:a1 brd ff:ff:ff:ff:ff:ff
    altname enx507b9d8884a1
3: wlp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 2e:95:f6:a5:e1:0e brd ff:ff:ff:ff:ff:ff permaddr 18:5e:0f:77:ec:0a
    altname wlx185e0f77ec0a
    inet 192.168.1.14/24 brd 192.168.1.255 scope global dynamic noprefixroute wlp3s0
    valid_lft 83052sec preferred_lft 83052sec
    inet6 2a01:cb00:11de:5800:17f1:7346:5528:d128/64 scope global dynamic noprefixroute
        valid_lft 1793sec preferred_lft 593sec
    inet6 fe80::d241:d1e1:8bcf:3b18/64 scope link noprefixroute
        valid_lft forever preferred_lft forever
4: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UNKNOWN group default qlen 500
    link/none
    inet 172.17.1.6 peer 172.17.1.5/32 scope global tun0
        valid_lft forever preferred_lft forever
    inet6 fe80::cfb2:853d:67bd:ebe/64 scope link stable-privacy proto kernel_ll
        valid_lft forever preferred_lft forever

ip -json addr
[{"ifindex":1,"ifname":"lo","flags":["LOOPBACK","UP","LOWER_UP"],"mtu":65536,"qdisc":"noqueue","operstate":"UNKNOWN","group":"default","txqlen":1000,"link_type":"loopback","address":"00:00:00:00:00:00","broadcast":"00:00:00:00:00:00","addr_info":[{"family":"inet","local":"127.0.0.1","prefixlen":8,"scope":"host","label":"lo","valid_life_time":4294967295,"preferred_life_time":4294967295},{"family":"inet6","local":"::1","prefixlen":128,"scope":"host","noprefixroute":true,"valid_life_time":4294967295,"preferred_life_time":4294967295}]},{"ifindex":2,"ifname":"enp0s25","flags":["NO-CARRIER","BROADCAST","MULTICAST","UP"],"mtu":1500,"qdisc":"fq_codel","operstate":"DOWN","group":"default","txqlen":1000,"link_type":"ether","address":"50:7b:9d:88:84:a1","broadcast":"ff:ff:ff:ff:ff:ff","altnames":["enx507b9d8884a1"],"addr_info":[]},{"ifindex":3,"ifname":"wlp3s0","flags":["BROADCAST","MULTICAST","UP","LOWER_UP"],"mtu":1500,"qdisc":"noqueue","operstate":"UP","group":"default","txqlen":1000,"link_type":"ether","address":"2e:95:f6:a5:e1:0e","broadcast":"ff:ff:ff:ff:ff:ff","permaddr":"18:5e:0f:77:ec:0a","altnames":["wlx185e0f77ec0a"],"addr_info":[{"family":"inet","local":"192.168.1.14","prefixlen":24,"broadcast":"192.168.1.255","scope":"global","dynamic":true,"noprefixroute":true,"label":"wlp3s0","valid_life_time":83031,"preferred_life_time":83031},{"family":"inet6","local":"2a01:cb00:11de:5800:17f1:7346:5528:d128","prefixlen":64,"scope":"global","dynamic":true,"noprefixroute":true,"valid_life_time":1773,"preferred_life_time":573},{"family":"inet6","local":"fe80::d241:d1e1:8bcf:3b18","prefixlen":64,"scope":"link","noprefixroute":true,"valid_life_time":4294967295,"preferred_life_time":4294967295}]},{"ifindex":4,"ifname":"tun0","flags":["POINTOPOINT","MULTICAST","NOARP","UP","LOWER_UP"],"mtu":1500,"qdisc":"fq_codel","operstate":"UNKNOWN","group":"default","txqlen":500,"link_type":"none","addr_info":[{"family":"inet","local":"172.17.1.6","address":"172.17.1.5","prefixlen":32,"scope":"global","label":"tun0","valid_life_time":4294967295,"preferred_life_time":4294967295},{"family":"inet6","local":"fe80::cfb2:853d:67bd:ebe","prefixlen":64,"scope":"link","stable-privacy":true,"protocol":"kernel_ll","valid_life_time":4294967295,"preferred_life_time":4294967295}]}]
```
