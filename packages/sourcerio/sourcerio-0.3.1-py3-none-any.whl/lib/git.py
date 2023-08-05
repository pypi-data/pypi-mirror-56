import os
import re

from lib.logging import info, warning
from lib.utils import exec, get_repo_name

class Git(object):
    def __init__(self, repo, dir, repo_name, verbose):
        self.dir = dir
        self.repo = repo
        self.repo_name = repo_name
        self.verbose = verbose

        os.environ['PROJECT_NAME'] = repo_name

    def clone(self):
        status = exec('git clone %s %s' % (self.repo, self.dir), verbose=self.verbose)

        if status.returncode is not 0:
            raise Exception(status.stderr.decode('utf-8'))

    def current_branch(self):
        status = exec('git branch', cwd=self.dir, verbose=False)

        if status.returncode is not 0:
            raise Exception(status.stderr.decode('utf-8'))

        regex = re.compile(r'^\* (.*)$')
        branch = regex.search(status.stdout.decode('utf-8')).group(1)

        return branch

    def fetch(self):
        cmd = 'git fetch'
        if self.verbose:
            cmd += ' -v'

        status = exec(cmd, cwd=self.dir, verbose=self.verbose)

        if status.returncode is not 0:
            raise Exception(status.stderr.decode('utf-8'))

    def list_remote_refs(self):
        cmd = 'git ls-remote -h origin'

        refs = []
        status = exec(cmd, cwd=self.dir, verbose=False)
        for line in status.stdout.decode('utf-8').splitlines():
            refs.append(line.split()[1])

        if status.returncode is not 0:
            raise Exception(status.stderr.decode('utf-8'))

        return refs

    def pull(self):
        cmd = 'git pull'
        if self.verbose:
            cmd += ' -v'

        status = exec(cmd, cwd=self.dir, verbose=self.verbose)

        if status.returncode is not 0:
            raise Exception(status.stderr.decode('utf-8'))

    def reset_origin_hard(self):
        current_branch = self.current_branch()
        status = exec('git reset --hard origin/%s' % current_branch, cwd=self.dir, verbose=self.verbose)

        if status.returncode is not 0:
            raise Exception(status.stderr.decode('utf-8'))