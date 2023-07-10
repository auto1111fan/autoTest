#!/usr/bin/env python3
import json
import os
import re
import subprocess


def get_cmd_output(command):
    try:
        return subprocess.check_output(command, shell=True).decode()
    except subprocess.CalledProcessError:
        return ""

def nic_info():
    nic_info_raw = get_cmd_output("ip -j link show")
    nic_data = json.loads(nic_info_raw)

    for nic in nic_data:
        print(f"\n== NIC: {nic['ifname']} ==")
        print(f"MAC Address: {nic['address']}")

        ip_info_raw = get_cmd_output(f"ip -j addr show {nic['ifname']}")
        ip_data = json.loads(ip_info_raw)
        for addr_info in ip_data[0]['addr_info']:
            print(f"IP Address: {addr_info['local']}")
            print(f"Subnet: {addr_info['prefixlen']}")

        open_ports_raw = get_cmd_output(f"ss -tulwn | grep {nic['ifname']}")
        open_ports = re.findall(r':(\d+)', open_ports_raw)
        print(f"Open ports: {', '.join(open_ports)}")

def cpu_info():
    cpu_info_raw = get_cmd_output("lscpu")
    print("\n== CPU Info ==")
    print(cpu_info_raw)


def ram_info():
    ram_info_raw = get_cmd_output("free -h")
    print("\n== RAM Info ==")
    print(ram_info_raw)


def gpu_info():
    gpu_info_raw = get_cmd_output("lspci | grep VGA")
    print("\n== GPU Info ==")
    print(gpu_info_raw)


def storage_info():
    df_info_raw = get_cmd_output("df -h")
    lsblk_info_raw = get_cmd_output("lsblk")
    print("\n== Storage Info ==")
    print(df_info_raw)
    print("\n=== Physical Storage ===")
    print(lsblk_info_raw)


def os_info():
    os_info_raw = get_cmd_output("cat /etc/os-release")
    print("\n== OS Info ==")
    print(os_info_raw)


def hypervisor_info():
    hypervisor_check = get_cmd_output("systemd-detect-virt")
    if hypervisor_check.strip() != "none":
        print("\n== Hypervisor Info ==")
        print("Hypervisor: " + hypervisor_check)
        dmidecode_info_raw = get_cmd_output("sudo dmidecode -s system-product-name")
        print("More details: " + dmidecode_info_raw)
    else:
        print("\n== Hypervisor Info ==")
        print("No hypervisor detected.")


def user_info():
    username = get_cmd_output("whoami")
    user_details = get_cmd_output(f"id {username}")
    print("\n== User Info ==")
    print("Current user: ", username)
    print(user_details)


def main():
    if os.name == "nt":
        print("This extension is only supported on Linux.")
        return
    user_info()
    nic_info()
    cpu_info()
    ram_info()
    gpu_info()
    storage_info()
    os_info()
    hypervisor_info()


def preload(parser):
    main()
