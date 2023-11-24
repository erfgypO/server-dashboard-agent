import socket
import psutil
import platform
from dotenv import load_dotenv
from requests import post
from os import getenv
from time import sleep


def main():
    load_dotenv()

    refresh_interval = int(getenv("REFRESH_INTERVAL")) / 1000

    while True:
        cpu_count = psutil.cpu_count()
        cpu_usage = psutil.cpu_percent(1, False)

        memory = psutil.virtual_memory()

        used_memory = memory.percent
        total_memory = memory.total

        hostname = socket.gethostname()
        os = platform.system()
        arch = platform.processor()

        uptime = psutil.boot_time()

        disk = psutil.disk_usage("/")

        disk_size = int(disk.total / 1000 / 1000)
        disk_usage = int((disk.total - disk.free) / 1000 / 1000)
        disk_usage_percent = 100 - ((disk.free / disk.total) * 100)

        payload = {
            "cpuCoreCount": cpu_count,
            "cpuUsage": cpu_usage,
            "totalMemory": total_memory,
            "usedMemory": used_memory,
            "hostname": hostname,
            "arch": arch,
            "platform": os,
            "uptime": int(uptime),
            "diskSize": disk_size,
            "diskUsed": disk_usage,
            "diskUsedPercent": disk_usage_percent,
        }

        res = post(url=getenv("API_URL"), json=payload, headers={
            "x-api-key": getenv("API_KEY")
        })

        if res.status_code is 200:
            print("Send stats to api")

        sleep(refresh_interval)


if __name__ == '__main__':
    main()
