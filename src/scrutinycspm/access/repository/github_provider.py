from typing import List
from github import Github, Repository as GitHubRepo, GithubException

class GitHubRepository:
    def __init__(self, access_token: str, repo_name: str):
        self.github = Github(access_token)
        self.repo = self.github.get_repo(repo_name)

    @property
    def name(self) -> str:
        return self.repo.name

    @property
    def description(self) -> str:
        return self.repo.description

    @property
    def url(self) -> str:
        return self.repo.html_url

    @property
    def is_private(self) -> bool:
        return self.repo.private

    def get_branches(self) -> List[str]:
        return [branch.name for branch in self.repo.get_branches()]

    def get_commits(self, branch: str) -> List[str]:
        commits = self.repo.get_commits(sha=branch)
        return [commit.sha for commit in commits]

    def get_file_contents(self, file_path: str, branch: str) -> str:
        try:
            contents = self.repo.get_contents(file_path, ref=branch)
            return contents.decoded_content.decode("utf-8")
        except GithubException as e:
            if e.status == 404:
                raise FileNotFoundError(f"File '{file_path}' not found in branch '{branch}'.")
            else:
                raise e

    def create_branch(self, branch_name: str) -> None:
        source_branch = self.repo.get_branch(self.repo.default_branch)
        self.repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source_branch.commit.sha)

    def create_file(self, file_path: str, content: str, branch: str, commit_message: str) -> None:
        self.repo.create_file(file_path, commit_message, content, branch=branch)

    def update_file(self, file_path: str, content: str, branch: str, commit_message: str) -> None:
        contents = self.repo.get_contents(file_path, ref=branch)
        self.repo.update_file(file_path, commit_message, content, contents.sha, branch=branch)

    def delete_file(self, file_path: str, branch: str, commit_message: str) -> None:
        contents = self.repo.get_contents(file_path, ref=branch)
        self.repo.delete_file(file_path, commit_message, contents.sha, branch=branch)