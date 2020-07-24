This repo contains tests using Flent to evaluate L4S, following https://github.com/heistp/sce-l4s-bakeoff.

It is designed for use on the [CloudLab](https://www.cloudlab.us/) testbed.


### Instructions

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

To use a different kernel, or to modify the kernel, you may follow these steps :

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

