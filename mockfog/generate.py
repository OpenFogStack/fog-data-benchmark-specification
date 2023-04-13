#!/usr/bin/env python3
#
# Copyright (c) Tobias Pfandzelter. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

import typing
import json

# AWS settings
ec2_region = "eu-central-1"
ssh_key_name = "mockfog"
agent_port = 3100
ami = "ami-0aa9794817db273c1"

#
output_file = "infrastructure.jsonc"

# parameters
Nsensors = 300
CPU_s = 0.25  # cores
Mem_s = 256  # MB
Disk_s = 4  # GB

CPU_gw = 4
Mem_gw = 4
Disk_gw = 256

CPU_onprem = 0.5
Mem_onprem = 48000
Disk_onprem = 2000

Ncloud = 3
CPU_cloud = 48
Mem_cloud = 96000
Disk_cloud = 4000

dist_onprem_to_cloud = 4208010.0  # meters
connection_onprem_to_cloud = "fiber"

connection_cloud_to_cloud = "fiber10Gbps"

volcanoes = {
    "haleakala": {
        "dist_to_onprem": 163969.0,  # meters
        "mean_dist_to_sensors": 8211.3,  # meters
        "std_dist_to_sensors": 2793.4,  # meters
        "connection_to_sensors": "lorawan",
        "connection_to_onprem": "fiber",
    },
    "kilauea": {
        "dist_to_onprem": 40085.5,
        "mean_dist_to_sensors": 8814.9,
        "std_dist_to_sensors": 3626.8,
        "connection_to_sensors": "lorawan",
        "connection_to_onprem": "fiber",
    },
    "hualalai": {
        "dist_to_onprem": 83273.0,
        "mean_dist_to_sensors": 4389.5,
        "std_dist_to_sensors": 2229.8,
        "connection_to_sensors": "lorawan",
        "connection_to_onprem": "fiber",
    },
    "mauna_kea": {
        "dist_to_onprem": 41824.0,
        "mean_dist_to_sensors": 5151.0,
        "std_dist_to_sensors": 2393.6,
        "connection_to_sensors": "lorawan",
        "connection_to_onprem": "lte-m",
    },
    "mauna_loa": {
        "dist_to_onprem": 61247.0,
        "mean_dist_to_sensors": 7290.0,
        "std_dist_to_sensors": 2514.2,
        "connection_to_sensors": "lorawan",
        "connection_to_onprem": "lte-m",
    },
    "kamaehuakanaloa": {
        "dist_to_onprem": 97580.2,
        "mean_dist_to_sensors": 3372.7,
        "std_dist_to_sensors": 1633.6,
        "connection_to_sensors": "lorawan",
        "connection_to_onprem": "lte-m",
    },
}

connection_properties = {
    "lte-m": {
        "delay_per_km": 0.0170263789,  # ms
        "delay_per_km_std": 0.00510791367,  # ms
        "bandwidth": 1,  # Mbps
        "loss": 1,  # %
        "corruption": 1,  # %
        "reordering": 1,  # %
        "duplication": 1,  # %
    },
    "lorawan": {
        "delay_per_km": 0.02128297362,  # ms
        "delay_per_km_std": 0.01064148681,  # ms
        "bandwidth": 0.022,  # Mbps
        "loss": 5,  # %
        "corruption": 5,  # %
        "reordering": 5,  # %
        "duplication": 5,  # %
    },
    "fiber": {
        "delay_per_km": 0.008513189448,  # ms
        "delay_per_km_std": 0.0008513189448,  # ms
        "bandwidth": 1000,  # Mbps
        "loss": 0.1,  # %
        "corruption": 0.1,  # %
        "reordering": 0.1,  # %
        "duplication": 0.1,  # %
    },
    "fiber10Gbps": {
        "delay_per_km": 0.008513189448,  # ms
        "delay_per_km_std": 0.0008513189448,  # ms
        "bandwidth": 10000,  # Mbps
        "loss": 0.1,  # %
        "corruption": 0.1,  # %
        "reordering": 0.1,  # %
        "duplication": 0.1,  # %
    },
}

# available AWS machines
# https://aws.amazon.com/ec2/instance-types/
machine_types: typing.Dict[str, typing.Dict[str, typing.Union[float]]] = {
    "t3.nano": {
        "cpu": 2,
        "mem": 512,
    },
    "t3.micro": {
        "cpu": 2,
        "mem": 1000,
    },
    "t3.small": {
        "cpu": 2,
        "mem": 2000,
    },
    "t3.medium": {
        "cpu": 2,
        "mem": 4000,
    },
    "t3.large": {
        "cpu": 2,
        "mem": 8000,
    },
    "t3.xlarge": {
        "cpu": 4,
        "mem": 16000,
    },
    "t3.2xlarge": {
        "cpu": 8,
        "mem": 32000,
    },
    "m5.4xlarge": {
        "cpu": 16,
        "mem": 64000,
    },
    "m5.8xlarge": {
        "cpu": 32,
        "mem": 128000,
    },
    "m5.12xlarge": {
        "cpu": 48,
        "mem": 192000,
    },
    "m5.16xlarge": {
        "cpu": 64,
        "mem": 256000,
    },
    "m5.24xlarge": {
        "cpu": 96,
        "mem": 384000,
    },
}

# just in case we made a mistake: sort machine types by cpu size
machine_types = {
    k: v for k, v in sorted(machine_types.items(), key=lambda item: item[1]["cpu"])
}


def get_machine_type(cpu_need: float, mem_need: float) -> str:
    """Get machine type that fits the needs"""
    for machine_type, machine_properties in machine_types.items():
        if (
            machine_properties["cpu"] >= cpu_need
            and machine_properties["mem"] >= mem_need
        ):
            return machine_type
    raise Exception(
        f"No suitable machine type found for {cpu_need} cpu and {mem_need} mem"
    )


def convert_rate(rate: float) -> str:
    """Convert rate to string"""
    if rate < 1:
        return f"{rate * 1000}kbps"
    elif rate > 1000:
        return f"{rate}mbps"
    else:
        return f"{rate/1000}gbps"


def convert_mem(mem: float) -> str:
    """Convert memory to string"""
    return f"{mem}m"


if __name__ == "__main__":
    infrastructure = {
        "aws": {
            "ec2_region": ec2_region,
            "ssh_key_name": ssh_key_name,
            "agent_port": agent_port,
        },
        "machines": [],
        "connections": [],
    }

    # add machines
    # sensor is one combined machine
    sensor_cpu_need = CPU_s * Nsensors
    sensor_mem_need = Mem_s * Nsensors

    # sensor machine type
    sensor_machine_type = get_machine_type(sensor_cpu_need, sensor_mem_need)

    # add sensor machine
    for volcano in volcanoes:
        infrastructure["machines"].append(  # type: ignore
            {
                "machine_name": f"{volcano}_sensors",
                "type": sensor_machine_type,
                "image": ami,
                "cpu": sensor_cpu_need,
                "mem": convert_mem(sensor_mem_need),
            }
        )

    # add the gw machines
    for volcano in volcanoes:
        infrastructure["machines"].append(  # type: ignore
            {
                "machine_name": f"{volcano}_gw",
                "type": get_machine_type(CPU_gw, Mem_gw),
                "image": ami,
                "cpu": CPU_gw,
                "mem": convert_mem(Mem_gw),
            }
        )

    # add on-prem machine
    infrastructure["machines"].append(  # type: ignore
        {
            "machine_name": "onprem_hilo",
            "type": get_machine_type(CPU_onprem, Mem_onprem),
            "image": ami,
            "cpu": CPU_onprem,
            "mem": convert_mem(Mem_onprem),
        }
    )

    # add cloud machine
    for i in range(Ncloud):
        infrastructure["machines"].append(  # type: ignore
            {
                "machine_name": f"cloud_{i}",
                "type": get_machine_type(CPU_cloud, Mem_cloud),
                "image": ami,
                "cpu": CPU_cloud,
                "mem": convert_mem(Mem_cloud),
            }
        )

    # add connections
    # sensor to gw
    for volcano in volcanoes:
        p = volcanoes[volcano]
        conn = connection_properties[p["connection_to_sensors"]]

        infrastructure["connections"].append(  # type: ignore
            {
                "from": f"{volcano}_sensors",
                "to": f"{volcano}_gw",
                "delay": conn["delay_per_km"] * p["mean_dist_to_sensors"],
                "delay-distro": conn["delay_per_km_std"] * p["mean_dist_to_sensors"],
                "rate": convert_rate(conn["bandwidth"]),
                "duplicate": conn["duplication"],
                "loss": conn["loss"],
                "corrupt": conn["corruption"],
                "reordering": conn["reordering"],
            }
        )

    # gw to on-prem
    for volcano in volcanoes:
        p = volcanoes[volcano]
        conn = connection_properties[p["connection_to_onprem"]]

        infrastructure["connections"].append(  # type: ignore
            {
                "from": f"{volcano}_sensors",
                "to": f"{volcano}_gw",
                "delay": conn["delay_per_km"] * p["dist_to_onprem"],
                "delay-distro": conn["delay_per_km_std"] * p["dist_to_onprem"],
                "rate": convert_rate(conn["bandwidth"]),
                "duplicate": conn["duplication"],
                "loss": conn["loss"],
                "corrupt": conn["corruption"],
                "reordering": conn["reordering"],
            }
        )

    # onprem to cloud
    for i in range(Ncloud):
        conn = connection_properties[connection_onprem_to_cloud]
        infrastructure["connections"].append(  # type: ignore
            {
                "from": "onprem_hilo",
                "to": f"cloud_{i}",
                "delay": conn["delay_per_km"] * dist_onprem_to_cloud,
                "delay-distro": conn["delay_per_km_std"] * dist_onprem_to_cloud,
                "rate": convert_rate(conn["bandwidth"]),
                "duplicate": conn["duplication"],
                "loss": conn["loss"],
                "corrupt": conn["corruption"],
                "reordering": conn["reordering"],
            }
        )

    # between clouds
    for i in range(Ncloud):
        for j in range(i + 1, Ncloud):
            conn = connection_properties[connection_cloud_to_cloud]
            infrastructure["connections"].append(  # type: ignore
                {
                    "from": f"cloud_{i}",
                    "to": f"cloud_{j}",
                    "delay": conn["delay_per_km"] * 0,
                    "delay-distro": conn["delay_per_km_std"] * 0,
                    "rate": convert_rate(conn["bandwidth"]),
                    "duplicate": conn["duplication"],
                    "loss": conn["loss"],
                    "corrupt": conn["corruption"],
                    "reordering": conn["reordering"],
                }
            )

    # write to file
    with open(output_file, "w") as f:
        json.dump(infrastructure, f, indent=4)
