import os
import struct
import hashlib

class TorCell:
    """A class to represent a Tor cell."""

    # Define constants for cell types
    DATA_CELL = 1
    CONTROL_CELL = 2

    def __init__(self, cell_type, circuit_id, payload):
        """Initialize a Tor cell with type, circuit ID, and payload.

        Args:
            cell_type (int): Type of the cell (DATA_CELL or CONTROL_CELL).
            circuit_id (int): ID for the circuit this cell belongs to.
            payload (bytes): The data payload of the cell.

        Raises:
            ValueError: If cell_type is not valid.
        """
        if cell_type not in (self.DATA_CELL, self.CONTROL_CELL):
            raise ValueError("Invalid cell type. Use DATA_CELL or CONTROL_CELL.")
        
        self.cell_type = cell_type
        self.circuit_id = circuit_id
        self.payload = payload

    def serialize(self):
        """Serialize the Tor cell into bytes for transmission.

        Returns:
            bytes: The serialized byte representation of the Tor cell.
        """
        # Pack the cell type (1 byte) and circuit ID (2 bytes) followed by the payload
        return struct.pack('!B H', self.cell_type, self.circuit_id) + self.payload

    @staticmethod
    def deserialize(data):
        """Deserialize bytes into a Tor cell.

        Args:
            data (bytes): The serialized byte representation of a Tor cell.

        Returns:
            TorCell: A TorCell object reconstructed from the serialized data.

        Raises:
            ValueError: If the data is too short to be a valid Tor cell.
        """
        if len(data) < 3:
            raise ValueError("Data too short to be a valid Tor cell.")
        
        # Unpack the first three bytes to get the cell type and circuit ID
        cell_type, circuit_id = struct.unpack('!B H', data[:3])
        payload = data[3:]  # The remaining bytes are the payload
        return TorCell(cell_type, circuit_id, payload)

    def __repr__(self):
        """Return a string representation of the Tor cell."""
        return (f"TorCell(type={self.cell_type}, "
                f"circuit_id={self.circuit_id}, "
                f"payload={self.payload})")

def generate_onion_session_key():
    """Generate a random onion session key.

    Returns:
        str: A hex-encoded string representing the onion session key.
    """
    # Generate a random 32-byte key (256 bits)
    key = os.urandom(32)
    # Hash the key to create a session key using SHA-256
    session_key = hashlib.sha256(key).hexdigest()
    return session_key

def main():
    """Main function to demonstrate Tor cell manipulation and key generation."""
    try:
        # Create a new Tor cell with a sample payload
        payload = b"Hello, Tor!"
        cell = TorCell(cell_type=TorCell.DATA_CELL, circuit_id=1, payload=payload)

        # Serialize the cell
        serialized_cell = cell.serialize()
        print("Serialized Cell:", serialized_cell)

        # Deserialize the cell back into a TorCell object
        deserialized_cell = TorCell.deserialize(serialized_cell)
        print("Deserialized Cell:", deserialized_cell)

        # Generate an onion session key
        onion_session_key = generate_onion_session_key()
        print("Generated Onion Session Key:", onion_session_key)

        # Demonstrate cell manipulation by updating the payload
        new_payload = b"Updated payload"
        cell.payload = new_payload
        print("Updated Cell:", cell)

        # Serialize and deserialize the updated cell to see changes
        updated_serialized_cell = cell.serialize()
        print("Re-serialized Cell with new payload:", updated_serialized_cell)

        # Deserialize again to see the updated cell
        updated_deserialized_cell = TorCell.deserialize(updated_serialized_cell)
        print("Deserialized Updated Cell:", updated_deserialized_cell)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
