import os
import re
import subprocess

from lib.logging import info, error, warning
from time import sleep

def exec(cmd, cwd=None, verbose=False):
    tag = '[%s]' % os.environ['PROJECT_NAME']
    if verbose:
        info('%s %s' % (tag, cmd))

    if isinstance(cmd, str):
        cmd = cmd.split()

    retry = 0
    max_retries = 3

    while (retry < max_retries):
        try:
            status = subprocess.run(cmd, capture_output=True, cwd=cwd, check=True)
            stdout = status.stdout.decode('utf-8').strip()
            stderr = status.stderr.decode('utf-8').strip()

            if verbose:
                if stdout:
                    print(stdout)
                if stderr:
                    print(stderr)

            return status
        except subprocess.CalledProcessError:
            retry += 1

            warning("last command failed. retries remaining: %s" % (max_retries - retry))
            sleep_time = 30 * retry
            warning('sleeping for %s seconds' % sleep_time)
            sleep(sleep_time)

            if retry == max_retries:
                pass

def get_repo_name(repo, type):
    if type == 'bitbucket':
        regex = re.compile(r'git@bitbucket.org:devolutions\/(.*).git')
    elif type == 'github':
        regex = re.compile(r'git@github.com:Devolutions\/(.*).git')
    result = regex.search(repo)
    
    return result.group(1)
