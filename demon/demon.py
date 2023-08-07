import signal
import time

import requests
from flask import Flask, request
from node import Node
import threading
import logging
import json

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
gossip = Flask(__name__)


# TODO: implement logging mode
@gossip.route('/receive_message', methods=['POST'])
def receive_message():
    if not Node.instance().is_alive:
        # reset_node()
        return "Dead Node", 500
    compare_and_update_node_data(request.get_json())
    return "OK"


@gossip.route('/reset_node')
def reset_node():
    node = Node.instance()
    node.is_alive = False
    node.client_thread.join()
    node.counter_thread.join()
    node.set_params(None, None, 0, None, {}, False, 0, 0, None, None, None, None, {})
    return "OK"


@gossip.route('/stop_node')
def stop_node():
    node = Node.instance()
    node.is_alive = False
    node.client_thread.join()
    node.counter_thread.join()
    return "OK"


def compare_and_update_node_data(inc_data):
    # TODO: update & propagate new node_list? (send data{realdata, node_list}), new data per round
    node = Node.instance()
    new_time_key = node.gossip_counter
    latest_entry = max(node.data.keys(), key=int) if len(node.data) > 0 else new_time_key
    new_data = inc_data
    # new_data = inc_data['data']
    # new_node_list = inc_data['node_list']
    all_keys = set().union(node.data[latest_entry].keys(), new_data.keys())
    inc_round = int(request.args.get('inc_round'))
    # received messages ['rm'] per round
    node.data_flow_per_round.setdefault(inc_round, {}).setdefault('rm', 0)
    node.data_flow_per_round[inc_round]['rm'] += 1

    # lists of ips who reclaim that this node is dead
    list1 = []
    list2 = []
    for key in all_keys:
        # both nodes store the data if IP
        if key in node.data[latest_entry] and key in new_data:
            list1 = node.data[latest_entry][key]["hbState"]["failureList"]
            list2 = new_data[key]["hbState"]["failureList"]
            if ('counter' in new_data[key] and 'counter' in node.data[latest_entry][key] \
                and float(new_data[key]['counter']) > float(node.data[latest_entry][key]['counter'])) or \
                    ('counter' in new_data[key] and 'counter' not in node.data[latest_entry][key]):
                node.data.setdefault(new_time_key, {})[key] = new_data[key]

                # fresh data per round ['fd'] per round, fresh data describes data that is updated or added in this node
                node.data_flow_per_round[inc_round].setdefault('fd', 0)
                node.data_flow_per_round[inc_round]['fd'] += 1
            else:
                node.data.setdefault(new_time_key, {})[key] = node.data[latest_entry][key]
        # inc data doesnt store the data of IP
        elif key in node.data[latest_entry] and key not in new_data:
            node.data.setdefault(new_time_key, {})[key] = node.data[latest_entry][key]
        # node doesnt store the data of IP
        else:
            node.data.setdefault(new_time_key, {})[key] = new_data[key]
            # node.data[key] = new_data[key]
            # new data per round ['nd'] per round (nd is data from an unknown node -> fd = nd)
            node.data_flow_per_round[inc_round].setdefault('nd', 0)
            node.data_flow_per_round[inc_round].setdefault('fd', 0)
            node.data_flow_per_round[inc_round]['nd'] += 1
            node.data_flow_per_round[inc_round]['fd'] += 1
        # only for deleted nodes
        if key in node.data[latest_entry] and key in new_data:
            merged_failure_list = list(set(list1).union(set(list2)))
            node.data[new_time_key][key]["hbState"]["failureList"] = merged_failure_list
    # TODO update Database
    # send both data and data_flow_per_round to monitor
    # TODO: Save latest data snapshot with key = self.gossip_counter in data
    if new_time_key not in node.data:
        print("No new data to send", flush=True)
        data_to_send_to_monitor = node.data[latest_entry]
    else:
        data_to_send_to_monitor = node.data[new_time_key]

    to_send = {'data': data_to_send_to_monitor, 'data_flow_per_round': node.data_flow_per_round[inc_round]}
    # TODO: Session here# 
    #Shashi- posting to external config.. Receive data in monitoring... 

    if node.is_send_data_back is True:

        node.session_to_monitoring.post(
            'http://{}:4000/receive_node_data?ip={}&port={}&round={}'.format(node.monitoring_address, node.ip, node.port,
                                                                         inc_round), json=to_send)


@gossip.route('/start_node', methods=['POST'])
def start_node():
    init_data = request.get_json()
    monitoring_address = init_data["monitoring_address"]
    database_address = init_data["database_address"]
    node_list = init_data["node_list"]
    target_count = init_data["target_count"]
    gossip_rate = init_data["gossip_rate"]
    node_ip = init_data["node_ip"]
    is_send_data_back = init_data["is_send_data_back"]
    node = Node.instance()
    time.sleep(10)
    client_thread = threading.Thread(target=node.start_gossiping, args=(target_count, gossip_rate))
    counter_thread = threading.Thread(target=node.start_gossip_counter)
    node.set_params(node_ip,
                    request.headers.get('Host').split(':')[1], 0,
                    node_list, {}, True, 0, 0, monitoring_address,  database_address,  is_send_data_back = is_send_data_back,
                    client_thread=client_thread, counter_thread=counter_thread,  data_flow_per_round={})
    client_thread.start()
    counter_thread.start()
    return "OK"


# Todo: add method to ask for registration
@gossip.route('/register_new_node', methods=['POST'])
def register_new_node():
    Node.instance().node_list.append(request.get_json())
    return "OK"

# With all the current and past time stamps -> Whole gossip cycle
@gossip.route('/get_data_from_node', methods=['GET'])
def get_data_from_node():
    return Node.instance().data

# Recent time stamp data..
@gossip.route('/get_recent_data_from_node', methods=['GET'])
def get_recent_data_from_node():
    data = Node.instance().data
    latest_entry = max(data.keys(), key=int)
    return data[latest_entry]


@gossip.route('/get_nodelist_from_node', methods=['GET'])
def get_nodelist_from_node():
    return json.dumps(Node.instance().node_list)

@gossip.route('/hello_world', methods=['GET'])
def get_hello_from_node():
    return "Hello from gossip agent!"


if __name__ == "__main__":
    # get port from container
    gossip.run(host='0.0.0.0', debug=True, threaded=True)
