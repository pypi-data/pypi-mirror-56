#!/usr/bin/env python

"""start or stop (depending on current state) ec2 instances with tag Name:example"""

import argparse
from argparse import RawTextHelpFormatter as rawtxt
import sys
from os.path import expanduser
import signal
import json
import subprocess
import time
import os
import configparser
import pkg_resources
import inquirer
from stringcolor import cs, bold, underline

def signal_handler(sig, frame):
    """handle control c"""
    print('\nuser cancelled')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def query_yes_no(question, default="yes"):
    '''confirm or decline'''
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("\nPlease respond with 'yes' or 'no' (or 'y' or 'n').\n")

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which
    return which(name) is not None

def main():
    '''starts and stops ec2 instances with tag names.'''
    version = pkg_resources.require("trafficlight")[0].version
    parser = argparse.ArgumentParser(
        description='start or stop (depending on current state) ec2 instances with tag Name:example',
        prog='trafficlight',
        formatter_class=rawtxt
    )

    #parser.print_help()
    parser.add_argument(
        "tag",
        help="""starts and stops ec2 instances with tag names.\n\n
    $ trafficlight example\n
    where example is the value for the tag with key Name""",
        nargs='?',
        default='none'
    )
    parser.add_argument('--key', help="optional. use a tag key besides Name", default="Name")
    parser.add_argument('-g', '--green', action='store_true', help='start.')
    parser.add_argument('-r', '--red', action='store_true', help='stop.')
    parser.add_argument('-y', '--yes', action='store_true', help='automatically approve instance state change.')
    parser.add_argument('-H', '--host', action='store_true', help='use hostnames instead of ip addresses.')
    parser.add_argument('-c', '--connect', action='store_true', help='begin an ssh session.')
    parser.add_argument('-p', '--pipe', action='store_true', help='output instance ip or hostname via standard out to pipe into other commands.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+version)
    args = parser.parse_args()
    tag = args.tag
    key = args.key
    green = args.green
    red = args.red
    host = args.host
    yes = args.yes
    connect = args.connect
    pipe = args.pipe
    do_nothing = False

    # check for aws
    if not is_tool("aws"):
        print(cs("this program requires aws cli", "yellow"))
        print("to install it run", cs("pip3 install awscli --upgrade --user", "fuchsia"))
        exit()

    # error checking for both stop and start and no flags.
    if green and red:
        print(cs("you cannot both start and stop.", "yellow"))
        print("either", cs("--green", "green"), "to start instances or", cs("--red", "red"), "to stop.")
        print("omit the flag to", cs("green light", "green"), "stopped instances and", cs("red light", "red"), "running instances.")
        exit()

    # error checking for both stop and connect flags.
    if red and connect:
        print(cs("you cannot connect to an instance you're stopping.", "yellow"))
        exit()

    if not pipe:
        print("checking for instances...")

    # if there's no positional arg output info for all instances and do nothing
    if tag == "none":
        cmd = "aws ec2 describe-instances --output json"
        instances = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
        if not red and not green:
            do_nothing = True
    # else get info for instances with tag name
    else:
        cmd = "aws ec2 describe-instances --filters 'Name=tag:{},Values={}' --output json"
        instances = subprocess.check_output(cmd.format(key, tag), shell=True).decode("utf-8").strip()

    # process the instance data
    instances = json.loads(instances)
    instances = instances['Reservations']
    number_of_instances = len(instances)

    # no instances found with the tag name given
    if number_of_instances == 0:
        print(cs("no instances found.", "yellow"))
        exit()

    # cannot connect to more than one instance
    if connect and number_of_instances > 1:
        print(cs("you've passed the --connect flag but there are more than one instances to list.", "yellow"))
        print(cs("if you'd like to use traffic light to connect to this instance, use a unique tag", "orange"), cs("Name", "orange").bold(), cs("or another tag with the --key flag.", "orange"))
        print()
        print(cs("for more information try:", "lightgrey2"), cs("trafficlight -h", "pink"))
        exit()

    # collect info
    state_code = 0
    for instance in instances:
        instance_id = instance['Instances'][0]['InstanceId']
        image_id = instance['Instances'][0]['ImageId']
        state_code = instance['Instances'][0]['State']['Code']
        state_name = instance['Instances'][0]['State']['Name']
        instance_type = instance['Instances'][0]['InstanceType']
        try:
            instance_tags = instance['Instances'][0]['Tags']
        except KeyError as e:
            instance_tags = ""
        tags_list = ""
        for instance_tag in instance_tags:
            tags_list += instance_tag['Key']+":"+instance_tag['Value']+", "
        tags_list = tags_list[:-2]
        if state_code == 16:
            state_color = "green"
            instance_ip = instance['Instances'][0]['PublicIpAddress']
            instance_host = instance['Instances'][0]['PublicDnsName']
            if host:
                description = instance_id+" - "+instance_type+" - "+instance_host
            else:
                description = instance_id+" - "+instance_type+" - "+instance_ip
        elif state_code == 80:
            state_color = "red"
            description = instance_id+" - "+instance_type
        else:
            state_color = "yellow"
            description = instance_id+" - "+instance_type

        # output instance info
        if pipe:
            description = description.replace(" - ", " ")
            sys.stdout.write(description + '\n')
        else:
            print(cs(state_name+"\n"+description+"\nTags: "+tags_list, state_color))
            print("-------")

    # set up naming for future print statements
    switch = False
    verbing = False
    if green:
        if connect:
            question = "start instances and connect?"
        else:
            question = "start instances?"
        switch = "start-instances"
        verb = "started"
        verbing = cs("starting", "green")
    elif red:
        question = "stop instances?"
        switch = "stop-instances"
        verb = "stopped"
        verbing = cs("stopping", "red")
    else:
        if connect:
            question = "connect?"
        else:
            question = "switch instance state?"
        verb = "switched"

    # switch instance states
    if not do_nothing and not pipe:
        if yes or query_yes_no(question, "yes"):
            state_code = 0
            tmp_switch = ""
            connect_to_started = False
            for instance in instances:
                instance_id = instance['Instances'][0]['InstanceId']
                state_code = instance['Instances'][0]['State']['Code']
                if state_code == 16  or state_code == 80:
                    if state_code == 16:
                        tmp_switch = "stop-instances"
                        tmp_verbing = cs("stopping", "red")
                    else:
                        tmp_switch = "start-instances"
                        tmp_verbing = cs("starting", "green")
                    if switch:
                        cmd = "aws ec2 "+switch+" --instance-ids "+instance_id
                        run = subprocess.check_output(cmd, shell=True)
                    else:
                        cmd = "aws ec2 "+tmp_switch+" --instance-ids "+instance_id
                        if tmp_switch == "stop-instances" and connect:
                            connect_to_started = True
                        else:
                            run = subprocess.check_output(cmd, shell=True)
                    if verbing:
                        print(verbing, instance_id)
                    elif not connect_to_started:
                        print(tmp_verbing, instance_id)
                else:
                    print(cs(instance_id+" not in a state to be "+verb, "yellow"))

            # connect to ec2 via ssh
            if connect:
                # handle key file config
                home = expanduser('~')
                trafficlight_config = os.path.join(home, ".trafficlight.ini")
                config_exists = False
                if os.path.exists(trafficlight_config):
                    config = configparser.ConfigParser()
                    config.read(trafficlight_config)
                    if "keyfile" in config['default']:
                        config_exists = True
                        keyfile = config['default']['keyfile']

                # config doesn't exist. creating a new one.
                if not config_exists:
                    print(cs("deprecated config file or no config file found.", "Khaki"))
                    keyfile = "unknown"
                    newconfig = """[default]
keyfile = {}
"""
                    while True:
                        keyfile = input("Full path to .pem keyfile ["+str(underline(keyfile))+"] : ") or keyfile
                        if not keyfile.endswith(".pem"):
                            keyfile = "unknown"
                            print(cs("ERROR:", "red"), cs("keyfile name must be .pem", "yellow"))
                            continue
                        elif not os.path.isfile(keyfile):
                            keyfile = "unknown"
                            print(cs("ERROR:", "red"), cs("file does not exist", "yellow"))
                            continue
                        else:
                            break
                    newconfig = newconfig.format(keyfile)
                    print(cs("for your convenience,", "PaleTurquoise"), cs("writing keyfile path to ~/.trafficlight.ini", "pink"))
                    with open(trafficlight_config, 'w+') as f:
                        f.write(newconfig)

                # calculate ssh username with ami
                # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connection-prereqs.html#connection-prereqs-get-info-about-instance
                ami_types = {
                    "Amazon Linux 2":"ec2-user",
                    "CentOS":"centos",
                    "Debian":"root",
                    "Fedora":"ec2-user",
                    "RHEL":"ec2-user",
                    "SUSE":"ec2-user",
                    "Ubuntu":"ubuntu",
                }
                image_cmd = "aws ec2 describe-images --image-ids \""+image_id+"\" --output json"
                image_json = subprocess.check_output(image_cmd, shell=True).decode("utf-8").strip()
                image_json = json.loads(image_json)
                os_descrip = image_json["Images"][0]["Description"]
                username = "ec2-user"
                for k, v in ami_types.items():
                    if k in os_descrip:
                        username = v

                # instance starting (above) wait for a ready state then get IP
                if not connect_to_started:
                    print(cs("please wait while the instance finishes starting...", "IndianRed"))
                    start_time = time.time()
                    state_code = 0
                    while state_code != 16:
                        cmd = "aws ec2 describe-instances --instance-ids {} --output json".format(instance_id)
                        instances = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
                        instances = json.loads(instances)
                        instances = instances['Reservations']
                        for instance in instances:
                            state_code = instance['Instances'][0]['State']['Code']
                        elapsed_time = time.time() - start_time
                        elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                        elapsed_time = str(elapsed_time)
                        print(cs(" --> Time Elapsed:", "grey"), elapsed_time+"     ", end="\r")
                    countdown = 15
                    while countdown > 0:
                        time.sleep(1)
                        elapsed_time = time.time() - start_time
                        elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                        elapsed_time = str(elapsed_time)
                        print(cs(" --> Time Elapsed:", "grey"), elapsed_time+"     ", end="\r")
                        countdown -= 1
                    cmd = "aws ec2 describe-instances --instance-ids {} --output json".format(instance_id)
                    instances = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
                    instances = json.loads(instances)
                    instances = instances['Reservations']
                    for instance in instances:
                        instance_ip = instance['Instances'][0]['PublicIpAddress']
                        instance_host = instance['Instances'][0]['PublicDnsName']
                    print(cs(" --> Time Elapsed:", "lightgrey4"), elapsed_time+"     ")

                # lets do some actual connecting
                if host:
                    cmd = cmd = "ssh -i {} {}@{}".format(keyfile, username, instance_host)
                else:
                    cmd = "ssh -i {} {}@{}".format(keyfile, username, instance_ip)
                subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    main()
