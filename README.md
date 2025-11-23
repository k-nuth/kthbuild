# kthbuild

[![PyPI version](https://badge.fury.io/py/kthbuild.svg)](https://badge.fury.io/py/kthbuild)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Build Automation and Package Management Tools for Knuth Cryptocurrency Node**

A Python library providing comprehensive build automation, version management, and Conan integration for the [Knuth](https://github.com/k-nuth/kth) cryptocurrency full-node implementation. Handles CPU architecture detection, compiler flag optimization, and multi-platform package builds.

## Features

- **Conan 2.0 Integration** - Seamless integration with Conan C/C++ package manager
- **CPU Architecture Detection** - Automatic detection and optimization for x86/x64 microarchitectures
- **Version Management** - Automatic version extraction from Git tags and branches
- **Build Configuration** - Generate optimized build configurations for different platforms
- **Remote Management** - Automatic setup of Knuth Conan remotes
- **Multi-Architecture Builds** - Support for building across multiple CPU architectures
- **CI/CD Ready** - Designed for automated continuous integration workflows

## Installation

```bash
pip install kthbuild
```

## Requirements

- Python 3.7+
- Conan >= 2.0
- Git (for version management features)
- [`microarch`](https://github.com/k-nuth/microarch) >= 0.2.0 (x86/x64 only, auto-installed)

## Quick Start

### Basic Usage in Conanfile

```python
from kthbuild import KnuthConanFile

class MyPackageConan(KnuthConanFile):
    name = "my-package"
    version = "1.0.0"

    # Automatic Knuth configuration
    # - Sets up remotes
    # - Configures build settings
    # - Handles version management
```

### Version Management

```python
import kthbuild

# Get version from Git tags
version = kthbuild.get_version(".")
print(f"Current version: {version}")

# Get current Git branch
branch = kthbuild.get_git_branch()
print(f"Current branch: {branch}")

# Check if on development branch
is_dev = kthbuild.is_development_branch()
print(f"Development branch: {is_dev}")

# Convert branch name to Conan channel
channel = kthbuild.branch_to_channel(branch)
print(f"Conan channel: {channel}")
```

### CPU Architecture Detection

```python
import kthbuild

# Get target architectures for build
archs = kthbuild.get_archs()
print(f"Target architectures: {archs}")

# Get base march IDs for multi-arch builds
march_ids = kthbuild.get_base_march_ids()
print(f"March IDs: {march_ids}")
```

### Conan Configuration

```python
import kthbuild

# Get Conan user/channel
user = kthbuild.get_user(".")
channel = kthbuild.get_channel(".")
print(f"Conan reference: {user}/{channel}")

# Get Knuth Conan upload URL
upload_url = kthbuild.get_conan_upload("k-nuth")
print(f"Upload URL: {upload_url}")

# Get configured remotes
remotes = kthbuild.get_conan_remotes("k-nuth")
print(f"Remotes: {remotes}")
```

## Core Functionality

### 1. Version Management

Automatically extracts version information from your Git repository:

- **From Git Tags**: Reads version from annotated tags (e.g., `v1.2.3`)
- **From Branches**: Increments version for development branches
- **From Files**: Reads version from `conan_version` file if present

```python
# Get version for current directory
version = kthbuild.get_version(".")

# Get version for development branch (auto-increments)
dev_version = kthbuild.get_version_from_git_describe(is_dev_branch=True)

# Get version from file
file_version = kthbuild.get_version_from_file(".")
```

### 2. Channel Management

Automatically determines the appropriate Conan channel:

- **master** → `stable`
- **dev/feature branches** → branch name as channel
- **release branches** → `stable`

```python
# Get channel from current branch
channel = kthbuild.get_channel_from_branch()

# Get channel from file or branch
channel = kthbuild.get_channel(".")
```

### 3. Build Configuration

Generates optimized build configurations for different architectures:

```python
# Get builder with automatic configuration
builder = kthbuild.get_builder(".", args)

# Handle microarchitecture-specific builds
kthbuild.handle_microarchs(
    opt_name="march_id",
    microarchs=march_ids,
    filtered_builds=builds,
    settings={},
    options={},
    env_vars={},
    build_requires={}
)
```

### 4. Conan Remote Management

Automatically configures Knuth Conan remotes on installation:

```python
# Remotes are configured automatically when installing kthbuild
# Default remote: https://packages.kth.cash/api/

# Get remote configuration
remotes = kthbuild.get_conan_remotes("k-nuth")
# Returns: "kth,https://packages.kth.cash/api/"
```

## Use Cases

### Building Knuth Packages

```python
from kthbuild import KnuthConanFile, option_on_off, get_version, get_channel

class KthInfrastructureConan(KnuthConanFile):
    name = "kth-infrastructure"
    version = get_version(".")

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_tests": [True, False],
        "march_id": ["ANY"],
    }

    default_options = {
        "shared": False,
        "fPIC": True,
        "with_tests": False,
        "march_id": "_DUMMY_",
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        # Automatic Knuth configuration
        super().configure()
```

### CI/CD Integration

```yaml
# .github/workflows/build.yml
- name: Install kthbuild
  run: pip install kthbuild

- name: Build package
  run: |
    conan create . kth/stable --build=missing
```

### Multi-Architecture Builds

```python
import kthbuild

# Get all target architectures
march_ids = kthbuild.get_base_march_ids()

for march_id in march_ids:
    print(f"Building for {march_id}...")
    # Build package for each architecture
```

## API Reference

### Version Functions

- `get_version(recipe_dir)` - Get version from Git or file
- `get_version_from_git_describe(is_dev_branch=False)` - Get version from Git tags
- `get_version_from_file(recipe_dir)` - Read version from file
- `get_git_describe()` - Get Git describe output
- `get_git_branch()` - Get current Git branch name

### Channel Functions

- `get_channel(recipe_dir)` - Get Conan channel from branch or file
- `get_channel_from_branch()` - Convert branch name to channel
- `branch_to_channel(branch)` - Convert branch name to channel name

### User/Repository Functions

- `get_user(recipe_dir)` - Get Conan user (default: "kth")
- `get_repository()` - Get repository name (default: "kth")
- `get_user_repository(org_name, repo_name)` - Get user/repo tuple

### Conan Configuration Functions

- `get_conan_upload(org_name)` - Get Conan upload URL
- `get_conan_remotes(org_name)` - Get Conan remotes configuration
- `get_builder(recipe_dir, args)` - Get configured Conan package builder

### Architecture Functions

- `get_archs()` - Get target architectures for current platform
- `get_base_march_ids()` - Get base microarchitecture IDs for builds
- `handle_microarchs(...)` - Configure builds for multiple microarchitectures

### Platform Functions

- `get_os()` - Get operating system identifier
- `is_development_branch()` - Check if on development branch

## Environment Variables

kthbuild respects several environment variables for CI/CD:

- `CONAN_UPLOAD` - Custom Conan upload URL
- `CONAN_REMOTES` - Custom Conan remotes
- `CONAN_REFERENCE` - Conan package reference
- `CPT_PROFILE` - Conan package tools profile

## Knuth Project Integration

kthbuild is a core component of the [Knuth](https://github.com/k-nuth/kth) cryptocurrency development platform. It's used to:

- Build Knuth C++ libraries and node implementations
- Generate architecture-optimized binaries for Bitcoin Cash (BCH) and Bitcoin (BTC)
- Manage Conan packages across the Knuth ecosystem
- Automate CI/CD pipelines for multi-platform builds
- Ensure reproducible builds across different environments

## Architecture Support

### x86/x64 Platforms

Full support with automatic CPU feature detection and optimization:
- Detects SSE, AVX, AVX2, AVX-512 support
- Generates optimal compiler flags per architecture
- Supports x86-64-v1, v2, v3, v4 microarchitecture levels

### ARM Platforms

Basic support without microarchitecture detection:
- Uses Conan's default architecture settings
- No CPU feature detection (x86-only CPUID instruction)

## Development

### Running Tests

```bash
# Install in development mode
pip install -e .

# Run your Conan builds
conan create . kth/stable
```

### Contributing

Contributions are welcome! This project is part of the Knuth ecosystem.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Credits

Created and maintained by [Fernando Pelliccioni](https://github.com/fpelliccioni) as part of the [Knuth Project](https://github.com/k-nuth).

## Related Projects

- [microarch](https://github.com/k-nuth/microarch) - CPU microarchitecture detection
- [cpuid](https://github.com/fpelliccioni/cpuid-py) - Python CPUID bindings
- [Knuth](https://github.com/k-nuth/kth) - Full-node cryptocurrency infrastructure
- [Conan](https://conan.io/) - C/C++ package manager

## Support

- Documentation: https://github.com/k-nuth/kthbuild
- Issues: https://github.com/k-nuth/kthbuild/issues
- Knuth Project: https://kth.cash
