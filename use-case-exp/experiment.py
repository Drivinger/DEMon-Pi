import csv
import sys

import geopy.distance as distance
from config import settings


def _load_csv_dataset_as_dict(filepath: str):
    with open(filepath, 'r') as file:
        dict_reader = csv.DictReader(file)
        return list(dict_reader)


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
    for counter, s in enumerate(ranked_servers, start=1):
        print(f"\t#{counter}: {s}")
    print("\n")


def main():
    users = _load_csv_dataset_as_dict(settings.users_dataset_filepath)
    edge_servers = _load_csv_dataset_as_dict(settings.edge_servers_dataset_filepath)

    min_dist, max_dist = _compute_minmax_distances(users, edge_servers)
    settings.min_dist = min_dist
    settings.max_dist = max_dist

    for user in users:
        servers_by_latency = _sort_edge_serves_by_latency(user, edge_servers)
        _perform_query(user, servers_by_latency)


if __name__ == '__main__':
    main()
