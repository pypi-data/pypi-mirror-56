#!/usr/bin/env python3
import minecraft_launcher_lib
import subprocess
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--username",required=True,help="Your mojang username")
parser.add_argument("--password",required=True,help="Your mojang password")
parser.add_argument("--version",default=minecraft_launcher_lib.utils.get_latest_version()["release"],help="The Minecraft version")
parser.add_argument("--minecraftDir",default=minecraft_launcher_lib.utils.get_minecraft_directory(),help="The path to the Minecraft directory")
parser.add_argument("--executablePath",help="The path to the java executable")
parser.add_argument("--jvmArguments",help="The jvm Arguments")
parser.add_argument("--gameDir",help="Set the game directory")
parser.add_argument("--demo",action="store_true",help="Run Minecraft in demo mode")
parser.add_argument("--resolutionWidth",help="Set the resolution width")
parser.add_argument("--resolutionHeight",help="Set the resolution height")
parser.add_argument("--server",help="The ip of a server where Minecraft connect to after start")
parser.add_argument("--port",help="The port of a server where Minecraft connect to after start")
parser.add_argument("--noInstall",action="store_true",help="Skip Minecraft installation")
parser.add_argument("--command",action="store_true",help="Print the command and do not run Minecraft")
args = parser.parse_args().__dict__

login_data = minecraft_launcher_lib.account.login_user(args["username"],args["password"])

if "errorMessage" in login_data:
    print(login_data["errorMessage"])
    sys.exit(0)

if not args["noInstall"]:
    minecraft_launcher_lib.install.install_minecraft_version(args["version"],args["minecraftDir"],callback={"setStatus":print})

options = {
    "username": login_data["selectedProfile"]["name"],
    "uuid": login_data["selectedProfile"]["id"],
    "token": login_data["accessToken"],
    "launcherName": "mclauncher-cmd",
    "launcherVersion": "1.0",
    "demo": args["demo"],
}

if args["executablePath"]:
    options["executablePath"] = args["executablePath"]

if args["gameDir"]:
    options["gameDirectory"] = args["gameDir"]

if args["jvmArguments"]:
    options["jvmArguments"] = []
    for i in args["jvmArguments"].split(" "):
        options["jvmArguments"].append(i)

if args["resolutionWidth"] or args["resolutionHeight"]:
    options["customResolution"] = True
    options["resolutionWidth"] = args["resolutionWidth"] or "854"
    options["resolutionHeight"] = args["resolutionHeight"] or "480"

if args["server"]:
    options["server"] = args["server"]
    if args["port"]:
        options["port"] = args["port"]

command = minecraft_launcher_lib.command.get_minecraft_command(args["version"],args["minecraftDir"],options)

if args["command"]:
    command_str = ""
    for i in command:
        command_str = command_str + i + " "
    print(command_str[:-1])
    sys.exit(0)

subprocess.call(command)
