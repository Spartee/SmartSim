import sys
import site
import argparse
import subprocess
from pathlib import Path
import pkg_resources

from smartsim.core.cli.utils import colorize, SetupError, Warning_


class Version:

    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        return ".".join((str(self.major),
                         str(self.minor),
                         str(self.patch)))

def pip_install(packages, end_point=None, verbose=False):
    """Install a pip package to be used in the SmartSim build
    Currently only Torch shared libraries are re-used for the build
    """
    if end_point:
        packages.append(f"-f {end_point}")
    packages = " ".join(packages)

    # form pip install command
    cmd = ["python", "-m", "pip", "install", packages]
    cmd = " ".join(cmd)

    if verbose:
        print(f"Installing packages {packages}...")
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, err = proc.communicate()
    returncode = int(proc.returncode)
    if returncode != 0:
        error = f"{packages} installation failed with exitcode {returncode}\n"
        error += err.decode("utf-8")
        raise SetupError(error)
    if verbose:
        print(f"{packages} installed successfully")


class Build:

    torch_version = Version(1, 7, 1)
    torchvis_version = Version(0, 8, 2)
    tf_version = Version(2, 4, 2)
    onnx_version = Version(1, 7, 0)

    def __init__(self, install_path):

        parser = argparse.ArgumentParser()
        parser.add_argument('-v', action="store_true", default=False,
                            help='Enable verbose build process')
        parser.add_argument('--device', type=str, default="cpu",
                            help='Device to build ML runtimes for (cpu || gpu)')
        parser.add_argument('--no_pt', action="store_true", default=False,
                            help='Do not build PyTorch backend')
        parser.add_argument('--no_tf', action="store_true", default=False,
                            help='Do not build TensorFlow backend')
        parser.add_argument('--onnx', action="store_true", default=False,
                            help='Build ONNX backend (off by default)')
        parser.add_argument('--torch_dir', default=None, type=str,
                            help='Path to custom <path>/torch/share/cmake/Torch/ directory (ONLY USE IF NEEDED)')
        args = parser.parse_args(sys.argv[2:])
        self.verbose = args.verbose

        self.script = install_path.joinpath("core/bin/smartsim_setup")

        if not self.script.is_file():
            msg = "Could not find smartsim_setup script. "
            msg += "You may have to trigger manually from the installation site"
            raise SetupError(msg)

        # check if user pointed to existing torch installation
        if args.torch_dir:
            user_torch_dir = Path(args.torch_dir).resolve()
            if not user_torch_dir.is_dir():
                raise SetupError("Could not find requested user Torch installation")
            self.torch_dir = str(user_torch_dir)
        else:
            self.torch_dir = None # pip install it

        # decide which runtimes to build
        print("\nBackends Requested")
        print("-------------------")
        print(f"    PyTorch: {color(not args.no_pt)}")
        print(f"    TensorFlow: {color(not args.no_tf)}")
        print(f"    ONNX: {color(args.onnx)}")
        print("\n")
        pt = 0 if args.no_pt else 1
        tf = 0 if args.no_tf else 1
        onnx = 1 if args.onnx else 0

        self.run_build(args.device, pt, tf, onnx)


    def run_build(self, device, pt, tf, onnx):
        print("Running SmartSim build process...")
        cmd = []
        device = device.lower()

        # sanity check for platform and tooling
        self.check_prereq("make")
        self.check_prereq("cmake")
        self.check_prereq("git-lfs")
        self.check_platform(device, onnx=onnx)

        # TORCH
        if pt == 1:
            if not self.torch_dir:
                self.install_torch(device=device)
                self.torch_dir = str(self.find_torch())
            cmd.append(f"Torch_DIR={self.torch_dir}")

        # ONNX
        if onnx == 1:
            self.check_onnx_install()

        # TF
        if tf == 1:
            self.check_tf_install()

        cmd.extend([f"PT={pt} TF={tf} TFL=0 ONNX={onnx}", str(self.script), device])
        cmd = " ".join(cmd)
        if self.verbose:
            subprocess.check_call(cmd, shell=True)
        else:
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _, err = proc.communicate()
            returncode = int(proc.returncode)
            if returncode != 0:
                error = f"SmartSim setup failed with exitcode {returncode}\n"
                error += err.decode("utf-8")
                raise SetupError(error)
            else:
                print("SmartSim setup complete!")


    @staticmethod
    def check_installed(package, supported):
        try:
            installed_version = pkg_resources.get_distribution(package).version
            installed_major, installed_minor, _ = installed_version.split(".")
            if int(installed_major) != supported.major or int(installed_minor) != supported.minor:
                msg = f"Only {package} version {supported} is offically supported. You have {installed_version}"
                raise SetupError(msg)
            else:
                return True
        except pkg_resources.DistributionNotFound:
            return False

    def install_torch(self, device="cpu"):
        """Torch shared libraries installed by pip are used in the build
        for SmartSim backends so we download them here.

        Raises SetupError if incompatible version is installed
        """
        packages = []
        end_point = None
        if not self.check_installed("torch", self.torch_version):
            # if we are on linux cpu, use the torch without CUDA
            if sys.platform == "linux" and device == "cpu":
                packages.append(f"torch=={self.torch_version}+cpu")
                packages.append(f"torchvision=={self.torchvis_version}+cpu")
                end_point = "https://download.pytorch.org/whl/torch_stable.html"
            # otherwise just use the version downloaded by pip
            else:
                packages.append(f"torch=={self.torch_version}")
                packages.append(f"torchvision=={self.torchvis_version}")

            pip_install(packages, end_point=end_point, verbose=self.verbose)
        else:
            installed_ver = pkg_resources.get_distribution("torch").version
            _, _, patch = installed_ver.split(".")
            if "cpu" in patch and device == "gpu":
                msg = "Torch CPU is currently installed but torch GPU requested. Uninstall all torch packages"
                msg += " and run the `smart` command again to obtain Torch GPU libraries"
                print(Warning_(msg))
            if device == "cpu" and "cpu" not in patch:
                msg = "Torch GPU installed in python environment but requested Torch CPU."
                msg += " Run `pip uninstall torch torchvision` and run `smart` again"
                print(Warning_(msg))
            print("Torch installed in Python environment")


    def check_onnx_install(self):
        """Check Python environment for ONNX installation"""
        # conversions tools for ONNX
        packages = [
            "skl2onnx==1.9.0",
            "onnxmltools==1.7.0",
            "onnx==1.7.0"
        ]
        try:
            if not self.check_installed("onnx", self.onnx_version):
                msg = f"ONNX {self.onnx_version} not installed in python environment\n"
                msg += f"Consider installing {' '.join(packages)} with pip"
                print(Warning_(msg))
            else:
                print("ONNX installed in Python environment")
        except SetupError as e:
            print(Warning_(str(e)))

    def check_tf_install(self):
        """Check Python environment for TensorFlow installation"""

        try:
            if not self.check_installed("tensorflow", self.tf_version):
                msg = f"TensorFlow {self.tf_version} not installed in Python environment\n"
                msg += f"Consider installing tensorflow=={self.tf_version} with pip"
                print(Warning_(msg))
            else:
                print("TensorFlow installed in Python environment")
        except SetupError as e:
            print(Warning_(str(e)))

    @staticmethod
    def check_platform(device, onnx=0):

        if sys.platform == "darwin":
            if device == "gpu":
                raise SetupError("SmartSim does not support GPU builds on MacOS")
            if onnx:
                raise SetupError("ONNX runtime is currently not supported on MacOS")

        if sys.platform in ["msys", "win32", "cygwin"]:
            msg = "Windows is not supported, but kudos to you for making it this far!"
            raise SetupError(msg)

    @staticmethod
    def check_prereq(command):
        try:
            cmd = " ".join([command, '--version'])
            _ = subprocess.check_call(cmd, shell=True,
                                      stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL)
        except (subprocess.SubprocessError, OSError):
            raise SetupError(
                f"{command} must be installed to build SmartSim") from None

    @staticmethod
    def find_site_packages_path():
        site_path = Path(site.getsitepackages()[0]).resolve()
        return site_path

    def find_torch(self):
        site_path = self.find_site_packages_path()
        torch_path = site_path.joinpath("torch/share/cmake/Torch/").resolve()
        return torch_path

    @staticmethod
    def make_description():
        header = "\nSmartSim Build\n"
        header += "----------------\n\n"
        header = colorize(header, bold=True, color="cyan")

        prebuilts = colorize("Supported Systems for ML backends\n", color="cyan")
        systems = "  1) Linux CPU (x86_64)\n"
        systems += "  2) MacOS CPU (x86_64)\n"
        systems += "  3) Linux GPU (CUDA >= 11)\n\n"
        systems = colorize(systems, color="green")

        default = "By default, the PyTorch and TensorFlow backends will\n"
        default += "be installed.\n"
        default = colorize(default, color="green")

        return "".join((header, prebuilts, systems, default))

def color(is_in_build=True):
    _color = "green" if is_in_build else "red"
    return colorize(str(is_in_build), color=_color)

