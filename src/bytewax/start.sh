#!/bin/bash

python -m bytewax.run workflows/cleanup:flow -r recovery/cleanup -s 30 -b 60 &

python -m bytewax.run workflows/answer_ttr:flow -r recovery/answer_ttr -s 30 -b 60 &

wait
