from __future__ import absolute_import, annotations

import argparse
import logging
import os
import re
import subprocess
from typing import Optional

import gitlab
import requests

"""
This script is meant for managing releases.

* GitLab release creation.
* Release issuing in linked (by means of a GitLab topic) projects.

Requires:
- python-gitlab==3.1.1
- requests==2.27.1

## GitLab release creation.

    It supporting the automatic definition of GitLab releases upon the creation of a new git tag.
    
    Allowed tags should satisfy the regex `([0-9]+).([0-9]+).([0-9]+)([a-zA-Z.\-]+)?`.
    The supported structure is therefore the one of the semantic versioning (e.g. `1.2.3.`, `1.2.3-rc`).
    
    The script expects the existence of a milestone that should be correctly named {major}.{minor} (e.g. `1.2`).
    
## Release issuing 

    It is possible by creating a new issue dedicated to the release for each linked project. 
    Older issues associated to the same project will be commented upon and closed.
    
    The project needs to be identified by a specific and unique GitLab topic.
    Each linked project needs to be associated with the project GitLab topic. 
"""


class Release:

    @staticmethod
    def read_from_changelog():
        logging.debug("Extracting release description from CHANGELOG.md file.")
        pipe = subprocess.PIPE
        git_process = subprocess.Popen([
            'awk',
            'flag{ if (/### /){printf "%s", buf; flag=0; buf=""} else buf = buf $0 ORS}; /### ' + release_tag + '/{flag=1}',
            "CHANGELOG.md"
        ], stdout=pipe, stderr=pipe)
        std_output, std_error_output = git_process.communicate()

        error = std_error_output.decode("utf-8")
        if error != "":
            logging.error(f"Could not get release description. Cause: {error}.")
            exit(1)

        return std_output.decode("utf-8")


class Version:

    def __init__(self, major: int, minor: int, patch: int, other: Optional[str] = None) -> None:
        self.major = major
        self.minor = minor
        self.patch = patch
        self.other = other

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    @staticmethod
    def build(raw_version: str) -> Version:
        result = re.search("([0-9]+).([0-9]+).([0-9]+)([a-zA-Z.\-]+)?", raw_version)
        if result:
            return Version(
                int(result.group(1)),
                int(result.group(2)),
                int(result.group(3)),
                other=result.group(4),
            )
        else:
            raise ValueError(f"Can not build version from [{raw_version}].")

    def label(self, with_minor: bool = True, with_context: bool = True) -> str:
        result = f"{self.major}.{self.minor}"
        if with_minor:
            result += f".{self.minor}"
            if with_context and self.other:
                result += f"{self.other}"
        return result

    @property
    def is_final(self) -> bool:
        """
        A version is considered `final` when its structure satisfies `{major}.{minor}.{patch}`.

        A different structure (this happens when the attribute `other` is set) usually defines
        a work in progress version.

        :return: Whether the version is final or not.
        """
        return self.other is None


def version_blocker(release_tag: str, allow_non_final_version: bool) -> Version:
    try:
        version = Version.build(release_tag)
        # In the context of this script, there is no interest in creating releases for work in
        # progress versions.
        if not allow_non_final_version and not version.is_final:
            logging.info(f"Target version [{version.label}] is not meant to be issued.")
            exit(1)
        return version
    except ValueError as e:
        logging.error(f"The structure of the tag [{release_tag}] does not support a release.", exc_info=e)
        exit(1)


if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(description="Release manager.")
    sub_parsers = arg_parser.add_subparsers(dest="command")

    arg_parser.add_argument("-t", "--api_token", type=str, default=os.getenv("CI_JOB_TOKEN"), help="The GitLab api token. Allows configuration via CI_JOB_TOKEN env variable.")
    arg_parser.add_argument("-r", "--release_tag", type=str, default=os.getenv("CI_COMMIT_TAG"), help="The GitLab tag. Allows configuration via CI_COMMIT_TAG env variable.")
    arg_parser.add_argument("-g", "--gitlab_url", type=str, default="https://lab.u-hopper.com", help="The GitLab instance url.")

    arg_parser.add_argument("--log", type=str, default=os.getenv("LOG_LEVEL", "INFO"), help="Log level. Allows configuration via LOG_LEVEL env variable. Default INFO.")
    arg_parser.add_argument("--dry_run", action="store_true", help="Run test dry-run without applying any changes.")

    create_release_parser = sub_parsers.add_parser("create", help='Create a new GitLab release.')
    create_release_parser.add_argument("-i", "--project_id", type=str, default=os.getenv("CI_PROJECT_ID"), help="The project id. Allows configuration via CI_PROJECT_ID env variable.")
    create_release_parser.add_argument("-d", "--release_description", type=str, default=os.getenv("RELEASE_DESCRIPTION", None), help="The release description. Allows configuration via RELEASE_DESCRIPTION env variable. Default None.")
    create_release_parser.add_argument("--allow_non_final_version", action="store_true", help="Allow the creation of a release based on a non final version.")

    issue_release_parser = sub_parsers.add_parser("issue", help='Issue a release to all the linked projects.')
    issue_release_parser.add_argument("-n", "--project_name", type=str, default=os.getenv("CI_PROJECT_TITLE"), help="The project name. Allows configuration via CI_PROJECT_TITLE env variable.")
    issue_release_parser.add_argument("-u", "--project_url", type=str, default=os.getenv("CI_PROJECT_URL"), help="The project name. Allows configuration via CI_PROJECT_URL env variable.")
    issue_release_parser.add_argument("-tp", "--gitlab_topic", type=str, help="The GitLab topic that identifies all other projects that should be notified of the new release.")

    slack_notify_release_parser = sub_parsers.add_parser("slack", help='Notify release in Slack.')
    slack_notify_release_parser.add_argument("-n", "--project_name", type=str, default=os.getenv("CI_PROJECT_TITLE"), help="The project name. Allows configuration via CI_PROJECT_TITLE env variable.")
    slack_notify_release_parser.add_argument("-u", "--project_url", type=str, default=os.getenv("CI_PROJECT_URL"), help="The project name. Allows configuration via CI_PROJECT_URL env variable.")
    slack_notify_release_parser.add_argument("-d", "--release_description", type=str, default=os.getenv("RELEASE_DESCRIPTION", None), help="The release description. Allows configuration via RELEASE_DESCRIPTION env variable. Default None.")
    slack_notify_release_parser.add_argument("-s", "--slack_webhook", type=str, default=os.getenv("SLACK_WEBHOOK", None), help="The Slack webhook where the notification should be sent. Allows configuration via SLACK_WEBHOOK env variable. Default None.")
    slack_notify_release_parser.add_argument("--allow_non_final_version", action="store_true", help="Allow the creation of a release based on a non final version.")

    args = arg_parser.parse_args()

    logging.basicConfig(level=args.log.upper())

    release_tag = args.release_tag
    dry_run = args.dry_run
    if dry_run:
        logging.info("Running in dry-run mode.")

    if args.command == "create":
        logging.info(f"Creating new release for tag {release_tag}.")

        project_id = args.project_id
        if not project_id:
            raise ValueError("Argument project_id is required.")
        release_description = args.release_description

        if not release_description:
            release_description = Release.read_from_changelog()

        version = version_blocker(release_tag, args.allow_non_final_version)

        gl = gitlab.Gitlab(args.gitlab_url, private_token=args.api_token)

        project = gl.projects.get(project_id, lazy=True)
        release_details = {
            "name": release_tag,
            "tag_name": release_tag,
            "description": release_description,
            "milestones": [
                version.label(with_minor=False)
            ]
        }

        logging.debug(f"New release ready to be created: {release_details}")
        if not dry_run:
            release = project.releases.create(release_details)
        logging.info(f"New release [{release_tag}] correctly created.")

    elif args.command == "issue":
        logging.info(f"Issuing new release [{release_tag}].")

        version_blocker(release_tag, False)

        gitlab_topic = args.gitlab_topic
        project_name = args.project_name
        project_url = args.project_url

        gl = gitlab.Gitlab(args.gitlab_url, private_token=args.api_token)

        target_projects = gl.projects.list(topic=gitlab_topic, all=True)
        for target_project in target_projects:
            logging.debug(f"Notifying release issue for project [{target_project.id}].")

            # Create the new issue regarding the target release.
            description = f"A new release [{release_tag}]({project_url}/-/releases/{release_tag}) is available for [{project_name}]({project_url}). You may want to update to get the latest functionalities."
            issue_description = {
                "title": f"Update to {project_name} version {release_tag}",
                "description": description,
                "labels": ["support"],
            }
            logging.debug(f"New issue ready to be created: {issue_description}.")
            if not dry_run:
                new_issue = target_project.issues.create(issue_description)
                logging.debug(f"New issue [{new_issue.id}] for release [{release_tag}] and project [{project_name}] created.")

                # Closing older issues that are still open.
                open_issues = target_project.issues.list(state="opened")
                for issue in open_issues:
                    if f"Update to {project_name} version" in issue.title and issue.iid != new_issue.iid:
                        logging.debug(f"Issue {issue.iid} represents an older release of project [{project_name}]: it should be closed.")
                        # Comment on the issue about new available version.
                        issue.notes.create({"body": f"A newer version [{release_tag}]({project_url}/-/releases/{release_tag}) has been released (details are available in #{new_issue.iid}). I am closing this issue."})
                        # Close the issue.
                        issue.state_event = "close"
                        issue.save()

    elif args.command == "slack":
        logging.info(f"Notifying on Slack new release [{release_tag}].")
        version = version_blocker(release_tag, args.allow_non_final_version)

        slack_webhook = args.slack_webhook
        if not slack_webhook:
            logging.error("Can not notify release. Slack webhook is not configured.")
            exit(1)

        project_url = args.project_url
        project_name = args.project_name
        if not project_url or not project_name:
            logging.error("Required arguments [project_url, project_name] are missing.")
            exit(1)

        def _adjust_links(matches):
            return f"<{matches.group(2)}|{matches.group(1)}>"

        release_description = args.release_description
        if not release_description:
            release_description = Release.read_from_changelog()
        release_description = release_description.replace("\n-", "\n•").replace("\n*", "\n•")
        release_description = re.sub("\[(.*?)\]\((.*?)\)", _adjust_links, release_description)

        body = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"A new release <{project_url}/-/releases/{release_tag}|{release_tag}> has just been created for <{project_url}|{project_name}> :unicorn_face:"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": release_description
                    }
                }
            ]
        }
        requests.post(slack_webhook, json=body)

    else:
        logging.error(f"Unknown command [{args.command}].")
        exit(1)
