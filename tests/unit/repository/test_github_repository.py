import unittest
from unittest.mock import MagicMock, patch
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
        branches = [MagicMock(name="branch1"), MagicMock(name="branch2")]
        self.repo.repo = MagicMock()
        self.repo.repo.get_branches.return_value = branches
        self.assertEqual(self.repo.get_branches(), ["branch1", "branch2"])

    def test_get_commits(self):
        commits = [MagicMock(sha="commit1"), MagicMock(sha="commit2")]
        self.repo.repo = MagicMock()
        self.repo.repo.get_commits.return_value = commits
        self.assertEqual(self.repo.get_commits("main"), ["commit1", "commit2"])

    def test_get_file_contents(self):
        content_file = MagicMock(decoded_content=b"Hello, World!")
        self.repo.repo = MagicMock()
        self.repo.repo.get_contents.return_value = content_file
        self.assertEqual(
            self.repo.get_file_contents("README.md", "main"), "Hello, World!"
        )

    def test_get_file_contents_file_not_found(self):
        self.repo.repo = MagicMock()
        self.repo.repo.get_contents.side_effect = GithubException(404, "File not found")
        with self.assertRaises(FileNotFoundError):
            self.repo.get_file_contents("nonexistent.txt", "main")

    @patch("github.AuthenticatedUser.AuthenticatedUser.has_in_repos")
    def test_create_branch(self, mock_has_in_repos):
        mock_has_in_repos.return_value = True
        self.repo.repo = MagicMock()
        self.repo.repo.get_branch.return_value = MagicMock(
            commit=MagicMock(sha="commit_sha")
        )
        self.repo.create_branch("new-branch")
        self.repo.repo.create_git_ref.assert_called_once_with(
            ref="refs/heads/new-branch", sha="commit_sha"
        )

    @patch("github.AuthenticatedUser.AuthenticatedUser.has_in_repos")
    def test_create_branch_permission_error(self, mock_has_in_repos):
        mock_has_in_repos.return_value = False
        with self.assertRaises(PermissionError):
            self.repo.create_branch("new-branch")


if __name__ == "__main__":
    unittest.main()
