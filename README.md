# Nectar

## How to ssh to a Linux VM
use the private key located at extras/cloud_cluster_computing.pem

```bash
# change the private key's permission to 400 or 600
chmod 400 <path_to_private_key> # In this case it's: chmod extras/cloud_cluster_computing.pem
ssh -i <path_to_private_key> ubuntu@<ip_address_of_vm> # In this case it's: ssh -i extras/cloud_cluster_computering.pem ubuntu@115.146.94.116
```