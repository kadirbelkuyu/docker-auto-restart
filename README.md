# Docker Container Monitor

Docker Container Monitor is a Python script that monitors the status of Docker containers and restarts them if necessary. It uses the Docker API to get information about running containers, and compares this information with the settings defined in a configuration file (`config.yml`). The script can be used to monitor the CPU and memory usage of Docker containers, and restart them if they exceed a certain threshold.

## Installation

To use Docker Container Monitor, you must have Docker installed on your system. You can install Docker by following the instructions on the [Docker website](https://docs.docker.com/get-docker/).

To install the Python dependencies required by Docker Container Monitor, run the following command:


## Configuration

The configuration file for Docker Container Monitor is `config.yml`. This file contains the settings for each Docker container that you want to monitor. For each container, you can specify the following settings:

- `name`: The name of the container
- `priority`: The priority of the container. Containers with a higher priority will be restarted before containers with a lower priority.
- `wait_time`: The time (in seconds) to wait before restarting a container. This can be useful to avoid restarting a container that is in the process of shutting down.
- `cpu_threshold`: The CPU usage threshold (as a percentage) at which the container should be restarted.
- `memory_threshold`: The memory usage threshold (as a percentage) at which the container should be restarted.

## Usage

To use Docker Container Monitor, simply run the following command:


The script will run indefinitely, checking the status of Docker containers at regular intervals (default: 10 seconds).

## License

Docker Container Monitor is licensed under the [MIT License](https://opensource.org/licenses/MIT).
