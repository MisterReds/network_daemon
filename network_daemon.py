import subprocess
import time
import configparser
import daemon
import signal
import logging

logging.basicConfig(filename='network_daemon.log', level=logging.INFO)

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode()

def configure_interface(interface, address, netmask, gateway):
    run_command(f"ip link set {interface} up")
    run_command(f"ip addr add {address}/{netmask} dev {interface}")
    run_command(f"ip route add default via {gateway}")

def read_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config

def run_daemon():
    while True:
        config = read_config('network.conf')
        for section in config.sections():
            if config[section]['iface'] == 'inet':
                address = config[section]['address']
                netmask = config[section]['netmask']
                gateway = config[section]['gateway']
                configure_interface(section, address, netmask, gateway)
                logging.info(f"Configured {section} with {address}")
        time.sleep(10)

def handle_signal(signum, frame):
    logging.info("Daemon stopped.")
    exit(0)

signal.signal(signal.SIGTERM, handle_signal)

with daemon.DaemonContext():
    run_daemon()
