class BinaryLoggable:
    """
    An entity that can be logged by the BinaryLogger.
    """

    def to_bytes(self) -> bytearray:
        """
        Serialize the fields of this object into a byte array.
        """
        pass

    def from_bytes(self, byte_array: bytearray) -> None:
        """
        Deserialize the fields of this object from a given byte array.
        """
        pass
