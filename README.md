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

# Libaries
## Required libraries
```bash
# Ubuntu
pip install nltk twitter couchdb
# Mac
sudo pip install ntlk twitter couchdb
```