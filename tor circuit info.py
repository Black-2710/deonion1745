from stem import Signal
from stem.control import Controller

def get_tor_circuit_info():
    # Connect to the Tor control port
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()  # Authenticate the connection

        # Signal for a new identity (new circuit)
        print("Requesting a new identity (circuit)...")
        controller.signal(Signal.NEWNYM)

        # Retrieve circuit status
        print("\nCurrent Circuit Info:")
        circuit_info = controller.get_info("circuit-status")
        print(circuit_info)

        # Retrieve detailed information about circuits
        circuits = controller.get_info("circuit-status").splitlines()

        # Display each circuit's details
        for circuit in circuits:
            print(f"\nCircuit Details: {circuit}")

            # Extracting specific details from the circuit string
            if "BUILT" in circuit:
                circuit_id = circuit.split()[0]  # Get the circuit ID
                print(f"Circuit ID: {circuit_id}")

                # Get the path for this circuit
                path_info = controller.get_info(f"circuit/{circuit_id}/path")
                print(f"Path for Circuit {circuit_id}: {path_info}")

                # Get additional info like status
                status_info = controller.get_info(f"circuit/{circuit_id}/status")
                print(f"Status for Circuit {circuit_id}: {status_info}")

def main():
    try:
        get_tor_circuit_info()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
