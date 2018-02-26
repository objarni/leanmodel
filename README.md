[![Build Status](https://travis-ci.org/objarni/leanmodel.svg?branch=master)](https://travis-ci.org/objarni/leanmodel)


Lean Business Model
-------------------

A humble attempt at simulating a Lean Business.

Example of interaction with this script:

```
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

How many machines do you want in your business model?
>>> 2
What time does machine 0 take to process one flow unit?
>>> 5
How many queue slots does machine 0 have?
>>> 5
What time does machine 1 take to process one flow unit?
>>> 5
How many queue slots does machine 1 have?
>>> 0
The expected delivery time of the business is: 35.0
```
