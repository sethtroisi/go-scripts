#!/usr/bin/env python3

import os
import re
import tensorflow as tf

BASE = "../cloudygo/instance/data"
runs = os.listdir(BASE)
runs = [r for r in runs if r.startswith('v')]
runs.sort()

print (runs)
for r in runs:
    bootstrap = os.path.join(BASE, r, "models", "000000-bootstrap")
    size = os.path.getsize(bootstrap + ".data-00000-of-00001")
    var_names = tf.train.load_checkpoint(bootstrap).get_variable_to_dtype_map()
    print(r, size, len(var_names))
    max_conv = max(k for k in var_names.keys() if re.match('conv2d_[0-9]{2}', k))
    shape = tf.train.load_variable(bootstrap, max_conv).shape
    print("\t", max_conv, shape)
    print()

