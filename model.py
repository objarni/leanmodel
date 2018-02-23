# coding: utf-8
import doctest


class Business(object):
    def __init__(self):
        self.machines = []

    def add_machine(self, machine):
        self.machines.append(machine)

    def expected_delivery_time(self):
        def single_machine_passthrough_time(m):
            return (m.queue_size + 1) * float(m.process_time)
        slowest_passthrough_time = single_machine_passthrough_time(self.machines[-1])
        delivery_time = 0
        for m in self.machines[::-1]:
            slowest_passthrough_time = max(slowest_passthrough_time, single_machine_passthrough_time(m))
            delivery_time += slowest_passthrough_time
        return delivery_time


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
    >>> b.expected_delivery_time()
    1.0

    Now, if we change queue_size to 1, things can
    start piling up at the only machine. This means
    the delivery time is increased to 2, as the new
    flow unit will have to wait in line to be processed:

    >>> m.queue_size = 1
    >>> b.expected_delivery_time()
    2.0

    Now, if we increase process_time to 2, each unit
    takes twice the time to process. This means a doubled
    delivery time:

    >>> m.process_time = 2
    >>> b.expected_delivery_time()
    4.0

    If we have a business process of two machines, no queues,
    and a process time of 10 in each machine, the average delivery
    time is the sum of the individual steps:

    >>> b2 = Business()
    >>> m1 = Machine(process_time=10, queue_size=0)
    >>> m2 = Machine(process_time=10, queue_size=0)
    >>> b2.add_machine(m1)
    >>> b2.add_machine(m2)
    >>> b2.expected_delivery_time()
    20.0

    If we add a queue of 10 units to the first machine,
    we make a "stack" on that step in the process, which
    means the average goes high up:

    >>> m1.queue_size = 10
    >>> b2.expected_delivery_time()
    120.0

    (Think about it: a flow unit needs to be processed
    by the first machine, but in order to be processed,
    it has to wait in line for a whole of 10 units
    to be processed before it. That's a 100 time units.
    Then, it will be processed by the machine itself,
    another 10 time units. Finally, it is ready for
    processing in second machine, another ten, a total
    of 120.

    After the value unit leaves the burdened 1st machine,
    it sips quickly through the 2nd machine.

    However, if instead it is the second machine that is
    encumbered, or slow, this means units processed in
    1st machine have to wait there until there is a spot
    ready in 2nd machine.

    This is an important observation: any machine down
    the line that is slow, will slow down the whole
    chain before it!

    In the simplest case, we have no queues and two
    machines:

    >>> b3 = Business()
    >>> m1 = Machine(queue_size=0, process_time=1)
    >>> m2 = Machine(queue_size=0, process_time=10)
    >>> b3.add_machine(m1)
    >>> b3.add_machine(m2)
    >>> b3.expected_delivery_time()
    20.0


    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
