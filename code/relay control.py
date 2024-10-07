from stem import Signal
from stem.control import Controller

# Connect to Tor's ControlPort (assuming it's set to 9051)
with Controller.from_port(port=9051) as controller:
    # Authenticate with the password
    controller.authenticate(password='yourpassword')

    # Send a signal to Tor to reload its configuration
    controller.signal(Signal.RELOAD)

    # Or you can use other signals, like NEWNYM to get a new circuit
    controller.signal(Signal.NEWNYM)

    # Get information about the relay's status
    relay_status = controller.get_info("status/circuit-established")
    print("Circuit established?" + relay_status)
