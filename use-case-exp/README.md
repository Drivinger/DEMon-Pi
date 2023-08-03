# Use-case experiment

## Requirements
```shell
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

ansible-galaxy install geerlingguy.docker
ansible-galaxy install geerlingguy.pip
```

## Configure RPi devices and deploy DEMon container
```shell
ansible-playbook -i ansible/inventory.yml ansible/install.yml -e @ansible/secrets.yml --ask-vault-pass
```

## Run the experiment
```shell
python experiment.py
```