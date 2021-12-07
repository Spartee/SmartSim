

import asyncio

import asyncio
import sys

async def get_date():
    code = 'import datetime; print(datetime.datetime.now()); import time; time.sleep(10);'
    print("starting ...")
    # Create the subprocess; redirect the standard output
    # into a pipe.
    proc = await asyncio.create_subprocess_exec(
        sys.executable, '-c', code,
        stdout=asyncio.subprocess.PIPE)

    await proc.wait()

    out, err = await proc.communicate()

    return out.decode("utf-8")

date = await asyncio.run(get_date())
print("FUCKKK")
date = await asyncio.run(get_date())

print(f"Current date: {date}")