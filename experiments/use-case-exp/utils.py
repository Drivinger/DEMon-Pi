import csv
import glob
import random
from config import settings
import requests
import socket
import uuid
import base64
import json

def load_csv_dataset_as_dict(filepath: str):
    with open(filepath, 'r') as file:
        dict_reader = csv.DictReader(file)
        return list(dict_reader)

def start_all_nodes(edge_servers: list[dict]):
                    
    external_monitoring_agent_ip =   socket.gethostbyname(socket.gethostname())
    target_count = settings
    for index_id, _ in enumerate(edge_servers):
        
        target_count = settings.target_count
        gossip_rate = settings.gossip_rate
        is_send_data_back = settings.is_send_data_back
        start_node(index_id, external_monitoring_agent_ip, edge_servers, target_count, gossip_rate,
                    is_send_data_back)


def start_node(index, external_monitoring_agent_ip, edge_servers, target_count, gossip_rate, is_send_data_back ):
    to_send = {"node_list": edge_servers, "target_count": target_count, "gossip_rate": gossip_rate,
               "database_address": "", "monitoring_address": external_monitoring_agent_ip,
               "node_ip": edge_servers[index]["ip"], "is_send_data_back": is_send_data_back }
    print("Sending the start  request to the node. IP:{}".format(edge_servers[index]["ip"]))
    try:
        response = requests.post("http://{}:{}/start_node".format(edge_servers[index]["ip"], edge_servers[index]["port"]), json=to_send)
        print("Starting the node {}, port:{}, Node list:{}. Response: {}".format(edge_servers[index]["ip"], edge_servers[index]["port"], edge_servers, response.text))
    except Exception as e:
        print("Node with ip {} not started: {}".format(edge_servers[index]["ip"], e))

def offload_object_detection_task(node_ip):

    try:
        # Get random image from the images folder
        images = []
        for image_file in glob.iglob(f"{settings.sample_image_dataset_filepath}/*.jpg"):
            images.append(image_file)
        image = random.choice(images)

        # object_detection API endopint
        url = f"http://{node_ip}:{settings.app_port}/api/object_detection"

        payload = {}
        #generate uuid for image
        id = uuid.uuid5(uuid.NAMESPACE_OID, image)
        payload['id'] = str(id)

        # Encode image into base64 string
        with open (image, 'rb') as image_file:
            payload['image'] = base64.b64encode(image_file.read()).decode('utf-8')

        print(f"Sending request to: {url}")

        headers = {'Accept': 'application/json'}
        response = requests.post(url, json=payload, headers=headers)
        if response.ok:
            print(response.json())
        else:
            print(f"An error occurred offloading request to node {node_ip} (status code: {response.status_code})")
            print(f"{response.json()}")

    except Exception as e:
        print(f"Exception in offloading request: {e}")