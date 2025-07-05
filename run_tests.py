#!/usr/bin/env python3
"""
Test runner script for E-CLARIA AI project.

This script provides various options for running tests including:
- Unit tests
- Integration tests
- All tests
- Coverage reporting
- Performance tests
- Test discovery

Requirements:
    - Python 3.12+
    - Docker and Docker Compose (for containerized testing)

Usage:
    python run_tests.py                 # Run all tests
    python run_tests.py --unit          # Run only unit tests
    python run_tests.py --integration   # Run only integration tests
    python run_tests.py --coverage      # Run tests with coverage
    python run_tests.py --performance   # Run performance tests
    python run_tests.py --markers auth  # Run tests with specific markers
    python run_tests.py --verbose       # Run with verbose output
    python run_tests.py --parallel      # Run tests in parallel
    python run_tests.py --fast          # Run tests quickly (skip slow tests)
"""

import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional


class TestRunner:
    """Test runner for E-CLARIA AI project."""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.tests_dir = self.project_root / "tests"
        self.coverage_dir = self.project_root / "htmlcov"
        self.reports_dir = self.project_root / "test_reports"

    def setup_test_environment(self):
        """Set up test environment variables."""
        test_env = os.environ.copy()
        test_env.update({
            'TESTING': 'true',
            'DATABASE_URL': 'sqlite:///test.db',
            'GROQ_API_KEY': 'test-key',
            'LLAMA_MODEL': 'llama3-8b-8192',
            'PYTHONPATH': str(self.project_root),
        })
        return test_env

    def clean_test_artifacts(self):
        """Clean up test artifacts."""
        artifacts = [
            self.project_root / "test.db",
            self.project_root / ".coverage",
            self.coverage_dir,
            self.project_root / ".pytest_cache",
            self.project_root / "junit.xml",
        ]

        for artifact in artifacts:
            if artifact.exists():
                if artifact.is_file():
                    artifact.unlink()
                elif artifact.is_dir():
                    shutil.rmtree(artifact)

    def ensure_directories(self):
        """Ensure required directories exist."""
        self.reports_dir.mkdir(exist_ok=True)

    def run_command(self, cmd: List[str], env: Optional[dict] = None) -> int:
        """Run a command and return the exit code."""
        env = env or self.setup_test_environment()

        print(f"Running: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, env=env, cwd=self.project_root)
            return result.returncode
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}")
            return e.returncode
        except FileNotFoundError:
            print(f"Command not found: {cmd[0]}")
            return 1

    def run_unit_tests(self, verbose: bool = False, parallel: bool = False) -> int:
        """Run unit tests."""
        cmd = ["python", "-m", "pytest", "tests/unit/", "-m", "unit"]

        if verbose:
            cmd.append("-v")

        if parallel:
            cmd.extend(["-n", "auto"])

        cmd.extend([
            "--tb=short",
            "--strict-markers",
            "--disable-warnings"
        ])

        return self.run_command(cmd)

    def run_integration_tests(self, verbose: bool = False, parallel: bool = False) -> int:
        """Run integration tests."""
        cmd = ["python", "-m", "pytest", "tests/integration/", "-m", "integration"]

        if verbose:
            cmd.append("-v")

        if parallel:
            cmd.extend(["-n", "auto"])

        cmd.extend([
            "--tb=short",
            "--strict-markers",
            "--disable-warnings"
        ])

        return self.run_command(cmd)

    def run_all_tests(self, verbose: bool = False, parallel: bool = False, fast: bool = False) -> int:
        """Run all tests."""
        cmd = ["python", "-m", "pytest", "tests/"]

        if verbose:
            cmd.append("-v")

        if parallel:
            cmd.extend(["-n", "auto"])

        if fast:
            cmd.extend(["-m", "not slow"])

        cmd.extend([
            "--tb=short",
            "--strict-markers",
            "--disable-warnings"
        ])

        return self.run_command(cmd)

    def run_tests_with_coverage(self, verbose: bool = False) -> int:
        """Run tests with coverage reporting."""
        cmd = [
            "python", "-m", "pytest", "tests/",
            "--cov=app",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-report=xml",
            "--cov-fail-under=80"
        ]

        if verbose:
            cmd.append("-v")

        cmd.extend([
            "--tb=short",
            "--strict-markers",
            "--disable-warnings"
        ])

        result = self.run_command(cmd)

        if result == 0:
            print(f"\nCoverage report generated in: {self.coverage_dir}")

        return result

    def run_performance_tests(self, verbose: bool = False) -> int:
        """Run performance tests."""
        cmd = [
            "python", "-m", "pytest", "tests/",
            "-m", "performance",
            "--benchmark-only",
            "--benchmark-sort=mean"
        ]

        if verbose:
            cmd.append("-v")

        return self.run_command(cmd)

    def run_tests_with_markers(self, markers: List[str], verbose: bool = False) -> int:
        """Run tests with specific markers."""
        cmd = ["python", "-m", "pytest", "tests/"]

        if len(markers) == 1:
            cmd.extend(["-m", markers[0]])
        else:
            marker_expression = " or ".join(markers)
            cmd.extend(["-m", marker_expression])

        if verbose:
            cmd.append("-v")

        cmd.extend([
            "--tb=short",
            "--strict-markers",
            "--disable-warnings"
        ])

        return self.run_command(cmd)

    def run_tests_with_reports(self, verbose: bool = False) -> int:
        """Run tests with detailed reporting."""
        self.ensure_directories()

        cmd = [
            "python", "-m", "pytest", "tests/",
            "--html=test_reports/report.html",
            "--self-contained-html",
            "--junit-xml=test_reports/junit.xml",
            "--cov=app",
            "--cov-report=html:test_reports/coverage",
            "--cov-report=xml:test_reports/coverage.xml"
        ]

        if verbose:
            cmd.append("-v")

        cmd.extend([
            "--tb=short",
            "--strict-markers",
            "--disable-warnings"
        ])

        result = self.run_command(cmd)

        if result == 0:
            print(f"\nTest reports generated in: {self.reports_dir}")

        return result

    def lint_code(self) -> int:
        """Run code linting."""
        print("Running code linting...")

        # Run flake8
        flake8_result = self.run_command([
            "python", "-m", "flake8", "app/", "tests/",
            "--max-line-length=88",
            "--extend-ignore=E203,W503"
        ])

        # Run black check
        black_result = self.run_command([
            "python", "-m", "black", "--check", "app/", "tests/"
        ])

        # Run isort check
        isort_result = self.run_command([
            "python", "-m", "isort", "--check-only", "app/", "tests/"
        ])

        return max(flake8_result, black_result, isort_result)

    def format_code(self) -> int:
        """Format code with black and isort."""
        print("Formatting code...")

        # Run black
        black_result = self.run_command([
            "python", "-m", "black", "app/", "tests/"
        ])

        # Run isort
        isort_result = self.run_command([
            "python", "-m", "isort", "app/", "tests/"
        ])

        return max(black_result, isort_result)

    def security_check(self) -> int:
        """Run security checks."""
        print("Running security checks...")

        # Run bandit
        bandit_result = self.run_command([
            "python", "-m", "bandit", "-r", "app/", "-f", "json",
            "-o", "test_reports/bandit.json"
        ])

        # Run safety
        safety_result = self.run_command([
            "python", "-m", "safety", "check", "--json",
            "--output", "test_reports/safety.json"
        ])

        return max(bandit_result, safety_result)

    def discover_tests(self) -> int:
        """Discover and list all tests."""
        cmd = [
            "python", "-m", "pytest", "tests/", "--collect-only", "-q"
        ]

        return self.run_command(cmd)

    def run_docker_tests(self) -> int:
        """Run tests in Docker environment."""
        print("Running tests in Docker...")

        # Build test image
        build_result = self.run_command([
            "docker-compose", "build", "test"
        ])

        if build_result != 0:
            return build_result

        # Run tests in container
        return self.run_command([
            "docker-compose", "run", "--rm", "test"
        ])


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Test runner for E-CLARIA AI project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Test type arguments
    parser.add_argument(
        "--unit", action="store_true",
        help="Run only unit tests"
    )
    parser.add_argument(
        "--integration", action="store_true",
        help="Run only integration tests"
    )
    parser.add_argument(
        "--performance", action="store_true",
        help="Run performance tests"
    )
    parser.add_argument(
        "--markers", nargs="+",
        help="Run tests with specific markers"
    )

    # Test options
    parser.add_argument(
        "--coverage", action="store_true",
        help="Run tests with coverage reporting"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Run with verbose output"
    )
    parser.add_argument(
        "--parallel", "-n", action="store_true",
        help="Run tests in parallel"
    )
    parser.add_argument(
        "--fast", action="store_true",
        help="Run tests quickly (skip slow tests)"
    )
    parser.add_argument(
        "--reports", action="store_true",
        help="Generate detailed test reports"
    )

    # Code quality arguments
    parser.add_argument(
        "--lint", action="store_true",
        help="Run code linting"
    )
    parser.add_argument(
        "--format", action="store_true",
        help="Format code with black and isort"
    )
    parser.add_argument(
        "--security", action="store_true",
        help="Run security checks"
    )

    # Other arguments
    parser.add_argument(
        "--discover", action="store_true",
        help="Discover and list all tests"
    )
    parser.add_argument(
        "--docker", action="store_true",
        help="Run tests in Docker environment"
    )
    parser.add_argument(
        "--clean", action="store_true",
        help="Clean test artifacts before running"
    )

    args = parser.parse_args()

    # Create test runner
    runner = TestRunner()

    # Clean artifacts if requested
    if args.clean:
        print("Cleaning test artifacts...")
        runner.clean_test_artifacts()

    # Determine what to run
    exit_code = 0

    if args.docker:
        exit_code = runner.run_docker_tests()
    elif args.discover:
        exit_code = runner.discover_tests()
    elif args.lint:
        exit_code = runner.lint_code()
    elif args.format:
        exit_code = runner.format_code()
    elif args.security:
        exit_code = runner.security_check()
    elif args.unit:
        exit_code = runner.run_unit_tests(args.verbose, args.parallel)
    elif args.integration:
        exit_code = runner.run_integration_tests(args.verbose, args.parallel)
    elif args.performance:
        exit_code = runner.run_performance_tests(args.verbose)
    elif args.markers:
        exit_code = runner.run_tests_with_markers(args.markers, args.verbose)
    elif args.coverage:
        exit_code = runner.run_tests_with_coverage(args.verbose)
    elif args.reports:
        exit_code = runner.run_tests_with_reports(args.verbose)
    else:
        # Default: run all tests
        exit_code = runner.run_all_tests(args.verbose, args.parallel, args.fast)

    # Exit with appropriate code
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
