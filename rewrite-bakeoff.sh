client_right=$(ip route get 10.10.4.2 | grep -oP "(?<=dev )[^ ]+")
m1_left=$(sudo ssh m1 -f ip route get 10.10.4.1 | grep -oP "(?<=dev )[^ ]+")
m1_right=$(sudo ssh m1 -f ip route get 10.10.1.1 | grep -oP "(?<=dev )[^ ]+")
m2_left=$(sudo ssh m2 -f ip route get 10.10.1.2 | grep -oP "(?<=dev )[^ ]+")
m2_right=$(sudo ssh m2 -f ip route get 10.10.5.2 | grep -oP "(?<=dev )[^ ]+")
dstn_left=$(sudo ssh dstn -f ip route get 10.10.3.2 | grep -oP "(?<=dev )[^ ]+")

sudo sed -i "s/RIGHTCLIFACE/$client_right/g" bakeoff.batch
sudo sed -i "s/LEFTM1IFACE/$m1_left/g" bakeoff.batch
sudo sed -i "s/RIGHTM1IFACE/$m2_right/g" bakeoff.batch
sudo sed -i "s/LEFTM2IFACE/$m2_left/g" bakeoff.batch
sudo sed -i "s/RIGHTM2IFACE/$m2_right/g" bakeoff.batch
sudo sed -i "s/LEFTDSIFACE/$dstn_left/g" bakeoff.batch



