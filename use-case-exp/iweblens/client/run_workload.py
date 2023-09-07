import yaml
import subprocess
import sys

def main():
    with open("hosts.yml") as f:
        hosts = yaml.load(f, Loader=yaml.FullLoader)
    try:
        processes = []
        for h in hosts:
            process = subprocess.Popen(["locust", "-f", "locust_file.py", "-H", f"{h['endpoint']}", "-u", f"{h['users']}", "-r", f"{h['rate']}", "--images-folder", "inputfolder", "--headless"])
            processes.append(process)
        print("Press Ctrl+C to stop Locust load test and exit...")
        while True:
            pass
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
        sys.exit()

if __name__ == '__main__':
    main()