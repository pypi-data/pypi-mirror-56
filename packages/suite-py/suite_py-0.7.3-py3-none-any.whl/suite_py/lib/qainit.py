from __future__ import print_function, unicode_literals
from .logger import Logger
from .config import Config

from .handler import git_handler as git
import subprocess
# import sys

config = Config().load()
logger = Logger()

# twig_command =
# '{}/twig-binaries/bin/twig-feature'.format(config['user']['projects_home'])
# development only
qainit_dir = '{}/qainit'.format(config['user']['projects_home'])


def qainit_deploy(args):
    git.check_repo_cloned('qainit')
    return subprocess.run(
        ['twig', 'feature', 'suite', 'deploy', args], cwd=qainit_dir, check=True)


def qainit_stop(branch):
    git.check_repo_cloned('qainit')
    git.sync('qainit')
    if git.branch_exists('qainit', branch):
        try:
            subprocess.run(['twig', 'feature', 'suite', 'stop',
                            branch], cwd=qainit_dir, check=True)
        except BaseException:
            logger.error(
                "Non sono riuscito a spegnere il qa, per favore spegnilo manualmente!\nDevops are watching you! ( •͡˘ _•͡˘)")

    else:
        logger.warning(
            "Non sono riuscito a trovare un qa per questa issue, se il qa esiste, per favore spegnilo manualmente\nDevops are watching you! ( •͡˘ _•͡˘)")
