import configparser

import requests
from flask import Flask, request
import socket

monitoring_demon = Flask(__name__)
parser = configparser.ConfigParser()
parser.read('demonMonitoringPi.ini')


def prepare_experiment(server_ip, node_list):
    # prepare pis here or manual/script before?
    # get ips from pis
    target_count = parser.getint('DemonParam', 'target_count')
    gossip_rate = parser.getint('DemonParam', 'gossip_rate')

    start_all_nodes(node_list, server_ip, target_count, gossip_rate)
    pass
@monitoring_demon.route('/receive_node_data', methods=['POST'])
def update_data_entries_per_ip():
    global experiment
    client_ip = request.args['ip']
    client_port = request.args['port']
    round = request.args['round']
    inc = request.get_json()
    data_stored_in_node = inc["data"]
    data_flow_per_round = inc["data_flow_per_round"]

    nd = data_flow_per_round.setdefault('nd', 0)
    fd = data_flow_per_round.setdefault('fd', 0)
    rm = data_flow_per_round.setdefault('rm', 0)
    # information count
    ic = len(data_stored_in_node)
    #bytes_of_data = len(json.dumps(data_stored_in_node).encode('utf-8'))

    # TODO: save information from data_flow_per_round to database
    print("IP: {} got {} informations stored in node".format(client_ip, ic))
    return "OK"


def start_all_nodes(node_list, monitoring_address, target_count, gossip_rate):
    for i, node in enumerate(node_list):
        start_node(i, monitoring_address, node_list, target_count, gossip_rate)


def start_node(index, monitoring_address, node_list, target_count, gossip_rate):
    to_send = {"node_list": node_list, "target_count": target_count, "gossip_rate": gossip_rate,
               "database_address": "", "monitoring_address": monitoring_address,
               "node_ip": node_list[index]["ip"]}
    try:
        a = requests.post("http://{}:{}/start_node".format(node_list[index]["ip"], node_list[index]["port"]), json=to_send)
        print(a.text)
    except Exception as e:
        print("Node with ip {} not started: {}".format(node_list[index]["ip"], e))


def update_during_experiment():
    # when finish?
    # what should we save and how (db, file, etc.)?
    pass


def reset_experiment(node_list):
    for node in node_list:
        reset_node(node["ip"], node["port"])
    pass


def reset_node(ip, port):
    try:
        requests.get("http://{}:{}/reset_node".format(ip, port), timeout=120)
    except Exception as e:
        print("An error occurred while resetting node with ip {} request: {}".format(ip, e))


@monitoring_demon.route('/start', methods=['GET'])
def start_demon():
    server_ip = socket.gethostbyname(socket.gethostname())

    node_list = [{"id": ", "ip": "", "port": 5000}]

    print("Server IP: {}".format(server_ip))
    # multiple runs?
    prepare_experiment(server_ip, node_list)
    print("Experiment prepared")
    update_during_experiment()
    print("Experiment finished")
    reset_experiment(node_list)
    print("Experiment reset")
    return "OK - Experiment finished"

if __name__ == "__main__":
    monitoring_demon.run(host='0.0.0.0', port=4000, debug=False, threaded=True)
