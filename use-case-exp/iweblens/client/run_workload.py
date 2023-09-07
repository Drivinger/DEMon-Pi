import yaml
import subprocess
import sys

def main():
    with open("hosts.yaml") as f:
        hosts = yaml.load(f, Loader=yaml.FullLoader)
    try:
        processes = []
        for h in hosts:
            process = subprocess.Popen(["locust", "-f", "locust_file.py", "-h", f"{h['endpoint']}", "-u", f"{h['users']}", "-r", f"{h['rate']}", "--headless"])
            processes.append(process)
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
        sys.exit()

if __name__ == '__main__':
    main()