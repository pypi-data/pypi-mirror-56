Sight Machine
-------------

The `BinaryLogger` allows to store instances of `BinaryLoggable` classes and
then enumerate all entries of any specified class in reverse order::

    import sight_machine
    with sight_machine.BinaryLogger() as log:
        log.write(BinaryLoggableX())
        log.write(BinaryLoggableY())
        log.write(BinaryLoggableX())
        log.write(BinaryLoggableX())

        for entry in log.read(BinaryLoggableX)):
            print(entry)

