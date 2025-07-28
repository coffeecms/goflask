"""
GoFlask - High-Performance Flask Alternative
Setup configuration for PyPI distribution
"""

from setuptools import setup, find_packages, Extension
import os
import sys
import platform
import subprocess
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

def get_version():
    """Get version from version file"""
    version_file = os.path.join(os.path.dirname(__file__), 'goflask', '_version.py')
    if os.path.exists(version_file):
        with open(version_file, 'r') as f:
            exec(f.read())
            return locals()['__version__']
    return "1.0.0"

def build_go_library():
    """Build the Go shared library if Go is available"""
    try:
        # Check if Go is installed
        subprocess.run(["go", "version"], check=True, capture_output=True)
        
        # Determine library extension based on platform
        if platform.system() == "Windows":
            lib_name = "goflask.dll"
            build_cmd = ["go", "build", "-buildmode=c-shared", "-o", lib_name]
        elif platform.system() == "Darwin":
            lib_name = "libgoflask.dylib"
            build_cmd = ["go", "build", "-buildmode=c-shared", "-o", lib_name]
        else:
            lib_name = "libgoflask.so"
            build_cmd = ["go", "build", "-buildmode=c-shared", "-o", lib_name]
        
        # Add source file to build command
        build_cmd.append("goflask_c_api.go")
        
        # Initialize Go module if not exists
        if not os.path.exists("go.mod"):
            subprocess.run(["go", "mod", "init", "goflask"], check=True)
            subprocess.run(["go", "mod", "tidy"], check=True)
        
        # Build the shared library
        print(f"Building GoFlask shared library: {lib_name}")
        subprocess.run(build_cmd, check=True)
        print(f"✅ Successfully built {lib_name}")
        
        return lib_name
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Go compiler not found. GoFlask will install in Python-only mode.")
        print("   Install Go 1.21+ for full performance benefits.")
        return None

# Build Go library during setup
go_library = build_go_library()

# Determine package data files
package_data = ['*.py', '*.md']
if go_library:
    package_data.extend(['*.dll', '*.so', '*.dylib', '*.h'])

setup(
    name="goflask",
    version=get_version(),
    author="GoFlask Team",
    author_email="team@goflask.dev",
    description="High-performance Flask-compatible web framework powered by Go",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coffeecms/goflask",
    project_urls={
        "Bug Reports": "https://github.com/coffeecms/goflask/issues",
        "Source": "https://github.com/coffeecms/goflask",
        "Documentation": "https://github.com/coffeecms/goflask/wiki",
        "Changelog": "https://github.com/coffeecms/goflask/blob/main/CHANGELOG.md",
    },
    packages=find_packages(exclude=["tests*", "examples*", "docs*"]),
    package_data={
        'goflask': package_data,
    },
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=[
        # No external Python dependencies - GoFlask is self-contained
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.12.0',
            'pytest-benchmark>=3.4.0',
            'black>=21.0.0',
            'flake8>=3.9.0',
            'mypy>=0.910',
            'pre-commit>=2.15.0',
        ],
        'testing': [
            'pytest>=6.0.0',
            'requests>=2.25.0',
            'pytest-asyncio>=0.15.0',
        ],
        'docs': [
            'sphinx>=4.0.0',
            'sphinx-rtd-theme>=0.5.0',
            'sphinx-autodoc-typehints>=1.12.0',
        ],
        'performance': [
            'wrk>=0.4.0',  # For load testing
            'matplotlib>=3.3.0',  # For performance graphs
            'numpy>=1.20.0',  # For statistical analysis
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Go",
        "Framework :: Flask",
        "Environment :: Web Environment",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords=[
        "web", "framework", "flask", "performance", "go", "golang", 
        "high-performance", "api", "rest", "microservices", "wsgi",
        "http", "server", "fast", "fiber", "cors", "rate-limiting"
    ],
    entry_points={
        'console_scripts': [
            'goflask=goflask.cli:main',
        ],
    },
    zip_safe=False,  # Due to Go shared library
)
