import logging
import sys
from os import environ
from shutil import which

import pytest
import time

from smartsim import Experiment
from smartsim.ext.ray import RayCluster

"""Test Ray cluster Slurm launch and shutdown.
"""

# retrieved from pytest fixtures
if pytest.test_launcher not in pytest.wlm_options:
    pytestmark = pytest.mark.skip(reason="Not testing WLM integrations")


environ["OMP_NUM_THREADS"] = "1"
try:
    import ray
    import ray.util
except ImportError:
    pass


pytestmark = pytest.mark.skipif(
    ("ray" not in sys.modules),
    reason="requires Ray",
)


def test_ray_launch_and_shutdown(fileutils, wlmutils, caplog):
    launcher = wlmutils.get_test_launcher()
    if launcher != "pbs":
        pytest.skip("Test only runs on systems with PBS as WLM")
    
    caplog.set_level(logging.CRITICAL)
    test_dir = fileutils.make_test_dir("test-ray-pbs-launch-and-shutdown")

    exp = Experiment("ray-cluster", test_dir, launcher=launcher)
    cluster = RayCluster(name="ray-cluster", run_args={}, ray_args={"num-cpus": 4},
                         launcher=launcher, workers=1, alloc=None, batch=False, time="00:05:00",
                         ray_port=6830)

    exp.generate(cluster)
    exp.start(cluster, block=False, summary=False)
    ray.util.connect(cluster.get_head_address()+":10001")

    time.sleep(5)
    right_resources = (len(ray.nodes()), ray.cluster_resources()['CPU']) == (2, 8)

    if not right_resources:
        print(len(ray.nodes()), ray.cluster_resources()['CPU']) 
        ray.util.disconnect()
        exp.stop(cluster)
        assert False

    ray.util.disconnect()
    exp.stop(cluster)
    

def test_ray_launch_and_shutdown_batch(fileutils, wlmutils, caplog):
    launcher = wlmutils.get_test_launcher()
    if launcher != "pbs":
        pytest.skip("Test only runs on systems with PBS as WLM")
    
    caplog.set_level(logging.CRITICAL)
    test_dir = fileutils.make_test_dir("test-ray-pbs-launch-and-shutdown-batch")

    exp = Experiment("ray-cluster", test_dir, launcher=launcher)
    cluster = RayCluster(name="ray-cluster", run_args={}, ray_args={"num-cpus": 4},
                         launcher=launcher, workers=1, alloc=None, batch=True, ray_port=6830, time="00:05:00")

    exp.generate(cluster)
    exp.start(cluster, block=False, summary=False)
    ray.util.connect(cluster.get_head_address()+":10001")

    time.sleep(5)
    right_resources = (len(ray.nodes()), ray.cluster_resources()['CPU']) == (2, 8)

    if not right_resources:
        print(len(ray.nodes()), ray.cluster_resources()['CPU']) 
        ray.util.disconnect()
        exp.stop(cluster)
        assert False

    ray.util.disconnect()
    exp.stop(cluster)