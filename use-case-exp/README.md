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
cd ansible
ansible-playbook -i inventory.yml install-docker.yml -e @secrets.yml --ask-vault-pass
ansible-playbook -i inventory.yml deploy-demon.yml -e @secrets.yml --ask-vault-pass
cd ..
```

## Run the experiment
```shell
python experiment.py
```