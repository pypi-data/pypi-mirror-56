import socket
import subprocess

import click
import requests
import toml
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client as TwilioClient

HOSTNAME = socket.gethostname()


def get_sd_status_text(unit, user):
    cmd = ["systemctl"]
    if user:
        cmd.append("--user")
    cmd.append("status")
    cmd.append(unit)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return result.stdout.decode()


def get_zpool_status(zpool):
    result = subprocess.run(
        ["zpool", "status", zpool], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    return result.stdout.decode()


def send_twilio_message(twilio_config, status_text):
    client = TwilioClient(twilio_config["account"], twilio_config["token"])
    try:
        client.messages.create(
            to=twilio_config["to"], from_=twilio_config["from"], body=status_text
        )
    except TwilioRestException as e:
        print(e)


def send_mailgun_message(mailgun_config, status_text, subject):
    with requests.Session() as session:
        response = session.post(
            mailgun_config["endpoint"],
            auth=("api", mailgun_config["key"]),
            data={
                "from": f"{mailgun_config['from_name']} "
                f"<{mailgun_config['from_address']}>",
                "to": mailgun_config["to_address"],
                "subject": subject,
                "text": status_text,
            },
        )
        if response.status_code != 200:
            print("could not send message.")
            print(response.text)


def handle_providers(providers: dict, status_text, unit):
    if twilio_config := providers.get("twilio"):
        send_twilio_message(twilio_config, status_text)
    if mailgun_config := providers.get("mailgun"):
        send_mailgun_message(mailgun_config, status_text, unit)


def zpool_is_healthy(zpool):
    result = subprocess.run(
        ["zpool", "status", "-x", zpool], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    return f"'{zpool}' is healthy" in result.stdout.decode()


@click.command()
@click.argument("component")
@click.option("--user", is_flag=True, help="Use a user level systemd unit instead")
@click.option(
    "-c",
    "--config-path",
    type=click.Path(exists=True),
    default="/etc/sd-fail-notify/config.toml",
    help="Specify path to configuration file. "
    "Defaults to /etc/sd-fail-notify/config.toml",
)
@click.option(
    "-z",
    "--zpool",
    default=False,
    help="Set component to be a zpool instead of systemd unit",
    is_flag=True,
)
@click.option("--zpool-operation", default=None, help="Which zpool operation failed")
@click.option(
    "--fail-only", default=False, help="Only send messages on failure", is_flag=True
)
def cli(component, user, config_path, zpool, zpool_operation, fail_only):
    """Send notification about COMPONENT

    COMPONENT is the name of the item to check on. By default it is a system-level
    systemd unit.
    """
    if zpool:
        if fail_only and zpool_is_healthy(component):
            return 0
        subject = f"zpool {zpool_operation} has failed on {component} on {HOSTNAME}"
        status_text = subject + "\n" + get_zpool_status(component)
    else:
        subject = f"{component} has failed on {HOSTNAME}"
        status_text = subject + "\n" + get_sd_status_text(component, user)
    config = toml.load(config_path)

    handle_providers(config["providers"], status_text, subject)
