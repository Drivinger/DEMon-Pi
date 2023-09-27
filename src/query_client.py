import random
import requests


def query(node_list, quorum_size, target_node_ip, target_node_port):
    while True:
        random_nodes = random.sample(node_list, quorum_size)
        metadatas = {}
        total_messages_for_query = 0
        for n in random_nodes:
            total_messages_for_query += 1
            try:
                r = requests.get("http://" + n["ip"] + ":" + n["port"] + "/metadata")
                metadatas[n["ip"] + ":" + n["port"]] = r.json()[target_node_ip + ":" + target_node_port]
            except:
                print("Node " + n["ip"] + ":" + n["port"] + " is not responding")
        counter_consensus = all(data['counter'] == list(metadatas.values())[0]['counter'] for data in metadatas.values())
        if counter_consensus:
            digest_consensus = all(data['digest'] == list(metadatas.values())[0]['digest'] for data in metadatas.values())
            if digest_consensus:
                response_from_query_client = requests.get(
                    "http://{}:{}/get_recent_data_from_node".format(random_nodes[0]["ip"], random_nodes[0]["port"]))
                query_result = response_from_query_client.json()[target_node_ip + ":" + target_node_port]
                print("Query result: " + query_result)
                return total_messages_for_query, query_result
