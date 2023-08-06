from __future__ import print_function, unicode_literals
from ..lib.handler.youtrack_handler import YoutrackHandler
from ..lib.handler.github_handler import GithubHandler
from ..lib.logger import Logger
from ..lib.qainit import qainit_deploy
from cement import shell

from ..lib.handler import git_handler as git  # import GitHandler
from ..lib.handler import drone_handler as drone
import json
import subprocess
import sys

youtrack = YoutrackHandler()
github = GithubHandler()
logger = Logger()

def entrypoint(args):
    pull_requests = select_pull_requests()
    branches = list(map(lambda pr: github.get_branch_from_pr(
        pr.project.name, pr.github_id), pull_requests))
    dict = {"projects": {}}

    for index, pr in enumerate(pull_requests):
        dict["projects"].update(
            {pr.project.name: {
                "branch": branches[index].name, "revision": branches[index].commit.sha[:14]}}
        )

    dump = json.dumps(dict)
    print(dump)

    json_arg = json.dumps(dump)
    print(json_arg)

    qainit_deploy(json_arg)

    youtrack.update_state(pull_requests[0].youtrack_id, "QA")
    for pr in pull_requests:
        db.update_pr_state(pr, "QA")

    logger.info("Creazione del qa lanciata! Puoi seguire lo stato su {}".format(
        drone.get_last_build_url('qainit')))


def select_pull_requests():
    options = db.get_all_owned_prs_with_qa(user, ['In Progress', 'Review'])

    if not options:
        logger.warning(
            "Non ci sono pull requests su progetti che hanno un qa, nulla da fare")
        sys.exit(0)
    else:
        p = shell.Prompt('Scegli la pull request da mandare in qa',
                         options=options,
                         numbered=True
                         )

    selection = p.prompt()
    other_prs = list(filter(lambda pr: pr.youtrack_id ==
                            selection.youtrack_id and pr.project_id != selection.project_id, options))

    if other_prs:
        logger.info(
            "Ci sono altre pull requests con lo stesso youtrack id di quella selezionata:")
        for pr in other_prs:
            print(pr)

        p = shell.Prompt("Vuoi aggiungerle alla build del qa?",
                         options=['yes', 'no'])

        if (p.prompt() == 'yes'):
            return [selection] + other_prs

    return [selection]
