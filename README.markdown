# A4M33AU: Rail station conversion to TPTP
This project is part of the [A4M33AU][a4m33au] course on [Faculty of Electrical Engineering][fee], the submission is [here][submission] (czech).

## Station format (rail)
The station is represented by directed graph where each node has specific format:

* Simple connection:            `node - in1 out1`
* Connection with signpost:     `node | in1 out1`
* Link with signpost:           `node > in1 in2 out1`
* Coupler:                      `node < in1 out1 out2`
* Input node:                   `node I out1`
* Output node:                  `node O in1`

Example railway station:
    I ----- > --- | --- < ----->
           /             \
          /               \
    I ----                 ---->

Example in rail format:
    a1 I 1
    a2 I 2
    b  > 1 2 3
    c  | 3 4
    d  < 4 5 6
    e1 O 5
    e2 O 6


[fee]: http://www.fel.cvut.cz/
[a4m33au]: https://cw.felk.cvut.cz/doku.php/courses/a4m33au/
[submissin]: https://cw.felk.cvut.cz/doku.php/courses/a4m33au/semestralni_prace
