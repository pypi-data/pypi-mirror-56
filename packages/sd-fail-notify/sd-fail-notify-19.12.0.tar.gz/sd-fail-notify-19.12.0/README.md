# Systemd Failure Notifier
This is a simple command utility designed to be run on the failure of a systemd unit.

## Usage
`sd-fail-notify <unit-name>`
 
 It is meant to be used with the `%i` unit name option passed in a systemd OnFailure dependency
 
 ## Supported Providers
 
 ### Twilio
 
 Required configuration: from, to, account, token. See example config for details.
