---
name: update-python-llama-cpp-python
description: Use when updating the Fedora python-llama-cpp-python RPM package to a new upstream llama-cpp-python release — bumping the bundled llama.cpp vendor tarball, fixing downstream patch conflicts, or diagnosing mock/koji build failures like "file INSTALL cannot find llama-mtmd-cli" or a `sources` file that lost an existing tarball checksum after `fedpkg new-sources`.
---

# Update python-llama-cpp-python

## Overview

`python-llama-cpp-python.spec` bundles a matching llama.cpp source tarball (Source1) alongside the pypi tarball (Source0), because llama-cpp-python vendors llama.cpp as a git submodule pinned to a specific commit. Bumping `pypi_version` without also re-pinning the vendored llama.cpp commit causes CMake install failures at build time — the two must move together.

## Workflow

1. **Bump the Python package version** — edit `%global pypi_version` in the spec.

2. **Find the matching llama.cpp commit.** Don't assume it's unchanged — re-derive it every time:
   ```
   git clone --depth 50 --branch v<version> https://github.com/abetlen/llama-cpp-python.git /tmp/check
   cd /tmp/check && git submodule status   # commit hash for vendor/llama.cpp
   ```
   Note: the repo moved from `github.com/ggerganov/llama.cpp` to `github.com/ggml-org/llama.cpp` (old URL still redirects, but use the canonical one). Update `%global llama_repo`, `%global llama_commit` (full hash), and `%global llama_archive` (`llama.cpp-<7-char-short-hash>.tar.gz`).

3. **Download sources and check for patch drift:**
   ```
   spectool -g python-llama-cpp-python.spec
   fedpkg prep
   ```
   If a downstream patch rejects (e.g. `0002-search-for-libllama-so-in-usr-lib64.patch`), it's usually because upstream changed the surrounding code — an `if` becoming an `elif`, or lines shifting up/down — which changes both the line numbers *and* the context lines in the patch's hunk. Fix by editing the patch file directly: diff the extracted source in `python-llama-cpp-python-<version>-build/llama-cpp-python-<version>/` against the patch's context, then update the `@@ -old,+new @@` header and any changed context lines to match. Re-run `fedpkg prep` until `%prep` succeeds with no rejects.

4. **Full local build via mock — this is the real test:**
   ```
   fedpkg mockbuild --root fedora-rawhide-x86_64
   ```
   `fedpkg prep` only proves patches apply; it does not compile or run `%check`. Watch for:
   - `file INSTALL cannot find ".../llama-mtmd-cli"` (or similar missing-binary CMake errors) — almost always means the vendored llama.cpp commit doesn't match this llama-cpp-python release. Redo step 2.
   - `%check` failures from new tests that call `hf_hub_download` and hit the network — mock/koji builds have no network, so these fail with `Temporary failure in name resolution`. Find them with `grep -n "hf_hub_download\|^def test_" tests/test_llama.py` in the extracted source, and add matching `-k 'not ...'` clauses to the spec's `%pytest` invocation (it already excludes patterns like `test_real_llama`, `test_real_model`, `test_llama_cpp_tokenization`).
   Full logs land in `results_python-llama-cpp-python/<version>/<release>/build.log`.

5. **Upload sources — avoid the overwrite trap:**
   ```
   fedpkg new-sources llama-cpp-python-<version>.tar.gz llama.cpp-<short-hash>.tar.gz
   ```
   **`fedpkg new-sources` REPLACES the whole `sources` file with exactly the filenames passed — it does not append.** This spec has two `Source` lines; always pass both in the same call, even if only one changed, or you silently drop the other's checksum. Verify after running it:
   ```
   git diff --cached sources
   ```
   and confirm every `Source` entry from the spec still has a line.

6. Commit the `.spec`, patch file(s), `sources`, and `.gitignore` (spectool appends the new tarball name there automatically).

## Common mistakes

| Mistake | Fix |
|---|---|
| Assuming the llama.cpp commit is unchanged across a version bump | Re-derive it from upstream's submodule pin every time (step 2) |
| "Fixing" a rejected patch by only adjusting line numbers | Diff against the actual new source — structural changes (`if`→`elif`) shift context text too |
| Treating `fedpkg prep` success as "the build works" | Only `mockbuild` compiles and runs `%check`, where mtmd/network failures actually surface |
| Running `fedpkg new-sources` with just the one changed file | Always pass every `Source` file in the spec; check `git diff --cached sources` afterward |
