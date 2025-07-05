#!/usr/bin/env python3
"""
Python version verification script for E-CLARIA AI project.

This script verifies that Python 3.12+ is being used and checks
compatibility with the project's dependencies.
"""

import sys
import platform
import subprocess
import importlib.util


def check_python_version():
    """Check if Python version is 3.12 or higher."""
    required_version = (3, 12)
    current_version = sys.version_info[:2]

    print(f"Python version: {platform.python_version()}")
    print(f"Python executable: {sys.executable}")
    print(f"Platform: {platform.platform()}")

    if current_version >= required_version:
        print(f"✅ Python {current_version[0]}.{current_version[1]} meets requirement (3.12+)")
        return True
    else:
        print(f"❌ Python {current_version[0]}.{current_version[1]} does not meet requirement (3.12+)")
        return False


def check_required_packages():
    """Check if required packages can be imported."""
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pydantic',
        'passlib',
        'python_dotenv',
        'psycopg2',
        'bcrypt',
        'openai'
    ]

    missing_packages = []
    available_packages = []

    for package in required_packages:
        try:
            # Handle special cases for package names
            import_name = package
            if package == 'python_dotenv':
                import_name = 'dotenv'
            elif package == 'psycopg2':
                import_name = 'psycopg2'

            spec = importlib.util.find_spec(import_name)
            if spec is not None:
                available_packages.append(package)
            else:
                missing_packages.append(package)
        except ImportError:
            missing_packages.append(package)

    print(f"\n📦 Package availability:")
    for package in available_packages:
        print(f"  ✅ {package}")

    if missing_packages:
        print(f"\n❌ Missing packages:")
        for package in missing_packages:
            print(f"  ❌ {package}")
        return False
    else:
        print(f"\n✅ All required packages are available")
        return True


def check_docker_availability():
    """Check if Docker is available."""
    try:
        result = subprocess.run(
            ['docker', '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(f"✅ Docker: {result.stdout.strip()}")

            # Check Docker Compose
            compose_result = subprocess.run(
                ['docker-compose', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if compose_result.returncode == 0:
                print(f"✅ Docker Compose: {compose_result.stdout.strip()}")
                return True
            else:
                print(f"❌ Docker Compose not available")
                return False
        else:
            print(f"❌ Docker not available")
            return False
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        print(f"❌ Docker not available")
        return False


def check_test_dependencies():
    """Check if test dependencies are available."""
    test_packages = [
        'pytest',
        'pytest_cov',
        'pytest_mock',
        'pytest_asyncio',
        'httpx'
    ]

    missing_test_packages = []
    available_test_packages = []

    for package in test_packages:
        try:
            spec = importlib.util.find_spec(package)
            if spec is not None:
                available_test_packages.append(package)
            else:
                missing_test_packages.append(package)
        except ImportError:
            missing_test_packages.append(package)

    print(f"\n🧪 Test dependencies:")
    for package in available_test_packages:
        print(f"  ✅ {package}")

    if missing_test_packages:
        print(f"\n⚠️  Missing test packages (install with: pip install -r requirements-test.txt):")
        for package in missing_test_packages:
            print(f"  ❌ {package}")
        return False
    else:
        print(f"\n✅ All test dependencies are available")
        return True


def check_environment_variables():
    """Check important environment variables."""
    import os

    env_vars = {
        'DATABASE_URL': 'Database connection string',
        'GROQ_API_KEY': 'AI service API key',
        'LLAMA_MODEL': 'AI model specification'
    }

    print(f"\n🔧 Environment variables:")
    all_set = True

    for var, description in env_vars.items():
        value = os.getenv(var)
        if value:
            if 'API_KEY' in var or 'PASSWORD' in var:
                print(f"  ✅ {var}: {'*' * 10} (hidden)")
            else:
                print(f"  ✅ {var}: {value}")
        else:
            print(f"  ⚠️  {var}: Not set ({description})")
            all_set = False

    return all_set


def main():
    """Main verification function."""
    print("🔍 E-CLARIA AI Python Environment Verification")
    print("=" * 50)

    checks = [
        ("Python Version", check_python_version()),
        ("Required Packages", check_required_packages()),
        ("Docker Availability", check_docker_availability()),
        ("Test Dependencies", check_test_dependencies()),
        ("Environment Variables", check_environment_variables())
    ]

    print("\n" + "=" * 50)
    print("📋 Verification Summary:")
    print("=" * 50)

    all_passed = True
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:.<30} {status}")
        if not result:
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! Your environment is ready for development.")
        print("\nNext steps:")
        print("1. Start Docker services: docker-compose up -d")
        print("2. Run tests: python run_tests.py")
        print("3. Access API docs: http://localhost:8000/docs")
    else:
        print("⚠️  Some checks failed. Please address the issues above.")
        print("\nCommon solutions:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Install test dependencies: pip install -r requirements-test.txt")
        print("3. Set up environment: cp .env.example .env && nano .env")
        print("4. Install Docker: https://docs.docker.com/get-docker/")

    print("=" * 50)
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
