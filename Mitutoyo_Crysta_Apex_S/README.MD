# Explanations to follow

## scripts for the communication between Mitutoyo Ko-ga-me and Kuka iiwa and Kuka KMR

* monitors the status of Crysta Apex and returns "busy" or "ready"
  * at every status change an mqtt message is published 
    * on the topic "sirris/diep2/klima/apex/machine/status_changed" 
    * with a json object payload in the format {"status_changed":"busy"} 
      * statusses can be: "busy", "ready" or "error".
* listens to messages 
  * on the topic "sirris/diep2/klima1/apex/machine/command"
  * expects a json objec payload in the format {"command":"run"}
