from typing import Protocol, List

class Repository(Protocol):
    @property
    def name(self) -> str:
        """The name of the repository."""
        ...

    @property
    def description(self) -> str:
        """The description of the repository."""
        ...

    @property
    def url(self) -> str:
        """The URL of the repository."""
        ...

    @property
    def is_private(self) -> bool:
        """Indicates whether the repository is private or public."""
        ...

    def get_branches(self) -> List[str]:
        """Retrieves a list of branch names in the repository."""
        ...

    def get_commits(self, branch: str) -> List[str]:
        """Retrieves a list of commit SHAs for the specified branch."""
        ...

    def get_file_contents(self, file_path: str, branch: str) -> str:
        """Retrieves the contents of a file in the repository."""
        ...

    def create_branch(self, branch_name: str) -> None:
        """Creates a new branch in the repository."""
        ...

    def create_file(self, file_path: str, content: str, branch: str, commit_message: str) -> None:
        """Creates a new file in the repository."""
        ...

    def update_file(self, file_path: str, content: str, branch: str, commit_message: str) -> None:
        """Updates an existing file in the repository."""
        ...

    def delete_file(self, file_path: str, branch: str, commit_message: str) -> None:
        """Deletes a file from the repository."""
        ...