import os
import random
import time
import psutil
import requests
from singleton import Singleton
import logging
import hashlib
import json


def mk_digest(to_digest):
    nested_dict_str = json.dumps(to_digest, sort_keys=True)
    hash_object = hashlib.sha256()
    hash_object.update(nested_dict_str.encode('utf-8'))
    digest = hash_object.hexdigest()
    return digest


def get_new_data():
    node = Node.instance()
    network = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
    data = {
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
            "failureList": node.failure_list,
            "nodeAlive": node.is_alive},
        "appSate": {
            "cpu": "{}".format(psutil.cpu_percent()),
            "memory": "{}".format(psutil.virtual_memory().percent),
            "network": "{}".format(network),
            "storage": "{}".format(psutil.disk_usage('/').free)},
        "nfState": {}}
    digest = mk_digest(data)
    data["digest"] = digest
    return data





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
        self.push_mode = None
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
            if self.push_mode:
                print("Pushing data", flush=True)
                if self.cycle % 3 == 0 and self.cycle != 0:
                    self.push_latest_data_and_delete_after_push()
            self.cycle += 1
            self.transmit(target_count)
            time.sleep(gossip_rate)

    def prepare_metadata_and_own_fresh_data(self, time_key):
        metadata = {}
        own_key = self.ip + ':' + self.port
        own_recent_data = self.data[time_key][own_key]
        for key in self.data[time_key]:
            if 'counter' in self.data[time_key][key] and key is not own_key:
                metadata[key] = self.data[time_key][key]['counter']
        to_send = {'metadata': metadata, own_key: own_recent_data}
        return to_send

    def transmit(self, target_count):
        new_time_key = self.gossip_counter
        if len(self.data) > 0:
            latest_entry = max(self.data.keys(), key=int)
            latest_data = self.data[latest_entry]
            self.data[new_time_key] = latest_data
        else:
            self.data[new_time_key] = {}
        self.data[new_time_key][self.ip + ':' + self.port] = get_new_data()
        random_nodes = self.get_random_nodes(self.node_list, target_count)

        for n in random_nodes:
            self.send_to_node(n, new_time_key)

    def update_failure_data(self, new_time_key, n):
        if self.ip + ':' + self.port not in self.data[new_time_key].get(n["ip"] + ':' + n["port"], {}).get("hbState",
                                                                                                           {}).get(
            "failureList", []):
            self.data[new_time_key][n["ip"] + ':' + n["port"]]["hbState"]["failureList"].append(
                self.ip + ':' + self.port)
            f_count = self.data[new_time_key].get(n["ip"] + ':' + n["port"], {}).get("hbState", {}).get("failureCount",
                                                                                                        0) + 1
            if f_count >= 3:
                self.delete_node_from_nodelist(n["ip"] + ':' + n["port"])
                self.data[new_time_key][n["ip"] + ':' + n["port"]]["hbState"]["nodeAlive"] = False
        pass

    def delete_node_from_nodelist(self, key_to_delete):
        self.node_list.pop(key_to_delete)

    def prepare_requested_data(self, time_key, requested_keys):
        requested_data = {}
        for key in requested_keys:
            requested_data[key] = self.data[time_key][key]
        return requested_data

    def reset_failure_data(self, new_time_key, ip_key):
        if ip_key in self.data[new_time_key]:
            self.data[new_time_key][ip_key]["hbState"]["failureCount"] = 0
            self.data[new_time_key][ip_key]["hbState"]["nodeAlive"] = True
            self.data[new_time_key][ip_key]["hbState"]["failureList"] = []
        else:
            self.data[new_time_key].setdefault(ip_key, {}).setdefault("hbState", {})[
                "failureCount"] = 0
            self.data[new_time_key].setdefault(ip_key, {}).setdefault("hbState", {})[
                "failureList"] = []
            self.data[new_time_key][ip_key]["hbState"]["nodeAlive"] = True

    def update_own_data(self, updates, new_time_key):
        for u_key in updates:
            self.data_flow_per_round.setdefault(self.cycle, {})
            if u_key in self.data[new_time_key]:
                self.data_flow_per_round[self.cycle].setdefault('fd', 0)
                self.data_flow_per_round[self.cycle]['fd'] += 1
            else:
                self.data_flow_per_round[self.cycle].setdefault('nd', 0)
                self.data_flow_per_round[self.cycle].setdefault('fd', 0)
                self.data_flow_per_round[self.cycle]['nd'] += 1
                self.data_flow_per_round[self.cycle]['fd'] += 1
            self.data[new_time_key][u_key] = updates[u_key]

        pass

    def send_to_node(self, n, new_time_key):
        data = self.prepare_metadata_and_own_fresh_data(new_time_key)
        try:
            r_metadata_and_updated = requests.post(
                'http://' + n["ip"] + ':' + '5000' + '/receive_metadata',
                json=data)

            requested_keys = r_metadata_and_updated.json()['requested_keys']
            requested_data = self.prepare_requested_data(new_time_key, requested_keys)
            response = requests.post(
                'http://' + n["ip"] + ':' + '5000' + '/receive_message?inc_round={}'.format(self.cycle),
                json=requested_data)
            self.update_own_data(r_metadata_and_updated.json()['updates'], new_time_key)
            if response.status_code == 500:
                self.update_failure_data(new_time_key, n)
            else:
                self.reset_failure_data(new_time_key, n["ip"] + ':' + n["port"])
        except Exception as e:
            # TODO: in production also add the above failure logic here.
            logging.error("Error while sending message to node {}: {}".format(n, e))

    def set_params(self, ip, port, cycle, node_list, data, is_alive, gossip_counter, failure_counter,
                   monitoring_address, database_address, is_send_data_back, client_thread, counter_thread, data_flow_per_round, push_mode, client_port):
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
        self.data_flow_per_round = data_flow_per_round
        self.is_send_data_back = is_send_data_back
        self.push_mode = push_mode
        self.client_port = client_port

    def get_random_nodes(self, node_list, target_count):
        new_node_list = []
        for node in node_list:
            if self.ip == node['ip']:
                continue
            new_node_list.append(node)
        random_os_data = os.urandom(16)
        seed = int.from_bytes(random_os_data, byteorder="big")
        random.seed(seed)
        return random.sample(new_node_list, target_count)

    def push_latest_data_and_delete_after_push(self):
        if self.data:
            latest_time_key = max(self.data.keys())
            latest_data = self.data[latest_time_key]
            to_send = self.data
            self.data = {latest_time_key: latest_data}
            to_push = {k: v for k, v in to_send.items() if k != latest_time_key}
            self.session_to_monitoring.post(
                'http://{}:{}/push_data_to_database?ip={}&port={}&round={}'.format(self.monitoring_address,self.client_port ,self.ip,
                                                                                 self.port,
                                                                                 self.cycle), json=to_push)

