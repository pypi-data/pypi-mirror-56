import docker
from blowpipe.model import Step, ContainerInfo
from blowpipe import constants
from blowpipe.exceptions import BlowpipeError
from datetime import datetime
import time

def list_volumes(prefix: str = None) -> int:
    client = docker_client()
    try:
        volumes = client.volumes.list()
        if prefix is not None:
            results = []
            for v in volumes:
                if str(v.name).startswith(prefix):
                    results.append(v)
            return results
        else:
            return volumes
    finally:
        client.close()




def count_volumes(prefix: str = None) -> int:
    return len(list_volumes(prefix))


def list_networks(prefix: str = None) -> int:
    client = docker_client()
    try:
        networks = client.networks.list()
        if prefix is not None:
            results = []
            for n in networks:
                if str(n.name).startswith(prefix):
                    results.append(n)
            return results
        else:
            return networks
    finally:
        client.close()


def count_networks(prefix: str = None) -> int:
    return len(list_networks(prefix))


def list_containers(prefix: str = None) -> int:
    client = docker_client()
    try:
        containers = client.containers.list()
        if prefix is not None:
            results = []
            for c in containers:
                if str(c.name).startswith(prefix):
                    results.append(c)
            return results
        else:
            return containers
    finally:
        client.close()


def count_containers(prefix: str = None) -> int:
    return len(list_containers(prefix))


def is_docker_available() -> bool:
    """
    indicates if docker is available
    :return:
    """
    try:
        client = docker.from_env()
        result = client.ping()
        client.close()
        return result
    except Exception:
        return False


def docker_client():
    """
    creates and returns a docker client
    :return:
    """
    return docker.from_env()


def api_docker_client():
    """
    creates and returns an docker.APIClient
    :return:
    """
    return docker.APIClient()


def get_container_info(step=None, name=None) -> ContainerInfo:
    """
    queries docker for the status of a model.Step, returning a ContainerInfo
    :param step:
    :param name:
    :return:
    """
    client = docker_client()
    try:
        if step is not None:
            output = client.api.inspect_container(step.get_container_name())
            return ContainerInfo(output)
        elif name is not None:
            output = client.api.inspect_container(name)
            return ContainerInfo(output)
        else:
            raise BlowpipeError("No name or step passed to docker_utils.get_container_info")
    except Exception as e:
        return None
    finally:
        client.close()


def start_step(workflow_instance, step, env_vars=None):
    """
    starts a model.Step object on docker, returning the first response
    :param step:
    :param env_vars:
    :return:
    """
    if env_vars is None:
        env_vars = step.environment()

    client = docker_client()

    volume_name = workflow_instance.get_shared_state_volume_name()
    volumes = {volume_name: {"bind": constants.SHARED_STATE_DEFAULT_MOUNT_POINT, "mode": "rw"}}
    try:
        response = start_container(client=client,
                                   image_name=step.get_image_name(),
                                   container_name=step.get_container_name(),
                                   command=step.get_command(),
                                   network=workflow_instance.get_shared_state_network_id(),
                                   volumes=volumes,
                                   detach=True,
                                   auto_remove=False,
                                   environment=env_vars)
        return response

        # return ContainerInfo(response)
    # response = client.containers.run(
    #     image=step.get_image_name(),
    #     name=step.get_container_name(),
    #     command=step.get_command(),
    #     detach=True,
    #     auto_remove=True,
    #     environment=env_vars,
    # )
    finally:
        client.close()


def start_container(client, image_name, container_name, command, network, volumes, detach, auto_remove, environment):
    """
    starts a container
    :param step:
    :param env_vars:
    :return:
    """
    response = client.containers.run(
        image=image_name,
        name=container_name,
        command=command,
        network=network,
        volumes=volumes,
        detach=detach,
        auto_remove=auto_remove,
        environment=environment,
    )
    return response


def wait_for_container_to_exit(self, container_id:str, timeout:int):
    duration = 0
    query_quit = False
    container_info = None
    start = datetime.today()
    while not query_quit:
        container_info = get_container_info(name=container_id)
        query_quit = container_info.is_container_exited()
        if not query_quit:
            time.sleep(0.1)
        now = datetime.today()
        diff = (now - start).seconds
        if diff >= timeout:
            raise BlowpipeError("Timeout exceeded for wait_for_container_to_exit(container_id=" + container_id)

    return container_info


"""
{
    "Id": "60076b33c0fe638840565dc96062876876a27335955d7e1cf1574bbbac041de9",
    "Created": "2019-07-16T17:40:29.5054854Z",
    "Path": "/bin/sh",
    "Args": ["-c", "python /run.py"],
    "State": {
        "Status": "exited",
        "Running": False,
        "Paused": False,
        "Restarting": False,
        "OOMKilled": False,
        "Dead": False,
        "Pid": 0,
        "ExitCode": 7,
        "Error": "",
        "StartedAt": "2019-07-16T17:40:29.9189411Z",
        "FinishedAt": "2019-07-16T17:40:34.9798069Z",
    },
    "Image": "sha256:9747299301827870c03d761bf5abebdb06cdaa5d620327a65543475a0e1af0e4",
    "ResolvConfPath": "/var/lib/docker/containers/60076b33c0fe638840565dc96062876876a27335955d7e1cf1574bbbac041de9/resolv.conf",
    "HostnamePath": "/var/lib/docker/containers/60076b33c0fe638840565dc96062876876a27335955d7e1cf1574bbbac041de9/hostname",
    "HostsPath": "/var/lib/docker/containers/60076b33c0fe638840565dc96062876876a27335955d7e1cf1574bbbac041de9/hosts",
    "LogPath": "/var/lib/docker/containers/60076b33c0fe638840565dc96062876876a27335955d7e1cf1574bbbac041de9/60076b33c0fe638840565dc96062876876a27335955d7e1cf1574bbbac041de9-json.log",
    "Name": "/blowpipe-test_latest-bedccbb7-f4f9-48dc-93b6-3a6347e2baa8",
    "RestartCount": 0,
    "Driver": "overlay2",
    "Platform": "linux",
    "MountLabel": "",
    "ProcessLabel": "",
    "AppArmorProfile": "",
    "ExecIDs": None,
    "HostConfig": {
        "Binds": None,
        "ContainerIDFile": "",
        "LogConfig": {"Type": "json-file", "Config": {}},
        "NetworkMode": "default",
        "PortBindings": None,
        "RestartPolicy": {"Name": "", "MaximumRetryCount": 0},
        "AutoRemove": False,
        "VolumeDriver": "",
        "VolumesFrom": None,
        "CapAdd": None,
        "CapDrop": None,
        "Dns": None,
        "DnsOptions": None,
        "DnsSearch": None,
        "ExtraHosts": None,
        "GroupAdd": None,
        "IpcMode": "shareable",
        "Cgroup": "",
        "Links": None,
        "OomScoreAdj": 0,
        "PidMode": "",
        "Privileged": False,
        "PublishAllPorts": False,
        "ReadonlyRootfs": False,
        "SecurityOpt": None,
        "UTSMode": "",
        "UsernsMode": "",
        "ShmSize": 67108864,
        "Runtime": "runc",
        "ConsoleSize": [0, 0],
        "Isolation": "",
        "CpuShares": 0,
        "Memory": 0,
        "NanoCpus": 0,
        "CgroupParent": "",
        "BlkioWeight": 0,
        "BlkioWeightDevice": None,
        "BlkioDeviceReadBps": None,
        "BlkioDeviceWriteBps": None,
        "BlkioDeviceReadIOps": None,
        "BlkioDeviceWriteIOps": None,
        "CpuPeriod": 0,
        "CpuQuota": 0,
        "CpuRealtimePeriod": 0,
        "CpuRealtimeRuntime": 0,
        "CpusetCpus": "",
        "CpusetMems": "",
        "Devices": None,
        "DeviceCgroupRules": None,
        "DiskQuota": 0,
        "KernelMemory": 0,
        "MemoryReservation": 0,
        "MemorySwap": 0,
        "MemorySwappiness": None,
        "OomKillDisable": False,
        "PidsLimit": 0,
        "Ulimits": None,
        "CpuCount": 0,
        "CpuPercent": 0,
        "IOMaximumIOps": 0,
        "IOMaximumBandwidth": 0,
        "MaskedPaths": [
            "/proc/asound",
            "/proc/acpi",
            "/proc/kcore",
            "/proc/keys",
            "/proc/latency_stats",
            "/proc/timer_list",
            "/proc/timer_stats",
            "/proc/sched_debug",
            "/proc/scsi",
            "/sys/firmware",
        ],
        "ReadonlyPaths": [
            "/proc/bus",
            "/proc/fs",
            "/proc/irq",
            "/proc/sys",
            "/proc/sysrq-trigger",
        ],
    },
    "GraphDriver": {
        "Data": {
            "LowerDir": "/var/lib/docker/overlay2/b2a5b02a0491ab39a900f894fdf6afe486afed972af45055cda2bcb62be8b8c6-init/diff:/var/lib/docker/overlay2/2d1b243823cae7359290b605438993711add0b6b3900300105974f0976f541e4/diff:/var/lib/docker/overlay2/fbe0f9e3ff90474d46e12d41deddc5986d2e54450e50b5c7c8fbcac97ac3ae76/diff:/var/lib/docker/overlay2/2d96314453db69f4bcff519144693c3b7541ac2d966884acfb2889f51800eb69/diff:/var/lib/docker/overlay2/5782791366d169901057b6cf2b7d597df3f39d38ed54766c5f6a7dbb1a0d34c8/diff:/var/lib/docker/overlay2/4fd98f423f989521795ac75fbbb9c9966a84b71d6f24dd9f51cd8f94472c842c/diff:/var/lib/docker/overlay2/9f6f4d3421e7ce419f4249f13631365112b9518baf71838b1b27b20ad7a5aa2d/diff",
            "MergedDir": "/var/lib/docker/overlay2/b2a5b02a0491ab39a900f894fdf6afe486afed972af45055cda2bcb62be8b8c6/merged",
            "UpperDir": "/var/lib/docker/overlay2/b2a5b02a0491ab39a900f894fdf6afe486afed972af45055cda2bcb62be8b8c6/diff",
            "WorkDir": "/var/lib/docker/overlay2/b2a5b02a0491ab39a900f894fdf6afe486afed972af45055cda2bcb62be8b8c6/work",
        },
        "Name": "overlay2",
    },
    "Mounts": [],
    "Config": {
        "Hostname": "60076b33c0fe",
        "Domainname": "",
        "User": "",
        "AttachStdin": False,
        "AttachStdout": False,
        "AttachStderr": False,
        "Tty": False,
        "OpenStdin": False,
        "StdinOnce": False,
        "Env": [
            "EXIT_CODE=7",
            "SLEEP=5",
            "PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
            "LANG=C.UTF-8",
            "GPG_KEY=0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D",
            "PYTHON_VERSION=3.7.2",
            "PYTHON_PIP_VERSION=19.0.1",
        ],
        "Cmd": ["/bin/sh", "-c", "python /run.py"],
        "ArgsEscaped": True,
        "Image": "blowpipe-test:latest",
        "Volumes": None,
        "WorkingDir": "",
        "Entrypoint": None,
        "OnBuild": None,
        "Labels": {},
    },
    "NetworkSettings": {
        "Bridge": "",
        "SandboxID": "fa65f54a9e6914d4b9f163c742d4c3a05415e3df394bd979b0dbbb9a58315e4d",
        "HairpinMode": False,
        "LinkLocalIPv6Address": "",
        "LinkLocalIPv6PrefixLen": 0,
        "Ports": {},
        "SandboxKey": "/var/run/docker/netns/fa65f54a9e69",
        "SecondaryIPAddresses": None,
        "SecondaryIPv6Addresses": None,
        "EndpointID": "",
        "Gateway": "",
        "GlobalIPv6Address": "",
        "GlobalIPv6PrefixLen": 0,
        "IPAddress": "",
        "IPPrefixLen": 0,
        "IPv6Gateway": "",
        "MacAddress": "",
        "Networks": {
            "bridge": {
                "IPAMConfig": None,
                "Links": None,
                "Aliases": None,
                "NetworkID": "6b3b1112a21b2019130ed2917ee6dad8894f4040fa8ac2e7fa7f99d85805475b",
                "EndpointID": "",
                "Gateway": "",
                "IPAddress": "",
                "IPPrefixLen": 0,
                "IPv6Gateway": "",
                "GlobalIPv6Address": "",
                "GlobalIPv6PrefixLen": 0,
                "MacAddress": "",
                "DriverOpts": None,
            }
        },
    },
}
"""