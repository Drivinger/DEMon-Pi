import os
import random
import time
import psutil
import requests
from singleton import Singleton
import logging


# TODO: implement logging, database and monitoring mode
# TODO: implement node_list update and dead_node_list for monitoring mode
def get_new_data():
    node = Node.instance()
    network = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
    return {
        "counter": "{}".format(node.gossip_counter),
        "cycle": "{}".format(node.cycle),
        "digest": "",
        "nodeState": {
            "id": "",
            "ip": "{}".format(node.ip),
            "port": "{}".format(node.port)},
        "hbState": {
            "timestamp": "{}".format(time.time()),
            "failureCount": node.failure_counter,
            "failureList": node.failure_list,# TODO: implement failure list
            "nodeAlive": node.is_alive},
        "appSate": {
            "cpu": "{}".format(psutil.cpu_percent()),
            "memory": "{}".format(psutil.virtual_memory().percent),
            "network": "{}".format(network),
            "storage": "{}".format(psutil.disk_usage('/').free)},
        "nfState": {}}


@Singleton
class Node:
    def __init__(self):
        self.ip = None
        self.port = None
        self.cycle = None
        self.node_list = None
        self.data = None
        self.data_flow_per_round = None
        self.is_alive = None
        self.gossip_counter = None
        self.failure_counter = None
        self.failure_list = []
        self.monitoring_address = None
        self.database_address = None
        self.client_thread = None
        self.counter_thread = None
        self.data_flow_per_round = None
        self.session_to_monitoring = requests.Session()
        self.is_send_data_back = None

    def start_gossip_counter(self):
        while self.is_alive:
            self.gossip_counter += 1
            time.sleep(1)

    def start_gossiping(self, target_count, gossip_rate):
        print("Starting gossiping with target count: {} and gossip rate: {} and length of node list: {}".format(
            target_count, gossip_rate, len(self.node_list)),
              flush=True)
        while self.is_alive:
            self.cycle += 1
            self.transmit(target_count)
            time.sleep(gossip_rate)

    def transmit(self, target_count):

        # TODO: Save latest data snapshot with key = self.gossip_counter in data
        new_time_key = self.gossip_counter

        if len(self.data) > 0:
            latest_entry = max(self.data.keys(), key=int)
            latest_data = self.data[latest_entry]
            self.data[new_time_key] = latest_data
        else:
            print("No data in data dict", flush=True)
            self.data[new_time_key] = {}
        self.data[new_time_key][self.ip + ':' + self.port] = get_new_data()
        random_nodes = self.get_random_nodes(self.node_list, target_count)
        # latest_entry = max(self.data.keys(), key=int)
        # latest_data = self.data[latest_entry]
        for n in random_nodes:
            # TODO: for raspberry pi use http://' + n["ip"] + ':' + n["port"] + '/receive_message
            # TODO: set max retries higher
            try:
                response = requests.post(
                    'http://' + n["ip"] + ':' + '5000' + '/receive_message?inc_round={}'.format(self.cycle),
                    json=self.data[new_time_key], timeout=20)
                if response.status_code == 500:
                    print("Node {}:{} seems to be dead".format(n["ip"], n["port"]), flush=True)
                    # TODO: No Failure count, but list of nodes, which describe this node is dead, if list length (unique nodes) >= 3, remove node from node_list
                    f_count = self.data[new_time_key].get(n["ip"] + ':' + n["port"], {}).get("hbState", {}).get("failureCount", 0) + 1
                    if self.ip + ':' + self.port not in self.data[new_time_key].get(n["ip"] + ':' + n["port"], {}).get("hbState", {}).get("failureList", []):
                        self.data[new_time_key][n["ip"] + ':' + n["port"]]["hbState"]["failureList"].append(self.ip + ':' + self.port)
                    f_list = self.data[new_time_key][n["ip"] + ':' + n["port"]]["hbState"]["failureList"]
                    # self.data[new_time_key][n["ip"] + ':' + n["port"]]["counter"] = self.gossip_counter
                    print("f_list: {}".format(f_list), flush=True)
                    if len(f_list) >= 3:
                        index = next((i for i, entry in enumerate(self.node_list) if
                                      entry["ip"] == n["ip"] and entry["port"] == n["port"]), None)
                        if index is not None:
                            self.node_list[index]["is_alive"] = False
                            print("Node {} {} is dead".format(n["ip"], n["port"]), flush=True)
                        self.data[new_time_key][n["ip"] + ':' + n["port"]]["hbState"]["nodeAlive"] = False
                else:
                    ip_key = n["ip"] + ':' + n["port"]
                    if ip_key in self.data[new_time_key]:
                        self.data[new_time_key][ip_key]["hbState"]["failureCount"] = 0
                        self.data[new_time_key][ip_key]["hbState"]["nodeAlive"] = True
                        self.data[new_time_key][ip_key]["hbState"]["failureList"] = []
                    else:
                        print("NO KEY IN DATA !!!! {} is alive".format(ip_key), flush=True)
                        self.data[new_time_key].setdefault(ip_key, {}).setdefault("hbState", {})[
                            "failureCount"] = 0
                        self.data[new_time_key].setdefault(ip_key, {}).setdefault("hbState", {})[
                            "failureList"] = []
                        self.data[new_time_key][ip_key]["hbState"]["nodeAlive"] = True
            except Exception as e:
                logging.error("Error while sending message to node {}: {}".format(n, e))

    def set_params(self, ip, port, cycle, node_list, data, is_alive, gossip_counter, failure_counter,
                   monitoring_address,  database_address,  is_send_data_back, client_thread, counter_thread, data_flow_per_round):
        self.ip = ip
        self.port = port
        self.monitoring_address = monitoring_address
        self.database_address = database_address
        self.cycle = cycle
        self.node_list = node_list
        self.data = data
        self.is_alive = is_alive
        self.gossip_counter = gossip_counter
        self.failure_counter = failure_counter
        self.client_thread = client_thread
        self.counter_thread = counter_thread
        self.is_send_data_back = is_send_data_back

        self.data_flow_per_round = data_flow_per_round

    def get_random_nodes(self, node_list, target_count):
        node_list = [n for n in node_list if n["ip"] != self.ip and n["port"] != self.port and n["is_alive"]]
        random_os_data = os.urandom(16)
        seed = int.from_bytes(random_os_data, byteorder="big")
        random.seed(seed)
        print("### Node list length:{}, target count :{}".format(len(node_list), target_count))
        return random.sample(node_list, target_count)
