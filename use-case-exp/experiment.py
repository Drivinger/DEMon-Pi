import csv
import sys

import geopy.distance as distance
from config import settings
import random
import utils
import requests



def _normalize_distance_to_latency_range(dist: float):
    return ((settings.max_latency - settings.min_latency) * (dist - settings.min_dist) / (settings.max_dist - settings.min_dist)) + settings.min_latency


def _compute_minmax_distances(users: list[dict], servers: list[dict]):
    min_dist = sys.maxsize
    max_dist = 0

    for user in users:
        for server in servers:
            user_coordinates = (user['latitude'], user['longitude'])
            server_coordinates = (server['latitude'], server['longitude'])
            dist = distance.distance(user_coordinates, server_coordinates).meters
            if dist > max_dist:
                max_dist = dist
            if dist < min_dist:
                min_dist = dist

    return min_dist, max_dist


def _sort_edge_serves_by_latency(user: dict, edge_servers: list[dict]):
    user_coordinates = (user['latitude'], user['longitude'])

    for server in edge_servers:
        server_coordinates = (server['latitude'], server['longitude'])
        dist = distance.distance(user_coordinates, server_coordinates).meters
        server['distance'] = dist
        server['latency'] = _normalize_distance_to_latency_range(server['distance'])

    return sorted(edge_servers, key=lambda s: s['latency'])


def _perform_query(user: dict, ranked_servers: list[dict]):
    print(f"### User {user['latitude'], user['longitude']} ###")
    #Get failed nodes
    fail_nodes = _get_failed_nodes(ranked_servers)
    target_nodes = []
    for node in ranked_servers:
        for index, node in ranked_servers:
            # print(f"\t#{counter}: {s}")
            if node in fail_nodes:
                print("Failed node from ranked servers")
                continue
            target_nodes.append(node)

    _perfrom_remote_query(target_nodes)
   

def _perfrom_remote_query(target_servers: list[dict]):
    # API call
    for index, node in target_servers:
        try:       
            response = requests.get("http://{}:{}/reset_get_recent_data_from_nodenode".format(target_servers[index]["ip"], 
                                                                                              target_servers[index]["port"]), timeout=120)
            print("Remote query  response: {}".format(response.text))  

        except Exception as e:
            print("Node with ip {} has error: {}".format(target_servers[index]["ip"], e))

        # TODO= Query logic
   
    
    
def _get_failed_nodes (ranked_servers: list[dict]):
    number_of_failed_nodes = (int)(len(ranked_servers) * settings.failure_rate)
    fail_nodes= [random.choice(ranked_servers) for i in  range(number_of_failed_nodes)]
    return fail_nodes




if __name__ == '__main__':
    main()


def main():
    users = utils.load_csv_dataset_as_dict(settings.users_dataset_filepath)
    edge_servers = utils.load_csv_dataset_as_dict(settings.edge_servers_dataset_filepath)

    min_dist, max_dist = _compute_minmax_distances(users, edge_servers)
    settings.min_dist = min_dist
    settings.max_dist = max_dist

    # start gossip monitoring inside the Rpis
    utils.start_all_nodes (edge_servers)
    # prepare for queries
    for user in users:
        servers_by_latency = _sort_edge_serves_by_latency(user, edge_servers)
        _perform_query(user, servers_by_latency)
