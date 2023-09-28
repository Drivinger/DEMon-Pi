import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm, rcParams

dbname = 'experiments.db'



class DemonDataDB:
    def __init__(self):
        self.connection = sqlite3.connect(dbname, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_runs_grouped_by_node_target_avg(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT node_count, target_count, AVG(convergence_round), AVG(convergence_message_count) FROM run_gc "
                "GROUP BY node_count, target_count")
            grouped_runs = self.cursor.fetchall()
            self.connection.close()
            return grouped_runs
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_delta_byte_grouped_by_node_count_and_round_50(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            # round < 8 -> 7 is convergence round
            self.cursor.execute(
                "SELECT SUM(delta_byte) from delta_each_round_storage WHERE round < 8 AND run_id = 1")
            rounds = self.cursor.fetchall()
            return rounds
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_delta_byte_grouped_by_node_count_and_round_100(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                # round < 9 -> 8 is convergence round
                "SELECT SUM(delta_byte) from delta_each_round_storage WHERE round < 9 AND run_id = 7")
            rounds = self.cursor.fetchall()
            return rounds
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_delta_byte_grouped_by_node_count_and_round_150(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            # round < 11 -> 10 is convergence round
            self.cursor.execute(
                "SELECT SUM(delta_byte) from delta_each_round_storage WHERE round < 11 AND run_id = 3")
            rounds = self.cursor.fetchall()
            return rounds
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_delta_byte_grouped_by_node_count_and_round_200(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            # round < 13 -> 12 is convergence round
            self.cursor.execute(
                "SELECT SUM(delta_byte) from delta_each_round_storage WHERE round < 13 AND run_id = 8")
            rounds = self.cursor.fetchall()
            return rounds
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_delta_byte_grouped_by_node_count_and_round_250(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            # round < 19 -> 18 is convergence round
            self.cursor.execute(
                "SELECT SUM(delta_byte) from delta_each_round_storage WHERE round < 19 AND run_id = 5")
            rounds = self.cursor.fetchall()
            return rounds
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_delta_byte_grouped_by_node_count_and_round_300(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            # round < 26 -> 25 is convergence round
            self.cursor.execute(
                "SELECT SUM(delta_byte) from delta_each_round_storage WHERE round < 26 AND run_id = 6")
            rounds = self.cursor.fetchall()
            return rounds
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_messages_grouped_by_round_gc_2(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT round,sum(nd) AS nd_sum from round_of_node WHERE run_id = 48 GROUP BY round")
            rounds = self.cursor.fetchall()
            return rounds
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_messages_grouped_by_round_gc_3(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT round,sum(nd) AS nd_sum from round_of_node WHERE run_id = 50 GROUP BY round")
            rounds = self.cursor.fetchall()
            return rounds
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_messages_grouped_by_round_gc_4(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT round,sum(nd) AS nd_sum from round_of_node WHERE run_id = 52 GROUP BY round")
            rounds = self.cursor.fetchall()
            return rounds
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_fogmon_runs_grouped_by_node_target_avg(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT node_count, target_count, AVG(convergence_round), AVG(convergence_message_count) FROM run_fogmon "
                "GROUP BY node_count, target_count")
            grouped_runs = self.cursor.fetchall()
            self.connection.close()
            return grouped_runs
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_runs_grouped_by_node_rate(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT node_count, gossip_rate, AVG(convergence_round), AVG(convergence_message_count), AVG(convergence_time) FROM run_gr "
                "GROUP BY node_count, gossip_rate")
            grouped_runs = self.cursor.fetchall()
            self.connection.close()
            return grouped_runs
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_sum_aoi_group_by_node_timer(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT node_count,gossip_count, snapshot_timer,AVG(aoi) from age_of_information GROUP BY node_count,gossip_count, snapshot_timer ORDER BY node_count,gossip_count, snapshot_timer")
            rounds = self.cursor.fetchall()
            return rounds
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_fresh_data_grouped_by_round_gc_2(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT round,sum(fd) AS fd_sum from rounds_of_node_incl_after_conv WHERE (run_id = 11 OR run_id = 9) AND round < 41 GROUP BY round")
            rounds = self.cursor.fetchall()
            return rounds
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_fresh_data_grouped_by_round_gc_3(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT round,sum(fd) AS fd_sum from rounds_of_node_incl_after_conv WHERE (run_id = 12 OR run_id = 13) AND round < 41 GROUP BY round")
            rounds = self.cursor.fetchall()
            return rounds
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_fresh_data_grouped_by_round_gc_4(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT round,sum(fd) AS fd_sum from rounds_of_node_incl_after_conv WHERE (run_id = 15 OR run_id = 16) AND round < 41 GROUP BY round")
            rounds = self.cursor.fetchall()
            return rounds
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_byte_grouped_by_round_gc_4(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT round,sum(bytes_of_data) AS bytes_sum from round_of_node WHERE run_id = 52 OR run_id = 53 OR run_id = 54 GROUP BY round")
            rounds = self.cursor.fetchall()
            return rounds
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_byte_grouped_by_round_gc_3(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT round,sum(bytes_of_data) AS bytes_sum from round_of_node WHERE run_id = 50 or run_id = 49 OR run_id = 51 GROUP BY round")
            rounds = self.cursor.fetchall()
            return rounds
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_byte_grouped_by_round_gc_2(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT round,sum(bytes_of_data) AS bytes_sum from round_of_node WHERE run_id = 48 OR run_id = 46 OR run_id = 47 GROUP BY round")
            rounds = self.cursor.fetchall()
            return rounds
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_runs_grouped_by_node_rate_count(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT node_count, gossip_rate,target_count, AVG(convergence_time) FROM run_gc_gr_time "
                "GROUP BY node_count, gossip_rate, target_count")
            grouped_runs = self.cursor.fetchall()
            self.connection.close()
            return grouped_runs
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_delta_byte_grouped_by_node_count_and_round_10(self):
        try:
            self.connection = sqlite3.connect(dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT node_count, round_range, AVG(delta_byte) AS total_delta_byte "
                "FROM ( "
                "    SELECT node_count, "
                "           CASE "
                "               WHEN round BETWEEN 1 AND 10 THEN '10' "
                "               WHEN round BETWEEN 11 AND 20 THEN '20' "
                "               WHEN round BETWEEN 21 AND 30 THEN '30' "
                "               WHEN round BETWEEN 31 AND 40 THEN '40' "
                "           END AS round_range, "
                "           delta_byte "
                "    FROM delta_each_round_storage "
                "    WHERE round < 41 "
                ") AS subquery "
                "GROUP BY node_count, round_range "
                "ORDER BY node_count, round_range"
            )
            rounds = self.cursor.fetchall()
            return rounds
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []


def plot_barplot_node_count_convergence_round():
    demon_db = DemonDataDB()
    data_target_2_round = {'x': [], 'y': []}
    data_target_3_round = {'x': [], 'y': []}
    data_target_4_round = {'x': [], 'y': []}
    for group in demon_db.get_runs_grouped_by_node_target_avg():
        if group[1] == 2:
            data_target_2_round['x'].append(group[0])
            data_target_2_round['y'].append(group[2])
        if group[1] == 3:
            data_target_3_round['x'].append(group[0])
            data_target_3_round['y'].append(group[2])
        if group[1] == 4:
            data_target_4_round['x'].append(group[0])
            data_target_4_round['y'].append(group[2])

    bar_width = 0.25

    index = np.arange(len(data_target_4_round['x']))
    # Create the figure and axis objects
    fig, ax = plt.subplots()
    ax.bar(index, data_target_2_round['y'], bar_width, edgecolor='black', color="tomato", label='gossip_count = 2',
           hatch='..')
    ax.bar(index + bar_width, data_target_3_round['y'], bar_width, edgecolor='black', color="royalblue",
           label='gossip_count = 3', hatch='++')
    ax.bar(index + 2 * bar_width, data_target_4_round['y'], bar_width, edgecolor='black', color="mediumseagreen",
           label='gossip_count = 4', hatch='//')
    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(data_target_4_round['x'], fontsize=12)
    ax.set_ylabel('Gossip rounds', fontsize=16)
    ax.set_xlabel('# of nodes', fontsize=16)
    ax.legend(fontsize=14)
    plt.savefig('convergence_plot_demon_all_gc_barplot.png')
    plt.savefig('convergence_plot_demon_all_gc_barplot.pdf')
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)
    plt.legend(fontsize=14)
    plt.show()
    plt.clf()


def plot_rounds_number_of_known_nodes():
    demon_db = DemonDataDB()
    grouped_by_rounds_gc_2 = demon_db.get_messages_grouped_by_round_gc_2()
    grouped_by_rounds_gc_3 = demon_db.get_messages_grouped_by_round_gc_3()
    grouped_by_rounds_gc_4 = demon_db.get_messages_grouped_by_round_gc_4()
    round_data_to_plot_2 = {'x': [], 'y': []}
    round_data_to_plot_3 = {'x': [], 'y': []}
    round_data_to_plot_4 = {'x': [], 'y': []}
    for group in grouped_by_rounds_gc_2:
        r = group[0]
        nd_sum = group[1]
        round_data_to_plot_2['x'].append(r)
        round_data_to_plot_2['y'].append(nd_sum / 300)

    for group in grouped_by_rounds_gc_3:
        r = group[0]
        nd_sum = group[1]
        round_data_to_plot_3['x'].append(r)
        round_data_to_plot_3['y'].append(nd_sum / 300)

    for group in grouped_by_rounds_gc_4:
        r = group[0]
        nd_sum = group[1]
        round_data_to_plot_4['x'].append(r)
        round_data_to_plot_4['y'].append(nd_sum / 300)
    plt.plot(round_data_to_plot_2['x'][:-8], round_data_to_plot_2['y'][:-8], color="tomato", marker='^',
             label="gossip_count=2")
    plt.plot(round_data_to_plot_3['x'], round_data_to_plot_3['y'], color="royalblue", marker='x',
             label="gossip_count=3")
    plt.plot(round_data_to_plot_4['x'], round_data_to_plot_4['y'], color="mediumseagreen", marker='o',
             label="gossip_count=4")

    plt.xlabel('Rounds', fontsize=16)
    plt.ylabel('# of new nodes known', fontsize=16)
    plt.legend(fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.savefig('demon_nd_per_round_all_gc_nc_300.png')
    plt.savefig('demon_nd_per_round_all_gc_nc_300.pdf')
    plt.show()
    plt.clf()


def plot_fogmon_demon_messages_all_gc():
    target_count_2 = 2
    target_count_3 = 3
    target_count_4 = 4

    data_target_2 = {'x': [], 'y': []}
    data_target_3 = {'x': [], 'y': []}
    data_target_4 = {'x': [], 'y': []}
    demon_db = DemonDataDB()
    for group in demon_db.get_runs_grouped_by_node_target_avg():
        node_count = group[0]
        target_count = group[1]
        avg_convergence_message_count = group[3]/1000
        if target_count == target_count_2:
            data_target_2['x'].append(node_count)
            data_target_2['y'].append(avg_convergence_message_count)
        if target_count == target_count_3:
            data_target_3['x'].append(node_count)
            data_target_3['y'].append(avg_convergence_message_count)
        if target_count == target_count_4:
            data_target_4['x'].append(node_count)
            data_target_4['y'].append(avg_convergence_message_count)

    data_target_2_fog = {'x': [], 'y': []}
    data_target_3_fog = {'x': [], 'y': []}
    data_target_4_fog = {'x': [], 'y': []}
    for group in demon_db.get_fogmon_runs_grouped_by_node_target_avg():
        node_count = group[0]
        target_count = group[1]
        avg_convergence_message_count = group[3]/1000
        if target_count == target_count_2:
            data_target_2_fog['x'].append(node_count)
            data_target_2_fog['y'].append(avg_convergence_message_count)
        elif target_count == target_count_3:
            data_target_3_fog['x'].append(node_count)
            data_target_3_fog['y'].append(avg_convergence_message_count)
        elif target_count == target_count_4:
            data_target_4_fog['x'].append(node_count)
            data_target_4_fog['y'].append(avg_convergence_message_count)
    # plt.xlabel('# of nodes', fontsize=16)
    # plt.ylabel('# of messages', fontsize=16)
    # plt.title('Convergence Messages with different Gossip Count')
    # plt.legend(fontsize=14)
    # plt.xticks(fontsize=12)
    # plt.yticks(fontsize=12)
    rcParams.update({'figure.autolayout': True})
    plt.plot(data_target_2['x'], data_target_2['y'], color="tomato", marker='^', label="Demon")
    plt.plot(data_target_2_fog['x'], data_target_2_fog['y'], color="royalblue", marker='x', label="Fog")
    plt.xlabel('# of nodes', fontsize=20)
    plt.ylabel('# of message (K)', fontsize=20)
    plt.legend(fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.grid(True)
    plt.savefig('convergence_plot_demon_fogmon_2_gc_messages.png')
    plt.savefig('convergence_plot_demon_fogmon_2_gc_messages.pdf')
    plt.show()
    plt.clf()

    plt.plot(data_target_3['x'], data_target_3['y'], color="tomato", marker='^', label="Demon")
    plt.plot(data_target_3_fog['x'], data_target_3_fog['y'], color="royalblue", marker='x', label="Fog")
    plt.xlabel('# of nodes', fontsize=20)
    plt.ylabel('# of message (k)', fontsize=20)
    plt.legend(fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.grid(True)
    plt.savefig('convergence_plot_demon_fogmon_3_gc_messages.png')
    plt.savefig('convergence_plot_demon_fogmon_3_gc_messages.pdf')
    plt.show()
    plt.clf()

    plt.plot(data_target_4['x'], data_target_4['y'], color="tomato", marker='^', label="Demon")
    plt.plot(data_target_4_fog['x'], data_target_4_fog['y'], color="royalblue", marker='x', label="Fog")
    plt.xlabel('# of nodes', fontsize=20)
    plt.ylabel('# of message (K)', fontsize=20)
    plt.legend(fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.grid(True)
    plt.savefig('convergence_plot_demon_fogmon_4_gc_messages.png')
    plt.savefig('convergence_plot_demon_fogmon_4_gc_messages.pdf')
    plt.show()
    plt.clf()


def plot_all_gr_avg_messages():
    demon_db = DemonDataDB()
    # TODO: change DB
    # demon_runs_gr = demon_db_gr.get_runs_grouped_by_node_rate()

    gossip_rate_2 = 1
    gossip_rate_4 = 5
    gossip_rate_6 = 10
    gossip_rate_15 = 15
    gossip_rate_8 = 20
    data_rate_2 = {'x': [], 'y': []}
    data_rate_4 = {'x': [], 'y': []}
    data_rate_6 = {'x': [], 'y': []}
    data_rate_8 = {'x': [], 'y': []}
    data_rate_15 = {'x': [], 'y': []}

    for group in demon_db.get_runs_grouped_by_node_rate():
        node_count = group[0]
        gossip_rate = group[1]
        avg_convergence_message_count = group[3]/1000

        # Check if the target count matches the one to plot
        if gossip_rate == gossip_rate_2:
            data_rate_2['x'].append(node_count)
            data_rate_2['y'].append(avg_convergence_message_count)
        elif gossip_rate == gossip_rate_4:
            data_rate_4['x'].append(node_count)
            data_rate_4['y'].append(avg_convergence_message_count)
        elif gossip_rate == gossip_rate_6:
            data_rate_6['x'].append(node_count)
            data_rate_6['y'].append(avg_convergence_message_count)
        elif gossip_rate == gossip_rate_8:
            data_rate_8['x'].append(node_count)
            data_rate_8['y'].append(avg_convergence_message_count)
        elif gossip_rate == gossip_rate_15:
            data_rate_15['x'].append(node_count)
            data_rate_15['y'].append(avg_convergence_message_count)

    plt.plot(data_rate_2['x'], data_rate_2['y'], color="tomato", marker='^', label=f'gossip_rate = 1')
    plt.plot(data_rate_4['x'], data_rate_4['y'], color="royalblue", marker='x', label=f'gossip_rate = 5')
    plt.plot(data_rate_6['x'], data_rate_6['y'], color="mediumseagreen", marker='o',
             label=f'gossip_rate = 10')
    plt.plot(data_rate_15['x'], data_rate_15['y'], color="darkorchid", marker='*', label=f'gossip_rate = 15')

    plt.plot(data_rate_8['x'], data_rate_8['y'], color="goldenrod", marker='2', label=f'gossip_rate = 20')
    plt.xlabel('# of nodes', fontsize=16)
    plt.ylabel('# of messages (K)', fontsize=16)
    # plt.title('Convergence Messages with different Gossip Count')
    plt.legend(fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.savefig('convergence_plot_demon_all_gr_message.png')
    plt.savefig('convergence_plot_demon_all_gr_message.pdf')
    plt.show()
    plt.clf()


def plot_all_gc_avg_messages():
    demon_db = DemonDataDB()

    gossip_count_2 = 2
    gossip_count_3 = 3
    gossip_count_4 = 4
    data_target_2 = {'x': [], 'y': []}
    data_target_3 = {'x': [], 'y': []}
    data_target_4 = {'x': [], 'y': []}

    for group in demon_db.get_runs_grouped_by_node_target_avg():
        node_count = group[0]
        target_count = group[1]
        avg_convergence_message_count = group[3]/1000
        if target_count == gossip_count_2:
            data_target_2['x'].append(node_count)
            data_target_2['y'].append(avg_convergence_message_count)
        elif target_count == gossip_count_3:
            data_target_3['x'].append(node_count)
            data_target_3['y'].append(avg_convergence_message_count)
        elif target_count == gossip_count_4:
            data_target_4['x'].append(node_count)
            data_target_4['y'].append(avg_convergence_message_count)
    plt.plot(data_target_2['x'], data_target_2['y'], color="tomato", marker='^', label=f'gossip_count = 2')
    plt.plot(data_target_3['x'], data_target_3['y'], color="royalblue", marker='x', label=f'gossip_count = 3')
    plt.plot(data_target_4['x'], data_target_4['y'], color="mediumseagreen", marker='o',
             label=f'gossip_count = 4')
    plt.xlabel('# of nodes', fontsize=16)
    plt.ylabel('# of messages (K)', fontsize=16)
    # plt.title('Convergence Messages with different Gossip Count')
    plt.legend(fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.savefig('convergence_plot_demon_all_gc_message.png')
    plt.savefig('convergence_plot_demon_all_gc_message.pdf')
    plt.show()
    plt.clf()


def plot_aoi():
    demon_db = DemonDataDB()
    aoi_2 = {'x': [], 'y': []}
    aoi_3 = {'x': [], 'y': []}
    aoi_4 = {'x': [], 'y': []}
    aoi_data = demon_db.get_sum_aoi_group_by_node_timer()
    for group in aoi_data:
        if group[1] == 2:
            aoi_2['x'].append(group[2])
            aoi_2['y'].append(group[3])
        elif group[1] == 3:
            aoi_3['x'].append(group[2])
            aoi_3['y'].append(group[3])
        elif group[1] == 4:
            aoi_4['x'].append(group[2])
            aoi_4['y'].append(group[3])
    # avg(aoi)
    cumulative_y_2 = np.cumsum(aoi_2['y'])

    cumulative_y_3 = np.cumsum(aoi_3['y'])
    cumulative_y_4 = np.cumsum(aoi_4['y'])
    # plt.plot(aoi_2['x'], cumulative_y_2, color="tomato", marker='^', label=f'gossip_count = 2')
    plt.plot(aoi_3['x'], cumulative_y_3, color="royalblue", marker='x', label=f'aoi')
    # plt.plot(aoi_4['x'], cumulative_y_4, color="mediumseagreen", marker='o', label=f'gossip_count = 4')
    plt.ylabel('Average AoI per node', fontsize=16)
    plt.xlabel('Time [s]', fontsize=16)
    plt.legend(fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    # plt.yscale('log')# Show the plot
    plt.grid(True)
    plt.savefig('aoi_gc_3.png')
    plt.savefig('aoi_gc_3.pdf')
    plt.show()
    plt.clf()


def plot_pushed_data_every_10th_round():
    demonDB = DemonDataDB()
    delta_storage = demonDB.get_delta_byte_grouped_by_node_count_and_round_10()
    delta_storage_50 = {'x': [], 'y': []}
    delta_storage_100 = {'x': [], 'y': []}
    delta_storage_150 = {'x': [], 'y': []}
    delta_storage_200 = {'x': [], 'y': []}
    delta_storage_250 = {'x': [], 'y': []}
    delta_storage_300 = {'x': [], 'y': []}
    delta_storage_50['x'].append(0)
    delta_storage_50['y'].append(0)
    delta_storage_100['x'].append(0)
    delta_storage_100['y'].append(0)
    delta_storage_150['x'].append(0)
    delta_storage_150['y'].append(0)
    delta_storage_200['x'].append(0)
    delta_storage_200['y'].append(0)
    delta_storage_250['x'].append(0)
    delta_storage_250['y'].append(0)
    delta_storage_300['x'].append(0)
    delta_storage_300['y'].append(0)

    for group in delta_storage:
        node_count = group[0]
        round_ = group[1]
        delta_kilo_byte = group[2] / 1024
        if node_count == 50:
            delta_storage_50['x'].append(round_)
            delta_storage_50['y'].append(delta_kilo_byte)
        elif node_count == 100:
            delta_storage_100['x'].append(round_)
            delta_storage_100['y'].append(delta_kilo_byte)
        elif node_count == 150:
            delta_storage_150['x'].append(round_)
            delta_storage_150['y'].append(delta_kilo_byte)
        elif node_count == 200:
            delta_storage_200['x'].append(round_)
            delta_storage_200['y'].append(delta_kilo_byte)
        elif node_count == 250:
            delta_storage_250['x'].append(round_)
            delta_storage_250['y'].append(delta_kilo_byte)
        elif node_count == 300:
            delta_storage_300['x'].append(round_)
            delta_storage_300['y'].append(delta_kilo_byte)

    # plt_1 = plt.figure(figsize=(10, 7.5))
    plt.plot(delta_storage_50['x'], delta_storage_50['y'], color="tomato", marker='^', label=f'n = 50')
    plt.plot(delta_storage_100['x'], delta_storage_100['y'], color="royalblue", marker='x', label=f'n = 100')
    plt.plot(delta_storage_150['x'], delta_storage_150['y'], color="mediumseagreen", marker='o',
             label=f'n = 150')
    plt.plot(delta_storage_200['x'], delta_storage_200['y'], color="goldenrod", marker='*', label=f'n = 200')
    plt.plot(delta_storage_250['x'], delta_storage_250['y'], color="indigo", marker='P', label=f'n = 250')
    plt.plot(delta_storage_300['x'], delta_storage_300['y'], color="dimgray", marker='>', label=f'n = 300')

    plt.xlabel('Rounds', fontsize=20)
    plt.ylabel('Storage per node [KB]', fontsize=20)
    # plt.title('Convergence Messages with different Gossip Count')
    #put legend outside of plot, on top
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.22),
          ncol=3, fontsize=16, frameon=False)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    # Show the plot
    plt.grid(True)
    plt.savefig('push_storage_per_node.png', bbox_inches='tight')
    plt.savefig('push_storage_per_node.pdf', bbox_inches='tight')
    plt.show()
    plt.clf()


def plot_new_data_per_round_incl_after_conv():
    # Storage per round till/after convergence
    demon_db = DemonDataDB()
    grouped_by_rounds_gc_2_after = demon_db.get_fresh_data_grouped_by_round_gc_2()
    grouped_by_rounds_gc_3_after = demon_db.get_fresh_data_grouped_by_round_gc_3()
    grouped_by_rounds_gc_4_after = demon_db.get_fresh_data_grouped_by_round_gc_4()
    fd_by_rounds_gc_2_after = {'x': [], 'y': []}
    fd_by_rounds_gc_3_after = {'x': [], 'y': []}
    fd_by_rounds_gc_4_after = {'x': [], 'y': []}
    for group in grouped_by_rounds_gc_2_after:
        r = group[0]
        fd = group[1]
        fd_by_rounds_gc_2_after['x'].append(r)
        fd_by_rounds_gc_2_after['y'].append(fd / (300))
    for group in grouped_by_rounds_gc_3_after:
        r = group[0]
        fd = group[1]
        fd_by_rounds_gc_3_after['x'].append(r)
        fd_by_rounds_gc_3_after['y'].append(fd / (300))
    for group in grouped_by_rounds_gc_4_after:
        r = group[0]
        fd = group[1]
        fd_by_rounds_gc_4_after['x'].append(r)
        fd_by_rounds_gc_4_after['y'].append(fd / (300))
    # convergence points:
    # 9 11 12 13 15 16

    plt.plot(fd_by_rounds_gc_2_after['x'], fd_by_rounds_gc_2_after['y'], color="tomato", marker='^',
             label="gossip_count=2", markersize=4)  # 29 30
    plt.plot(fd_by_rounds_gc_2_after['x'][30], fd_by_rounds_gc_2_after['y'][30], marker="D", color='black',
             markersize=6)
    plt.plot(fd_by_rounds_gc_3_after['x'], fd_by_rounds_gc_3_after['y'], color="royalblue", marker='x',
             label="gossip_count=3", markersize=4)  # 20 22
    plt.plot(fd_by_rounds_gc_3_after['x'][21], fd_by_rounds_gc_3_after['y'][21], marker="D", color='black',
             markersize=6)
    plt.plot(fd_by_rounds_gc_4_after['x'], fd_by_rounds_gc_4_after['y'], color="mediumseagreen", marker='o',
             label="gossip_count=4", markersize=4)  # 19
    plt.plot(fd_by_rounds_gc_4_after['x'][18], fd_by_rounds_gc_4_after['y'][18], marker="D", color='black',
             label="Convergence", markersize=6)

    # plt.plot(data_target_4['x'], data_target_4['y'], 'mo-', label=f'DEMon')

    plt.xlabel('Rounds', fontsize=16)
    plt.ylabel('# of new data per node', fontsize=16)
    #plt.title('Convergence Messages with different Gossip Count')
    plt.legend(fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Show the plot
    plt.grid(True)
    plt.savefig('after_convergence_plot_demon_fd_per_node_nc_300.png')
    plt.savefig('after_convergence_plot_demon_fd_per_node_nc_300.pdf')
    plt.show()
    plt.clf()


def plot_storage_per_node_after_conv():
    demonDB = DemonDataDB()
    values = [demonDB.get_delta_byte_grouped_by_node_count_and_round_50()[0][0] / (50 * 1024),
              demonDB.get_delta_byte_grouped_by_node_count_and_round_100()[0][0] / (100 * 1024),
              demonDB.get_delta_byte_grouped_by_node_count_and_round_150()[0][0] / (150 * 1024),
              demonDB.get_delta_byte_grouped_by_node_count_and_round_200()[0][0] / (200 * 1024),
              demonDB.get_delta_byte_grouped_by_node_count_and_round_250()[0][0] / (250 * 1024),
              demonDB.get_delta_byte_grouped_by_node_count_and_round_300()[0][0] / (300 * 1024)]
    # print(values[5])

    colors = ['tomato', 'royalblue', 'mediumseagreen', 'goldenrod', 'indigo', 'dimgray']
    hatches = ['o', '+', 'x', '\\', '*', '.']
    categories = ['50', '100', '150', '200', '250', '300']
    for i in range(len(categories)):
        plt.bar(categories[i], values[i], hatch=hatches[i], edgecolor='black', color=colors[i],
                label='node_count = {}'.format(categories[i]))
    plt.yscale('log')
    plt.xlabel('System size', fontsize=18)
    plt.ylabel('Storage per node [KB]', fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    # plt.legend()
    plt.savefig('storage_convergence_pernode.png', bbox_inches='tight')
    plt.savefig('storage_convergence_pernode.pdf', bbox_inches='tight')
    plt.show()
    plt.clf()


def plot_bandwidth_per_round():
    # Bandwidth per round plot
    demon_db = DemonDataDB()
    grouped_by_rounds_gc_2_bytes = demon_db.get_byte_grouped_by_round_gc_2()
    grouped_by_rounds_gc_3_bytes = demon_db.get_byte_grouped_by_round_gc_3()
    grouped_by_rounds_gc_4_bytes = demon_db.get_byte_grouped_by_round_gc_4()
    round_data_to_plot_2_bytes = {'x': [], 'y': []}
    round_data_to_plot_3_bytes = {'x': [], 'y': []}
    round_data_to_plot_4_bytes = {'x': [], 'y': []}
    for group in grouped_by_rounds_gc_2_bytes:
        r = group[0]
        byte_sum = group[1]
        round_data_to_plot_2_bytes['x'].append(r)
        round_data_to_plot_2_bytes['y'].append(byte_sum / (1048576 * 300 * 3))

    for group in grouped_by_rounds_gc_3_bytes:
        r = group[0]
        byte_sum = group[1]
        round_data_to_plot_3_bytes['x'].append(r)
        round_data_to_plot_3_bytes['y'].append(byte_sum / (1048576 * 300 * 3))

    for group in grouped_by_rounds_gc_4_bytes:
        r = group[0]
        byte_sum = group[1]
        round_data_to_plot_4_bytes['x'].append(r)
        round_data_to_plot_4_bytes['y'].append(byte_sum / (1048576 * 300 * 3))

    plt.plot(round_data_to_plot_2_bytes['x'], round_data_to_plot_2_bytes['y'], color="tomato", marker='^',
             label="gc=2")
    plt.plot(round_data_to_plot_3_bytes['x'], round_data_to_plot_3_bytes['y'], color="royalblue", marker='x',
             label="gc=3")
    plt.plot(round_data_to_plot_4_bytes['x'], round_data_to_plot_4_bytes['y'], color="mediumseagreen", marker='o',
             label="gc=4")
    plt.xlabel('Rounds', fontsize=18)
    plt.ylabel('Node bandwidth [MB]', fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    # plt.title('Convergence Messages with different Gossip Count')
    plt.legend(fontsize=18, loc='upper right')

    # Show the plot
    plt.grid(True)
    plt.savefig('convergence_plot_demon_bandwidth_per_node_nc_300.png', bbox_inches='tight')
    plt.savefig('convergence_plot_demon_bandwidth_per_node_nc_300.pdf', bbox_inches='tight')
    plt.show()
    plt.clf()


def plot_3d_time_gr_gc():
    demon_db = DemonDataDB()
    gr_gc_data = demon_db.get_runs_grouped_by_node_rate_count()
    # there are 3 different target counts 2,3,4 and 4 different gossip rates 2,4,6,8
    # target count is stored in index 2 and gossip rate in index 1
    # goal is to get the convergence time for each target count and gossip rate
    # data example is (70, 6, 3, 116.26352826754233), where 70 is the node count, 6 is the gossip rate, 3 is the target count and 116.26352826754233 is the convergence time
    # the data is ordered by node count, gossip rate and target count, now permutate all combinations of gossip rate and target count
    gc_2_gr_2 = {'x': [], 'y': []}
    gc_2_gr_4 = {'x': [], 'y': []}
    gc_2_gr_6 = {'x': [], 'y': []}
    gc_2_gr_8 = {'x': [], 'y': []}
    gc_3_gr_2 = {'x': [], 'y': []}
    gc_3_gr_4 = {'x': [], 'y': []}
    gc_3_gr_6 = {'x': [], 'y': []}
    gc_3_gr_8 = {'x': [], 'y': []}
    gc_4_gr_2 = {'x': [], 'y': []}
    gc_4_gr_4 = {'x': [], 'y': []}
    gc_4_gr_6 = {'x': [], 'y': []}
    gc_4_gr_8 = {'x': [], 'y': []}

    nc_10 = {'x': [], 'y': [], 'z': []}
    nc_300 = {'x': [], 'y': [], 'z': []}

    for group in gr_gc_data:

        if group[0] == 10:
            # gr
            nc_10['x'].append(group[1])
            nc_10['y'].append(group[2])
            nc_10['z'].append(group[3])
        if group[0] == 300:  # gr
            nc_300['x'].append(group[1])
            nc_300['y'].append(group[2])
            nc_300['z'].append(group[3])
        if group[2] == 2:
            if group[1] == 2:
                gc_2_gr_2['x'].append(group[1])
                gc_2_gr_2['y'].append(group[3])
            if group[1] == 4:
                gc_2_gr_4['x'].append(group[0])
                gc_2_gr_4['y'].append(group[3])
            if group[1] == 6:
                gc_2_gr_6['x'].append(group[0])
                gc_2_gr_6['y'].append(group[3])
            if group[1] == 8:
                gc_2_gr_8['x'].append(group[0])
                gc_2_gr_8['y'].append(group[3])

        if group[2] == 3:
            if group[1] == 2:
                gc_3_gr_2['x'].append(group[0])
                gc_3_gr_2['y'].append(group[3])
            if group[1] == 4:
                gc_3_gr_4['x'].append(group[0])
                gc_3_gr_4['y'].append(group[3])
            if group[1] == 6:
                gc_3_gr_6['x'].append(group[0])
                gc_3_gr_6['y'].append(group[3])
            if group[1] == 8:
                gc_3_gr_8['x'].append(group[0])
                gc_3_gr_8['y'].append(group[3])

        if group[2] == 4:
            if group[1] == 2:
                gc_4_gr_2['x'].append(group[0])
                gc_4_gr_2['y'].append(group[3])
            if group[1] == 4:
                gc_4_gr_4['x'].append(group[0])
                gc_4_gr_4['y'].append(group[3])
            if group[1] == 6:
                gc_4_gr_6['x'].append(group[0])
                gc_4_gr_6['y'].append(group[3])
            if group[1] == 8:
                gc_4_gr_8['x'].append(group[0])
                gc_4_gr_8['y'].append(group[3])

    # append all data to one list
    gc_gr_data = [gc_2_gr_2, gc_2_gr_4, gc_2_gr_6, gc_2_gr_8, gc_3_gr_2, gc_3_gr_4, gc_3_gr_6, gc_3_gr_8, gc_4_gr_2,
                  gc_4_gr_4, gc_4_gr_6, gc_4_gr_8]

    x = nc_300['x']
    y = nc_300['y']
    z = nc_300['z']

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    bar_width = 2.5
    bar_length = 0.5

    start = min(z) - 100
    x_centered = np.array(x) - bar_width / 2
    y_centered = np.array(y) - bar_length / 2
    z_scaled = np.array(z) - start

    # COLORMAP:
    colormap = cm.turbo  # You can choose a different colormap here
    z_normalized = np.array(z_scaled) / max(z_scaled)
    colors = [colormap(z) for z in z_normalized]
    ax.bar3d(x_centered, y_centered, start, bar_width, bar_length, z_scaled, shade=True, color=colors)

    ax.set_xlabel('gossip_rate')
    ax.set_ylabel('gossip_count')
    ax.set_zlabel('Time [s]')
    ax.set_xticks(x)
    ax.set_xticklabels(x)
    ax.set_yticks(y)
    ax.set_yticklabels(y)
    ax.invert_yaxis()
    ax.invert_xaxis()
    ax.set_zlim(start, max(z))

    plt.show()
    fig.savefig("time3dplot.png")
    fig.savefig('time3dplot.pdf')
    plt.clf()

if __name__ == '__main__':
    plot_barplot_node_count_convergence_round()
    plot_rounds_number_of_known_nodes()
    plot_fogmon_demon_messages_all_gc()
    plot_all_gr_avg_messages()
    plot_all_gc_avg_messages()
    plot_aoi()
    plot_new_data_per_round_incl_after_conv()
    plot_pushed_data_every_10th_round()
    plot_storage_per_node_after_conv()
    plot_bandwidth_per_round()
    plot_3d_time_gr_gc()



