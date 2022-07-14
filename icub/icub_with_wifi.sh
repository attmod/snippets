ip route del default via 10.0.0.1
ip route del 10.0.0.0/8

ip route add 10.0.0.2 via 10.0.0.1


ip route get 8.8.8.8
ip route get 10.0.0.2
ip route get 10.255.8.30

