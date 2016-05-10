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
sudo pip install ansible
```

# Docker
## Install
```bash
# Ubuntu
curl -fsSL https://get.docker.com/ | sh
sudo apt-get install docker-engine
# Mac download the dmg file
```
