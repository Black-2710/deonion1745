import struct

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
        """
        self.cell_type = cell_type
        self.circuit_id = circuit_id
        self.payload = payload

    def serialize(self):
        """Serialize the Tor cell into bytes for transmission.
        
        Returns:
            bytes: The serialized byte representation of the Tor cell.
        """
        # Struct format: one byte for cell type, two bytes for circuit ID
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
        return f"TorCell(type={self.cell_type}, circuit_id={self.circuit_id}, payload={self.payload})"

# Example usage
if __name__ == "__main__":
    # Create a new Tor cell with a sample payload
    try:
        payload = b"Hello, Tor!"
        cell = TorCell(cell_type=TorCell.DATA_CELL, circuit_id=1, payload=payload)

        # Serialize the cell
        serialized_cell = cell.serialize()
        print("Serialized Cell:", serialized_cell)

        # Deserialize the cell back into a TorCell object
        deserialized_cell = TorCell.deserialize(serialized_cell)
        print("Deserialized Cell:", deserialized_cell)

        # Manipulate the cell (e.g., change the payload)
        new_payload = b"Updated payload"
        cell.payload = new_payload
        serialized_cell = cell.serialize()
        print("Re-serialized Cell with new payload:", serialized_cell)

        # Deserialize again to see the updated cell
        deserialized_cell = TorCell.deserialize(serialized_cell)
        print("Deserialized Cell with updated payload:", deserialized_cell)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
