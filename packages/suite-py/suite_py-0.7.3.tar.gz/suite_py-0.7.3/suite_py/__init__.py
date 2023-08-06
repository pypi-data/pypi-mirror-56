from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals

import argparse

from .commands import merge_pr
from .commands import deploy
from .commands import create_branch
from .commands import open_pr
from .commands import lock_project
from .commands import ask_review

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", help="sub-command help")

parser_create_branch = subparsers.add_parser(
    "create-branch", help="Crea branch locale e imposta la card di YouTrack in progress")
parser_create_branch.add_argument(
    "--card", help="number of the card (ex. PRIMA-123)")

parser_lock_project = subparsers.add_parser(
    "lock-project", help="Lock/unlock dei merge sul branch master di un progetto")
parser_lock_project.add_argument(
    "action", choices=["lock", "l", "unlock", "u"])

parser_open_pr = subparsers.add_parser(
    "open-pr", help="Apre una PR su GitHub")

parser_ask_review = subparsers.add_parser(
    "ask-review", help="Chiede la review di una PR")

parser_merge_pr = subparsers.add_parser(
    "merge-pr", help="Merge del branch selezionato con master se tutti i check sono ok")

parser_deploy = subparsers.add_parser(
    "deploy", help="Deploy in produzione del branch master")


def dispatch(cmd_args):
    args = parser.parse_args(args=cmd_args)

    if(args.command == "create-branch"):
        return create_branch.entrypoint(args)
    elif(args.command == "deploy"):
        return deploy.entrypoint(args)
    elif(args.command == "merge-pr"):
        return merge_pr.entrypoint(args)
    elif(args.command == "open-pr"):
        return open_pr.entrypoint(args)
    elif(args.command == "lock-project"):
        return lock_project.entrypoint(args)
    elif(args.command == "ask-review"):
        return ask_review.entrypoint(args)
