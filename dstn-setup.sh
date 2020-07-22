sudo apt update

sudo apt -y install apache2 texinfo

sudo apt -y install autoconf automake
git clone https://github.com/HewlettPackard/netperf /tmp/netperf
cd /tmp/netperf
./autogen.sh
./configure --enable-dirty=yes --enable-demo=yes
make
sudo make install

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

# enable TCP Prague
sudo modprobe tcp_prague
sudo sysctl -w net.ipv4.tcp_ecn=3

