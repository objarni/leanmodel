# coding: utf-8
import doctest


class Business(object):
    def __init__(self, machines=None):
        self.machines = machines if machines else []

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


def ask(q):
    inp = raw_input if raw_input else input
    print(q)
    return inp()

def selftest():
    """A Lean model!

    We want to model how the 'flow' of in Lean as described
    by N. Modig and P. Åhlströms works.

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


    
    ||||  Observation 1 - bottle necks are worse in end |||

    This is an interesting observation: if your bottleneck
    is placed in the end of the line, it will slow down
    every station/machine before it!

    Imagine a 5 station business. If we have one station
    taking 5 times as long as any of the other stations,
    how much difference does it make to put the station
    in first instead of last?

    >>> fast_machines = [Machine(queue_size=0, process_time=1) for x in range(4)]
    >>> slow_machine = Machine(queue_size=0, process_time=5)
    >>> b4 = Business(machines=fast_machines + [slow_machine])
    >>> b4.expected_delivery_time()
    25.0
    >>> b5 = Business(machines=[slow_machine] + fast_machines)
    >>> b5.expected_delivery_time()
    9.0

    So in this simple model, the delivery time was tripled
    because of the machine being placed last instead of first!



    ||| Observation 2 - queues are killing process times! |||

    Another observation: adding a queue to a station, is the
    same as slowing down the station by the number of queue slots
    plus one.

    To prove this, we'll compare the expected delivery time of
    a slow machine with process time 5, no queue, and a fast machine
    with process time 1, but a queue of 4 units:

    >>> b6 = Business(machines=[Machine(queue_size=0, process_time=5)])
    >>> b6.expected_delivery_time()
    5.0
    >>> b7 = Business(machines=[Machine(queue_size=4, process_time=1)])
    >>> b7.expected_delivery_time()
    5.0

    """
# observation 1: bottlenecks are _much_ worse in end of process
#                than start!
# observation 2: a queue of size N is the same as multiplying
#                process_time with N+1!!!

doc = """
Welcome to Lean Business Model!
This model simulates a very simplistic 'flow model'
as described in N. Modig and P. Åhlströms book "Detta är Lean!"
(ISBN: 978-91-87791-13-0).

We simulate a business delivery process by thinking of it as
a series of "machines" or "stations" that sequentially enhances
the value of the "product" or "flow unit".

Each machine is modelled as something that has:

  1) a process time per unit
  2) a queue size.

We do not model variation neither external (in flow units)
nor internal (downtime in machines).

A business is then, in this simple model, just a series of
machines.

What we are interested to know is the expected delivery time
of the modelled business, when the business is working at
full capacity.
"""

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print(doc)
    n = int(ask("How many machines do you want in your business model?"))
    machines = []
    for i in range(n):
        t = float(ask("What time does machine %d take to process one flow unit?" % i))
        q = int(ask("How many queue slots does machine %d have?" % i))
        machines.append(Machine(process_time=t, queue_size=q))
    business = Business(machines=machines)

    print("The expected delivery time of the business is: %1.1f" %
        business.expected_delivery_time())

