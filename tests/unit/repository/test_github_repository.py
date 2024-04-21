import unittest
import uuid
from github import (
    Github,
    Repository as GitHubRepo,
    GithubException,
    Branch,
    Commit,
    ContentFile,
)
from hydra.core.global_hydra import GlobalHydra
import hydra
from src.scrutinycspm.access.repository.github_provider import GitHubRepository
from typing import List

from tests.unit.base_test_case import BaseTestCase

class TestGitHubRepository(BaseTestCase):

    def setUp(self):
        
        super().setUp(config_path="../../conf", config_name="vault")        

        # Get the repository name and access token from the configuration
        self.repo_name = self.cfg_secure.repositories.github.repository
        self.access_token = self.cfg_secure.repositories.github.token
        # Create an instance of the GitHubRepository class
        self.repo = GitHubRepository(self.repo_name, self.access_token)
        

    def test_name(self):
        self.assertTrue(self.repo.name == "snarfswap")

    def test_description(self):
        self.assertIsNone(self.repo.description)

    def test_url(self):
        url = f"https://github.com/{self.cfg_secure.repositories.github.repository}"
        self.assertEqual(self.repo.url, url)

    def test_is_private(self):
        self.assertFalse(self.repo.is_private)

    @unittest.expectedFailure
    def test_get_branches(self):

        branches: List[str] = self.repo.get_branches
        self.assertEqual(self.repo.get_branches(), ["branch1", "branch2", 'main', 'robertfischer3-patch-2', 'robertfischer3-patch-2'])

    def test_get_commits(self):
        # this test will fail if the number of commits in the main branch is not 8
        # this a brittle test that will fail if the number of commits in the main branch changes
        # needs 
        self.assertEqual(len(self.repo.get_commits("main")), 8)

    def test_get_file_contents(self):
        """
        Test case for the `get_file_contents` method of the GitHubRepository class.
        """
        # Get the contents of a file from the GitHub repository
        contents: str = self.repo.get_file_contents(self.cfg.testing.github.file_to_test, "main")
        
        # Check if the contents start with the expected string
        self.assertTrue(contents.startswith("use secp256k1;"))

    def test_get_file_contents_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.repo.get_file_contents("nonexistent.txt", "main")

    
    def test_create_branch(self):
        """
        Test case for creating a branch in a GitHub repository.

        This test generates a unique branch name using UUID, creates the branch in the repository,
        and then checks if the branch exists in the list of branches. Finally, it deletes the branch
        and verifies that the branch no longer exists in the list of branches.
        """

        # Generate a unique branch name using UUID
        unique_branch_name:str = f"test-branch-{uuid.uuid4()}"

        # Create the branch in the repository
        self.repo.create_branch(unique_branch_name, "main")

        # Check if the branch exists in the list of branches
        self.assertIn(unique_branch_name, self.repo.get_branches())

        # Delete the branch
        self.repo.delete_branch(unique_branch_name)

        # Verify that the branch no longer exists in the list of branches
        self.assertNotIn(unique_branch_name, self.repo.get_branches())


if __name__ == "__main__":
    unittest.main()
