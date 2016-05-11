# Nectar
## How to ssh to a Linux VM
use the private key located at extras/cloud_cluster_computing.pem

```bash
# change the private key's permission to 400 or 600
chmod 400 <path_to_private_key> # In this case it's: chmod extras/cloud_cluster_computing.pem
ssh -i <path_to_private_key> ubuntu@<ip_address_of_vm> # In this case it's: ssh -i extras/cloud_cluster_computering.pem ubuntu@115.146.94.116
```

## How to install CouchDB on Ubuntu
http://askubuntu.com/questions/640288/how-to-install-latest-couchdb-on-ubuntu
```bash
sudo apt-get install python-software-properties
sudo apt-add-repository ppa:couchdb/stable
sudo apt-get update
sudo apt-get install couchdb couchdb-bin couchdb-common -f
```

## How to disk partition & mount
https://help.ubuntu.com/community/InstallingANewHardDrive#Partition_The_Disk
```bash
# partitioning
sudo fdisk <path_to_disk> # In this case it's: sudo fdisk /dev/vdb
# format partition
sudo mkfs -t ext4 <path_to_partition> # In this case it's: sudo mkfs -t ext4 /dev/vdb1
# create a path for the partition to be mounted to
sudo mkdir /media/<dir_name> # In this case it's: sudo mkdir /media/nectar_couchdb
# mount the partition to the path that's created above
sudo mount <path_to_partition> <path_to_mount_dir> # In this case it's: sudo mount /dev/vdb1 /media/nectar_couchdb
```

# Libaries
## Required libraries
```bash
# Ubuntu
pip install nltk twitter couchdb
# Mac
sudo pip install ntlk twitter couchdb
```

# Ansible
## Installation
```bash
# Mac
sudo pip install ansible
# Ubuntu
sudo apt-get install software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible
```

## Install additional module
```bash
# docker-py
sudo pip install docker-py
# shade
sudo pip install shade
```

## Auto Deployment
```bash
# To deploy and update couchdb
sudo ansible-playbook playbooks/deploy-couchdb.yaml
# To deploy and update latest twitter mining application
sudo ansible-playbook playbooks/deploy-twitter-miner.yaml
```

# Docker
## Install
```bash
# Ubuntu
curl -fsSL https://get.docker.com/ | sh
sudo apt-get install docker-engine
# Mac download the dmg file and install
```

# Gulp
## Install
```bash
# Install Node.js
## Ubuntu & Debian
sudo apt-get install -y build-essentials
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install -y nodejs
## Windows and mac can download and install from installers
# Install gulp
npm install -g gulp
```
## Build
```bash
# Make sure you are under the root directory of where the gulpfile is
# Install node modules that's specified in the package.json
npm install
# Step 1 - build and packge the application to dist folder
gulp
# Step 2 - build docker image and push to docker hub
gulp docker-publish
```
