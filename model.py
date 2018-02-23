# coding: utf-8
import doctest


class Business(object):
    def __init__(self):
        self.machines = []

    def add_machine(self, machine):
        self.machines.append(machine)

    def average_delivery_time(self):
        def machine_avg(m):
            return (m.queue_size + 1) * float(m.process_time)
        return sum(machine_avg(m) for m in self.machines)


class Machine(object):
    def __init__(self, queue_size, process_time):
        self.process_time = process_time
        self.queue_size = queue_size



def selftest():
    """A Lean model!

    We want to model how the 'flow' of in Lean as described
    by N. Modig and P. Nordström works.

    They include a lot of concepts:

    - flow unit
    - resources
    - 'stations' or 'machines'
    - processes / factory layouts
    - process times (on average)
    - queues
    - variation (in input and among machines)
    - value adding activities
    - waste
    - ... probably more I've forgotten about.

    But I don't want or need to encompass all of it
    to start with! It's enough to think about machines, processes,
    flow units, process times to figure out the most
    important thing about a 'business': the time it
    takes from order to delivery!

    First example, a business with a single 'pit-stop'.
    This means a single 'machine'. Here, the average
    delivery time is simply the delivery time of the
    machine:

    >>> b = Business()
    >>> m = Machine(process_time=1.0, queue_size=0)
    >>> b.add_machine(m)
    >>> b.average_delivery_time()
    1.0

    Now, if we change queue_size to 1, things can
    start piling up at the only machine. This means
    the delivery time is increased to 2, as the new
    flow unit will have to wait in line to be processed:

    >>> m.queue_size = 1
    >>> b.average_delivery_time()
    2.0

    Now, if we increase process_time to 2, each unit
    takes twice the time to process. This means a doubled
    delivery time:

    >>> m.process_time = 2
    >>> b.average_delivery_time()
    4.0

    If we have a business process of two machines, no queues,
    and a process time of 10 in each machine, the average delivery
    time is the sum of the individual steps:

    >>> b2 = Business()
    >>> m1 = Machine(process_time=10, queue_size=0)
    >>> m2 = Machine(process_time=10, queue_size=0)
    >>> b2.add_machine(m1)
    >>> b2.add_machine(m2)
    >>> b2.average_delivery_time()
    20.0

    If we add a queue of 10 units to the first machine,
    we make a "stack" on that step in the process, which
    means the average goes high up:

    >>> m1.queue_size = 10
    >>> b2.average_delivery_time()
    120.0

    (Think about it: a flow unit needs to be processed
    by the first machine, but in order to be processed,
    it has to wait in line for a whole of 10 units
    to be processed before it. That's a 100 time units.
    Then, it will be processed by the machine itself,
    another 10 time units. Finally, it is ready for
    processing in second machine, another ten, a total
    of 120.

    It does not matter in which order the machines are,
    so if the long queue is on the second machine instead
    of the first, we get the same average delivery time:

    >>> m1.queue_size = 0
    >>> m2.queue_size = 10
    >>> b2.average_delivery_time()
    120.0

    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
