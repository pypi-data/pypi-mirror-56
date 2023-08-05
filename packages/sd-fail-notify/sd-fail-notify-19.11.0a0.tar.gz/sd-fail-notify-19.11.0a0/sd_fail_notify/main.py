import subprocess

import click
import toml
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client as TwilioClient


def get_status_text(unit, user):
    cmd = ["systemctl"]
    if user:
        cmd.append("--user")
    cmd.append("status")
    cmd.append(unit)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return f"{unit} has failed to run\n" + result.stdout.decode()


def send_twilio_message(twilio_config, status_text):
    client = TwilioClient(twilio_config["account"], twilio_config["token"])
    try:
        client.messages.create(
            to=twilio_config["to"], from_=twilio_config["from"], body=status_text
        )
    except TwilioRestException as e:
        print(e)


def handle_providers(providers: dict, status_text):
    if twilio_config := providers.get("twilio"):
        send_twilio_message(twilio_config, status_text)


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
    handle_providers(config["providers"], status_text)
