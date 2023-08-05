import socket
import subprocess

import click
import requests
import toml
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client as TwilioClient

HOSTNAME = socket.gethostname()


def get_status_text(unit, user):
    cmd = ["systemctl"]
    if user:
        cmd.append("--user")
    cmd.append("status")
    cmd.append(unit)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return f"{unit} has failed on {HOSTNAME}\n" + result.stdout.decode()


def send_twilio_message(twilio_config, status_text):
    client = TwilioClient(twilio_config["account"], twilio_config["token"])
    try:
        client.messages.create(
            to=twilio_config["to"], from_=twilio_config["from"], body=status_text
        )
    except TwilioRestException as e:
        print(e)


def send_mailgun_message(mailgun_config, status_text, unit):
    with requests.Session() as session:
        response = session.post(
            mailgun_config["endpoint"],
            auth=("api", mailgun_config["key"]),
            data={
                "from": f"{mailgun_config['from_name']} "
                f"<{mailgun_config['from_address']}>",
                "to": mailgun_config["to_address"],
                "subject": f"{unit} has failed on {HOSTNAME}",
                "text": status_text,
            },
        )
        if response.status_code != 200:
            print("Could not send message.")
            print(response.text)


def handle_providers(providers: dict, status_text, unit):
    if twilio_config := providers.get("twilio"):
        send_twilio_message(twilio_config, status_text)
    if mailgun_config := providers.get("mailgun"):
        send_mailgun_message(mailgun_config, status_text, unit)


@click.command()
@click.argument("unit")
@click.option("--user", is_flag=True)
@click.option(
    "-c",
    "--config-path",
    type=click.Path(exists=True),
    default="/etc/sd-fail-notify/config.toml",
)
def cli(unit, user, config_path):
    status_text = get_status_text(unit, user)
    config = toml.load(config_path)
    handle_providers(config["providers"], status_text, unit)
