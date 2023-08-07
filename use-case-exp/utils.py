import csv
from config import settings
import requests
import socket

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
        print("Starting the node. Response: {}".format(response.text))
    except Exception as e:
        print("Node with ip {} not started: {}".format(edge_servers[index]["ip"], e))