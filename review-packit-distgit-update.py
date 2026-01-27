"""
Find dist-git updates of Packit projects and review them.
"""

import os
import ogr
from ogr.abstract.status import PRStatus

fedora_distgit_url = "https://src.fedoraproject.org"
fedora_distgit_service = ogr.PagureService(token=os.getenv("FEDORA_DISTGIT_TOKEN"), instance_url=fedora_distgit_url)

def main():
    fedora_distgit_project = fedora_distgit_service.get_project(namespace="rpms", repo="packit")
    # TODO: project.get_branches()
    for branch in get_dist_git_branches():
        for pr in fedora_distgit_project.get_pr_list(status=PRStatus.merged)[:3]:
            print_pr_info(pr)

def print_pr_info(pr):
    print(f"PR {pr.id}: {pr.title}\n{pr.description}\nFile diff: {pr.patch}")

def get_dist_git_branches():
    return ["rawhide", "f42", "f43"]

if __name__ == "__main__":
    main()