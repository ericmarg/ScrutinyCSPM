from typing import List, Optional
from github import Github, Repository as GitHubRepo, GithubException
from github.AuthenticatedUser import AuthenticatedUser


class GitHubRepository:
    """
    Represents a GitHub repository.

    Args:
        repo_name (str): The name of the repository.
        access_token (str, optional): The access token for authentication. Defaults to None.
    """

    def __init__(self, repo_name: str, access_token: Optional[str] = None):
        if access_token:
            self.github = Github(access_token)
        else:
            self.github = Github()
        self.repo = self.github.get_repo(repo_name)

    @property
    def name(self) -> str:
        """
        Get the name of the repository.

        Returns:
            str: The name of the repository.
        """
        return self.repo.name

    @property
    def description(self) -> str:
        """
        Get the description of the repository.

        Returns:
            str: The description of the repository.
        """
        return self.repo.description

    @property
    def url(self) -> str:
        """
        Get the URL of the repository.

        Returns:
            str: The URL of the repository.
        """
        return self.repo.html_url

    @property
    def is_private(self) -> bool:
        """
        Check if the repository is private.

        Returns:
            bool: True if the repository is private, False otherwise.
        """
        return self.repo.private

    def get_branches(self) -> List[str]:
        """
        Get a list of branch names in the repository.

        Returns:
            List[str]: A list of branch names.
        """
        return [branch.name for branch in self.repo.get_branches()]

    def get_branch(self, branch_name) -> str:
        """
        Get a specific branch in the repository.

        Args:
            branch_name (str): The name of the branch.

        Returns:
            str: The branch object.
        """
        return self.repo.get_branch(branch_name)

    def get_commits(self, branch: str) -> List[str]:
        """
        Get a list of commit SHAs in a specific branch.

        Args:
            branch (str): The name of the branch.

        Returns:
            List[str]: A list of commit SHAs.
        """
        commits = self.repo.get_commits(sha=branch)
        return [commit.sha for commit in commits]

    def get_file_contents(self, file_path: str, branch: str) -> str:
        """
        Get the contents of a file in a specific branch.

        Args:
            file_path (str): The path of the file.
            branch (str): The name of the branch.

        Returns:
            str: The contents of the file.
        
        Raises:
            FileNotFoundError: If the file is not found in the branch.
            GithubException: If an error occurs while accessing the GitHub API.
        """
        try:
            contents = self.repo.get_contents(file_path, ref=branch)
            return contents.decoded_content.decode("utf-8")
        except GithubException as e:
            if e.status == 404:
                raise FileNotFoundError(
                    f"File '{file_path}' not found in branch '{branch}'."
                )
            else:
                raise e

    def get_files_by_extension(self, folder_path: str, file_extension: str) -> list:
        """
        Get a list of file paths with a specific file extension in a folder.

        Args:
            folder_path (str): The path of the folder.
            file_extension (str): The file extension.

        Returns:
            list: A list of file paths.

        Raises:
            GithubException: If an error occurs while accessing the GitHub API.
        """
        try:
            contents = self.repo.get_contents(folder_path)
            filtered_files = []

            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(self.repo.get_contents(file_content.path))
                elif file_content.type == "file" and file_content.path.endswith(
                    file_extension
                ):
                    filtered_files.append(file_content.path)

            return filtered_files

        except GithubException as e:
            print(f"Error: {e}")
            return []

    def create_branch(self, branch_name: str, source_branch) -> None:
        """
        Create a new branch in the repository.

        Args:
            branch_name (str): The name of the new branch.
            source_branch: The source branch to create the new branch from.

        Raises:
            PermissionError: If the access token is required to create a branch.
            GithubException: If an error occurs while accessing the GitHub API.

        Returns:
            None
        """
        try:
            user: AuthenticatedUser = self.github.get_user()
        except GithubException as e:
            if e.status == 401:
                raise PermissionError("Access token is required to create a branch.")
            else:
                raise e

        source_branch = self.repo.get_branch(self.repo.default_branch)
        self.repo.create_git_ref(
            ref=f"refs/heads/{branch_name}", sha=source_branch.commit.sha
        )

    def delete_branch(self, branch_name: str) -> None:
        """
        Deletes a branch from the GitHub repository.

        Args:
            branch_name (str): The name of the branch to be deleted.

        Raises:
            PermissionError: If the access token is required to delete a branch.
            GithubException: If an error occurs while accessing the GitHub API.

        Returns:
            None
        """
        try:
            user: AuthenticatedUser = self.github.get_user()
        except GithubException as e:
            if e.status == 401:
                raise PermissionError(
                    "Access token is required to delete a branch."
                )
            else:
                raise e

        # Get the branch object
        branch = self.repo.get_branch(branch_name)

        # Delete the branch using the GitHub API
        self.repo._requester.requestJsonAndCheck(
            "DELETE", self.repo.url + f"/git/refs/heads/{branch_name}"
        )

    def create_file(
        self, file_path: str, content: str, branch: str, commit_message: str
    ) -> None:
        """
        Create a new file in the repository.

        Args:
            file_path (str): The path of the new file.
            content (str): The content of the new file.
            branch (str): The name of the branch to create the file in.
            commit_message (str): The commit message for the file creation.

        Raises:
            PermissionError: If the access token is required to create a file.

        Returns:
            None
        """
        if not self.github.get_user().get_repo(self.repo.full_name):
            raise PermissionError("Access token is required to create a file.")
        self.repo.create_file(file_path, commit_message, content, branch=branch)

    def update_file(
        self, file_path: str, content: str, branch: str, commit_message: str
    ) -> None:
        """
        Update an existing file in the repository.

        Args:
            file_path (str): The path of the file to update.
            content (str): The new content of the file.
            branch (str): The name of the branch to update the file in.
            commit_message (str): The commit message for the file update.

        Raises:
            PermissionError: If the access token is required to update a file.

        Returns:
            None
        """
        if not self.github.get_user().get_repo(self.repo.full_name):
            raise PermissionError("Access token is required to update a file.")
        contents = self.repo.get_contents(file_path, ref=branch)
        self.repo.update_file(
            file_path, commit_message, content, contents.sha, branch=branch
        )

    def delete_file(self, file_path: str, branch: str, commit_message: str) -> None:
        """
        Delete an existing file from the repository.

        Args:
            file_path (str): The path of the file to delete.
            branch (str): The name of the branch to delete the file from.
            commit_message (str): The commit message for the file deletion.

        Raises:
            PermissionError: If the access token is required to delete a file.

        Returns:
            None
        """
        if not self.github.get_user().get_repo(self.repo.full_name):
            raise PermissionError("Access token is required to delete a file.")
        contents = self.repo.get_contents(file_path, ref=branch)
        self.repo.delete_file(file_path, commit_message, contents.sha, branch=branch)
