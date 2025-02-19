"""
Checks for default credentials on machines
"""

import argparse
import csv
import pathlib
import sys
import time
import typing

import fabric
import paramiko
import requests


def main(argv: list[str]) -> int:
    argparser: argparse.ArgumentParser = argparse.ArgumentParser(description="Checks for default credentials on machines")
    argparser.add_argument("--delay-time", "-d", default=5.0, type=float,
            help="The minimum delay between requests.")
    argparser.add_argument("--endpoint", "-e", default=None, type=str,
            help="The HTTP endpoint to send warnings to")
    argparser.add_argument("user_file", type=pathlib.Path,
            help="A file containing a newline-separated list of users")
    argparser.add_argument("password_file", type=pathlib.Path,
            help="A file containing a newline-separated list of passwords to try for the users")
    argparser.add_argument("service_file", type=pathlib.Path,
            help="A CSV file containing a list of services.")
    parsedargs: dict[str, typing.Any] = vars(argparser.parse_args())

    users: list[str] = []
    passwords: list[str] = []
    services: list[tuple[str,int]] = []

    with open(parsedargs["user_file"], 'r') as usersfile:
        for user in usersfile:
            users.append(user.rstrip())
    with open(parsedargs["password_file"], 'r') as passwordsfile:
        for password in passwordsfile:
            passwords.append(password.rstrip())
    with open(parsedargs["service_file"], 'r') as servicescsvfile:
        servicescsvreader: csv.DictReader = csv.DictReader(servicescsvfile)
        for servicerow in servicescsvreader:
            if servicerow["service"] == "ssh":
                services.append((servicerow["ip"], int(servicerow["port"])))
    
    if parsedargs["endpoint"] is None:
        print("Note: No webhook endpoint configured. Notifications will be local only.")

    while True:
        for password in passwords:
            for user in users:
                for ip_address, port in services:
                    next_request_start_time: float = time.time() + parsedargs["delay_time"]
                    """The time that the next request should start by"""
                    ssh_connection = fabric.Connection(host=ip_address, port=port, user=user, connect_kwargs={
                        "password": password,
                        "timeout": 8
                    })
                    try:
                        ssh_connection.run("id")
                        print("ERROR: Connection succeeded to " + ip_address + " port " + str(port) + " over SSH. THIS IS BAD!")
                        if parsedargs["endpoint"] is not None:
                            try:
                                requests.post(parsedargs["endpoint"], data="\U0001F6A8 Connection succeeded to " + ip_address + 
                                        " port " + str(port) + " over SSH with default credentials! \U0001F6A8", headers={
                                            "X-Title": "[CRIT] Default Credentials Detected",
                                            "X-Priority": "urgent",
                                            "X_Tags": "defaultcreds,critical",
                                        })
                            except requests.RequestException as e:
                                print("WARN: An exception occured when publishing webhook: " + str(e))
                    except TimeoutError:
                        print("Timed out")
                    except paramiko.ssh_exception.AuthenticationException:
                        print("Authentication failure")

                    # Wait until whenever we should send the next request.
                    time.sleep(max(0, next_request_start_time - time.time()))

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
