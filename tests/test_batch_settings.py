import pytest
from smartsim.settings import BsubBatchSettings, QsubBatchSettings, SbatchSettings, CobaltBatchSettings
from smartsim.settings.settings import create_batch_settings

def test_create_pbs_batch():
    pbs_batch = create_batch_settings(
        "pbs", nodes=1, time="10:00:00", queue="default", account="myproject", ncpus=10
    )  # test that kwargs make it to class init
    args = pbs_batch.format_batch_args()
    assert isinstance(pbs_batch, QsubBatchSettings)
    assert args == [
        "-l select=1:ncpus=10",
        "-l place=scatter",
        "-l walltime=10:00:00",
        "-q default",
        "-A myproject",
    ]


def test_create_sbatch():
    batch_args = {"exclusive": None, "oversubscribe": None}
    slurm_batch = create_batch_settings(
        "slurm",
        nodes=1,
        time="10:00:00",
        queue="default",  # actually sets partition
        account="myproject",
        batch_args=batch_args,
        ncpus=10,
    )  # test that kwargs from
    # pbs doesn't effect slurm (im thinking this will be common)

    assert isinstance(slurm_batch, SbatchSettings)
    assert slurm_batch.batch_args["partition"] == "default"
    args = slurm_batch.format_batch_args()
    assert args == [
        "--exclusive",
        "--oversubscribe",
        "--nodes=1",
        "--time=10:00:00",
        "--partition=default",
        "--account=myproject",
    ]


def test_create_bsub():
    batch_args = {"core_isolation": None}
    bsub = create_batch_settings(
        "lsf",
        nodes=1,
        time="10:00:00",
        account="myproject",  # test that account is set
        queue="default",
        batch_args=batch_args,
    )
    assert isinstance(bsub, BsubBatchSettings)
    args = bsub.format_batch_args()
    assert args == ["-core_isolation", "-nnodes 1", "-q default"]


def test_auto_batch(wlmutils):
    launcher = wlmutils.get_test_launcher()
    if launcher == "local":
        pytest.skip(reason="test irrelevant for local launcher")

    fake_batch = create_batch_settings(launcher="auto", nodes=1)
    if launcher == "lsf":
        assert(isinstance(fake_batch, BsubBatchSettings))
    elif launcher == "slurm":
        assert(isinstance(fake_batch, SbatchSettings))
    elif launcher == "pbs":
        assert(isinstance(fake_batch, QsubBatchSettings))
    elif launcher == "cobalt":
        assert(isinstance(fake_batch, CobaltBatchSettings))