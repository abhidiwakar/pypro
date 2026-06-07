# Project Memory

## Release convention

For `kraf`, every published package change should follow this sequence:

1. Bump the package version.
2. Build and upload the package to PyPI.
3. Confirm the PyPI release is available.
4. Create and push a matching git tag, for example `v0.1.1`.
5. Create a GitHub Release from that tag with concise release notes.

Do not create the GitHub Release before the PyPI publish succeeds.
