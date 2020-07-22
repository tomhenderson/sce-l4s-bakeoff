sudo apt update

sudo apt -y install fping jq apache2 texinfo

sudo apt -y install autoconf automake
git clone https://github.com/HewlettPackard/netperf /tmp/netperf
cd /tmp/netperf
./autogen.sh
./configure --enable-dirty=yes --enable-demo=yes
make
sudo make install


:'
sudo bash -c "cat >> /etc/systemd/system/netserver.service" << EOL
[Unit]
Description=netperf server
After=network.target

[Service]
ExecStart=/usr/local/bin/netserver -D
User=nobody

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl enable netserver
sudo systemctl start netserver
'


# install python 3
sudo apt -y install python3
# verify python 3 is the default or make it so, e.g.:
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10
sudo apt -y install python3-pip
sudo pip3 install setuptools matplotlib
git clone https://github.com/tohojo/flent /tmp/flent
cd /tmp/flent
make
sudo make install

# enable TCP Prague
sudo modprobe tcp_prague
sudo sysctl -w net.ipv4.tcp_ecn=3


sudo bash -c "cat >> /etc/ssh/ssh_config" << EOL
Host *
   StrictHostKeyChecking no
   UserKnownHostsFile=/dev/null
EOL
