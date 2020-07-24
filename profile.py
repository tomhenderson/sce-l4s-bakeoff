"""CloudLab profile for running the Flent tests in the SCE L4S bakeoff.


Instructions:

To start this experiment on [CloudLab](https://www.cloudlab.us/):

1. Visit the [profile page](https://www.cloudlab.us/p/CloudLab/sce-l4s-bakeoff-git) and click "Next".
2. Parameterize your experiment. If you have forked this repository and made changes, supply the URL to your fork, and the name of the setup scripts to run on the client and receiver nodes. If not, you can keep the default values. Click "Next".
3. The experiment topology will be illustrated on the right side. Choose the "Cloudlab Wisconsin" cluster. Click "Next"
4. Set your experiment duration and click "Finish".
5. Wait while your experiment resources are configured. Then, refer to the instructions in the "Instructions" tab.


### Setup

The setup is automatic. It will take about 30 minutes for your experiment topology to be prepared and for the setup steps to finish.

The designated client setup script in the Git repo will run automatically on the client node when it boots, and the designated server setup script will run automatically on the server (`dstn`) node. The setup scripts will install Flent prerequisites and configure the nodes. 

If you make changes to these scripts, you may need to see the log files to debug your changes. The logs for the startup scripts are located at:

```
/var/tmp/startup-1.txt
```


### Run an experiment

First, make sure that in your CloudLab topology, all nodes appear "green", indicating that they are ready for use.

Then, you can open a terminal session on the client node - right-click on the client node and choose "Shell". This will open another tab inside your CloudLab work area, with a browser-based shell session on the client node. (If you prefer, you can instead use a terminal to SSH into the client node with the SSH details supplied in the "List view" tab.)


```
cd /tmp/custom-repo; bash rewrite-bakeoff.sh; ./run.sh l4s
```

to run all L4S experiments. (Alternatively, you can specify a different batch name, as defined in `bakeoff.batch`.)

It will take around 3-5 hours to run all L4S experiments.

This runs a wrapper script, located in the repository you specified when you started the experiment, that modifies the `bakeoff.batch` file to reflect the hostnames and interface names in your topology.

Then, `run.sh` starts flent with the `bakeoff.batch` script and the batch name you specified.

### View results

You may view or download the results of any experiment in your browser. First, get the URL. In a shell on the client node, run

```
echo "http://$(hostname -f):8000"
```

Copy this URL. Then, run

```
cd /tmp/custom-repo; python2 -m SimpleHTTPServer
```

in your shell on the client node. Then, visit the URL in another tab on your browser to see log files and figures from your experiments.


### Change kernel

The L4S kernel on the `client`, `m1`, `m3`, and `dstn` nodes is from [L4STeam on Github](https://github.com/L4STeam/linux/), commit [3b63cc04e75f3fb450f34aede1b65364a402be80](https://github.com/L4STeam/linux/commit/3b63cc04e75f3fb450f34aede1b65364a402be80).

To use a different kernel, or to modify the kernel, you may follow these steps:

(On the node at which you want to build a new kernel)

first install prerequisites :

```
sudo apt update
sudo apt -y install libelf-dev libssl-dev libncurses-dev flex bison pkg-config gcc
```

Then 
```
cd /kernel
```

Now, you may clone a linux kernel from a github repository of your choice. As an example, you would run this to clone the latest commit from the testing branch of the TCP Prague Github repo :

```
sudo git clone https://github.com/L4STeam/linux.git
cd linux
sudo git checkout testing

```

Make any changes to the code you want to and finally build the kernel :

```
sudo make menuconfig # select options
sudo make -j $(nproc)
sudo make modules_install -j $(nproc)
sudo make install -j $(nproc)
```
After the build finishes, reboot with :

```
sudo reboot
```

Once the node has booted up again, you can verify using :
```
uname -r
```



"""

#
# NOTE: This code was machine converted. An actual human would not
#       write code like this!
#

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal object,
pc = portal.Context()

# Describe the parameter(s) this profile script can accept.
pc.defineParameter( "git", "Link to Git repository containing flent configuration", portal.ParameterType.STRING, "https://github.com/ffund/sce-l4s-bakeoff")
pc.defineParameter( "client", "Name of client setup script", portal.ParameterType.STRING, "client-setup.sh")
pc.defineParameter( "dstn", "Name of server setup script", portal.ParameterType.STRING, "dstn-setup.sh")


# Retrieve the values the user specifies during instantiation.
params = pc.bindParameters()


# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()


# Node client
node_client = request.RawPC('client')
node_client.disk_image = 'urn:publicid:IDN+wisc.cloudlab.us+image+cloudlab-PG0//l4s-apr25'
iface0 = node_client.addInterface('interface-0')
bs0 = node_client.Blockstore("bs0", "/kernel")
bs0.size = "30GB"
node_client.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /usr/bin/git clone " + params.git+ " /tmp/custom-repo; cd /tmp/custom-repo; /usr/bin/sudo bash " + params.client))


# Node M1
node_M1 = request.RawPC('M1')
node_M1.disk_image = 'urn:publicid:IDN+wisc.cloudlab.us+image+cloudlab-PG0//l4s-apr25'
iface1 = node_M1.addInterface('interface-5')
iface2 = node_M1.addInterface('interface-1')
bs1 = node_M1.Blockstore("bs1", "/kernel")
bs1.size = "30GB"


# Node dstn
node_dstn = request.RawPC('dstn')
node_dstn.disk_image = 'urn:publicid:IDN+wisc.cloudlab.us+image+cloudlab-PG0//l4s-apr25'
iface3 = node_dstn.addInterface('interface-8')
bs5 = node_dstn.Blockstore("bs5", "/kernel")
bs5.size = "30GB"
node_dstn.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /usr/bin/git clone " + params.git+ " /tmp/custom-repo; cd /tmp/custom-repo; /usr/bin/sudo bash " + params.dstn))

# Node M2
node_M2 = request.RawPC('M2')
node_M2.disk_image = 'urn:publicid:IDN+wisc.cloudlab.us+image+cloudlab-PG0//l4s-apr25'
iface4 = node_M2.addInterface('interface-4')
iface5 = node_M2.addInterface('interface-2')
bs2 = node_M2.Blockstore("bs2", "/kernel")
bs2.size = "30GB"

# Node M3
node_M3 = request.RawPC('M3')
node_M3.disk_image = 'urn:publicid:IDN+wisc.cloudlab.us+image+cloudlab-PG0//l4s-apr25'
iface6 = node_M3.addInterface('interface-7')
iface7 = node_M3.addInterface('interface-3')
bs3 = node_M3.Blockstore("bs3", "/kernel")
bs3.size = "30GB"

# Node M4
node_M4 = request.RawPC('M4')
node_M4.disk_image = 'urn:publicid:IDN+wisc.cloudlab.us+image+cloudlab-PG0//l4s-apr25'
iface8 = node_M4.addInterface('interface-6')
iface9 = node_M4.addInterface('interface-9')
bs4 = node_M4.Blockstore("bs4", "/kernel")
bs4.size = "30GB"

# Link link-2
link_2 = request.Link('link-2')
link_2.Site('undefined')
link_2.addInterface(iface4)
link_2.addInterface(iface1)

# Link link-3
link_3 = request.Link('link-3')
link_3.Site('undefined')
link_3.addInterface(iface8)
link_3.addInterface(iface6)

# Link link-4
link_4 = request.Link('link-4')
link_4.Site('undefined')
link_4.addInterface(iface3)
link_4.addInterface(iface9)

# Link link-0
link_0 = request.Link('link-0')
link_0.Site('undefined')
link_0.addInterface(iface0)
link_0.addInterface(iface2)

# Link link-1
link_1 = request.Link('link-1')
link_1.Site('undefined')
link_1.addInterface(iface5)
link_1.addInterface(iface7)


# Print the generated rspec
pc.printRequestRSpec(request)
