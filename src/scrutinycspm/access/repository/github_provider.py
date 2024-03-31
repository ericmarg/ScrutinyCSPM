from typing import List, Optional
from github import Github, Repository as GitHubRepo, GithubException
from github.AuthenticatedUser import AuthenticatedUser

class GitHubRepository:
    def __init__(self, repo_name: str, access_token: Optional[str] = None):
        if access_token:
            self.github = Github(access_token)
        else:
            self.github = Github()
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
    
    def get_branch(self, branch_name) -> str:    
        self.repo.get_branch(branch_name)


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

    def get_files_by_extension(self, folder_path: str, file_extension: str) -> list:
        try:
            contents = self.repo.get_contents(folder_path)
            filtered_files = []

            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(self.repo.get_contents(file_content.path))
                elif file_content.type == "file" and file_content.path.endswith(file_extension):
                    filtered_files.append(file_content.path)

            return filtered_files

        except GithubException as e:
            print(f"Error: {e}")
            return []
        
    def create_branch(self, branch_name: str, source_branch) -> None:
        try:
            user: AuthenticatedUser = self.github.get_user()
        except GithubException as e:
            if e.status == 401:
                raise PermissionError("Access token is required to create a branch.")
            else:
                raise e
        
        source_branch = self.repo.get_branch(self.repo.default_branch)
        self.repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source_branch.commit.sha)

    def delete_branch(self, branch_name: str) -> None:
        try:
            user: AuthenticatedUser = self.github.get_user()
        except GithubException as e:
            if e.status == 401:
                raise PermissionError("Access token is required to delete a branch.")
            else:
                raise e
        
        branch = self.repo.get_branch(branch_name)
        self.repo._requester.requestJsonAndCheck(
            "DELETE",
            self.repo.url + f"/git/refs/heads/{branch_name}"
        )

    def create_file(self, file_path: str, content: str, branch: str, commit_message: str) -> None:
        if not self.github.get_user().get_repo(self.repo.full_name):
            raise PermissionError("Access token is required to create a file.")
        self.repo.create_file(file_path, commit_message, content, branch=branch)

    def update_file(self, file_path: str, content: str, branch: str, commit_message: str) -> None:
        if not self.github.get_user().get_repo(self.repo.full_name):
            raise PermissionError("Access token is required to update a file.")
        contents = self.repo.get_contents(file_path, ref=branch)
        self.repo.update_file(file_path, commit_message, content, contents.sha, branch=branch)

    def delete_file(self, file_path: str, branch: str, commit_message: str) -> None:
        if not self.github.get_user().get_repo(self.repo.full_name):
            raise PermissionError("Access token is required to delete a file.")
        contents = self.repo.get_contents(file_path, ref=branch)
        self.repo.delete_file(file_path, commit_message, contents.sha, branch=branch)