# Production follow up of the polishing process

A script intended to run on the pc00392 server that listens to socket messages from the iiwa cobot and translates them into mqtt messages.

* listens for socket messages from iiwa polishing cobot,
* translates and sends mqqt message to mosquitto broker.

*Rationale is to avoid having to install mqtt client on iiwa cobot controller.*
