# BSD 2-Clause License
#
# Copyright (c) 2021, Hewlett Packard Enterprise
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Constants for SmartSim
import os
from .enums import Status

PROJECT_NAME = "SmartSim"
VERSION = "0.3.2"
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ML backend versions
TF_VERSION = "2.4.0"
TORCH_VERSION = "1.7.1"
ONNX_VERSION = "1.6.0"

# Interval for Job Manager
LOCAL_JM_INTERVAL = 2

# Task Manager Interval
TM_INTERVAL = 1

# Status groupings
TERMINAL_STATUSES = (Status.STATUS_CANCELLED,
                     Status.STATUS_COMPLETED,
                     Status.STATUS_FAILED)
LIVE_STATUSES = (Status.STATUS_RUNNING,
                 Status.STATUS_PAUSED,
                 Status.STATUS_NEW)

