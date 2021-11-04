import argparse
import shutil
from pathlib import Path
import sys



class Clean:
    def __init__(self, install_path):
        parser = argparse.ArgumentParser(description="Remove previous ML runtime installation")
        parser.add_argument('--clobber', action="store_true", default=False,
                    help='Remove all SmartSim non-python dependencies as well')
        args = parser.parse_args(sys.argv[:2])

        self.clean(install_path, _all=args.clobber)


    def clean(self, install_path, _all=False):
        """Remove pre existing installations of ML runtimes

        :param lib_path: path to installation
        :type lib_path: pathlib.Path
        :param _all: Remove all non-python dependencies
        :type _all: bool, optional
        """
        build_temp = install_path.joinpath(".third-party")
        if build_temp.is_dir():
            shutil.rmtree(build_temp, ignore_errors=True)
        lib_path = install_path.joinpath("lib")
        if lib_path.is_dir():
            # remove RedisAI
            rai_path = lib_path.joinpath("redisai.so")
            if rai_path.is_file():
                rai_path.unlink()
                print("Successfully removed existing RedisAI installation")

            backend_path = lib_path.joinpath("backends")
            if backend_path.is_dir():
                shutil.rmtree(backend_path, ignore_errors=True)
                print("Successfully removed ML runtimes")


        bin_path = install_path.joinpath("bin")
        if bin_path.is_dir() and _all:
            files_to_remove = ["redis-server", "redis-cli"]
            removed = False
            for _file in files_to_remove:
                file_path = bin_path.joinpath(_file)
                if file_path.is_file():
                    removed = True
                    file_path.unlink()
            if removed:
                print("Successfully removed SmartSim Redis installation")

