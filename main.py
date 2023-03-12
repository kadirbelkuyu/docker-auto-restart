import docker
import logging
import time
import yaml
import psutil
import os

def check_containers(client, config):
    running_containers = client.containers.list()
    for container_config in config['containers']:
        container_name = container_config['name']
        container_priority = container_config.get('priority', 0)
        container_wait_time = container_config.get('wait_time', 0)
        container = None
        for running_container in running_containers:
            if running_container.name == container_name:
                container = running_container
                break
        if container is None:
            logging.warning(f"Container {container_name} not found")
            continue
        if container.status != "running":
            logging.error(f"Container {container_name} is not running. Status: {container.status}")
            time.sleep(container_wait_time)
            restart_container(container)
        cpu_percent = container.stats(stream=False)['cpu_stats']['cpu_usage']['total_usage'] / psutil.cpu_count() * 100
        memory_percent = container.stats(stream=False)['memory_stats']['usage'] / container.stats(stream=False)['memory_stats']['limit'] * 100
        logging.info(f"Container {container_name} - CPU Usage: {cpu_percent:.2f}%, Memory Usage: {memory_percent:.2f}%")
        if cpu_percent >= container_config.get('cpu_threshold', 0) or memory_percent >= container_config.get('memory_threshold', 0):
            logging.warning(f"Container {container_name} is using too many resources. Restarting container")
            restart_container(container)
    running_containers.sort(key=lambda x: x.labels.get('priority', 0), reverse=True)
    for container in running_containers:
        if container.status == "running":
            continue
        if container not in [config_container['name'] for config_container in config['containers']]:
            logging.warning(f"Unknown container {container.name} is not running. Status: {container.status}")
            continue
        logging.warning(f"Starting stopped container {container.name}")
        container.start()

def restart_container(container):
    logging.info(f"Restarting container {container.name}")
    container.restart()

def load_config(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config

def get_file_paths():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_paths = {
        'main': os.path.join(current_dir, 'main.py'),
        'config': os.path.join(current_dir, 'config.yml')
    }
    return file_paths

if __name__ == "__main__":
    logging.basicConfig(filename="container_monitor.log", level=logging.INFO)
    client = docker.from_env()
    config_file_paths = get_file_paths()
    config = load_config(config_file_paths['config'])
    while True:
        check_containers(client, config)
        time.sleep(10)
