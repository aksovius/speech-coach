#!/bin/bash

# Run cleanup flow
python -m bytewax.run stream.workflows.cleanup:flow -r stream/recovery/cleanup -s 30 -b 60 &
python -m bytewax.run stream.workflows.answer_ttr:flow -r stream/recovery/answer_ttr -s 30 -b 60 &
python -m bytewax.run stream.workflows.active_words:flow -r stream/recovery/active_words -s 30 -b 60 &
# Wait for all background processes
wait
