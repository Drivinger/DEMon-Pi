# Demon Monitoring System Emulation

This is an emulation of the Demon Monitoring System, comprising three primary components: `monitoring_exp`, `demon`, and `config`. The system enables you to manage Docker containers running Demon instances and configure experiment hyperparameters.

## Components

### 1. [`monitoring_exp.py`](`/monitoring_exp.py`)

The `monitoring_exp` component is responsible for creating and scaling Docker containers running Demon. It provides a Flask server with essential endpoints for controlling experiments.

### 2. `demon`

The `demon` component is the core of the system, running within each Docker container. It performs monitoring and management tasks, making it an integral part of the Demon Monitoring System.

### 3. `config.ini`

The `config` component allows you to configure experiment hyperparameters. Customize the behavior of the Demon Monitoring System by editing the `config.ini` file.

## How to Run

Follow these steps to run the Demon Monitoring System emulation:

### 1. Build the Docker Image

In the `src/demon` directory, build the Docker image using the provided `dockerImage.dockerfile`:
    
   ```bash
docker build -f dockerImage.dockerfile -t demonv1 .
```

### 2. Configure Parameters

Edit the `config.ini` file in the `config` directory. Ensure the `docker_ip` parameter is correctly set for communication with the Docker client.

### 3. Start `monitoring_exp.py`

Run the `monitoring_exp.py` script. It launches a Flask server with your hosts ip-address with key endpoints:

- To initiate experiments based on the configured settings, visit: `http://_ip_:4000/start`
- To delete all Docker containers with the specified Docker image at any time, visit: `http://_ip_:4000/delete_nodes`

### 4. Create Demon Nodes

Once `monitoring_exp.py` is running, it will create a specified range of Demon nodes and start Demon instances in each of them.

### 5. Monitor and Manage Experiments

Observe the behavior and performance of your Demon instances during the experiments. Adjust parameters as needed in the `config.ini` file to optimize performance.

### 6. Cleanup After Experiments

After completing all experiments, the script will automatically delete all created nodes and provide a success message.
