import unittest
from unittest.mock import MagicMock, patch
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

class TestGitHubRepository(unittest.TestCase):

    def setUp(self):
        GlobalHydra.instance().clear()
        hydra.initialize(
            config_path="../../../conf", job_name="test_job", version_base="1.1"
        )
        self.cfg = hydra.compose(config_name="vault")

        private_vault_config = self.cfg.private_path

        GlobalHydra.instance().clear()
        hydra.initialize(
            config_path=private_vault_config, job_name="test_job_2", version_base="1.1"
        )
        self.cfg_secure = hydra.compose(config_name="private_vault")

        self.repo_name = self.cfg_secure.repositories.github.repository
        self.access_token = self.cfg_secure.repositories.github.token
        self.repo = GitHubRepository(self.repo_name, self.access_token)
        

    def test_name(self):

        self.assertEqual(self.repo.name == "snarfswap")

    def test_description(self):
        
        self.assertIsNone(self.repo.description)

    def test_url(self):
        url = f"https://github.com/{self.cfg_secure.repositories.github.repository}"
        self.assertEqual(self.repo.url, url)

    def test_is_private(self):
        self.assertFalse(self.repo.is_private)

    def test_get_branches(self):

        branches: List[str] = self.repo.get_branches
        self.assertEqual(self.repo.get_branches(), ["branch1", "branch2", 'main', 'robertfischer3-patch-1'])

    def test_get_commits(self):

        self.repo.get_commits
        self.assertEqual(self.repo.get_commits("main"), self.cfg.testing.github.commits)

    def test_get_file_contents(self):

        contents: str = self.repo.get_file_contents(self.cfg.testing.github.file_to_test, "main")
        self.assertTrue(contents.startswith("use secp256k1;"))

    def test_get_file_contents_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.repo.get_file_contents("nonexistent.txt", "main")

    
    def test_create_branch(self):
        # Generate a unique branch name using UUID
        unique_branch_name:str = f"test-branch-{uuid.uuid4()}"
        self.repo.create_branch(unique_branch_name, "main")
        
        self.assertIn(unique_branch_name, self.repo.get_branches())

        self.repo.delete_branch(unique_branch_name)
        self.assertNotIn(unique_branch_name, self.repo.get_branches())


if __name__ == "__main__":
    unittest.main()
