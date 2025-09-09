
# AkashaOS Update Instructions

This package contains the enhanced version of AkashaOS with:

- CLI tool (`akasha`)
- Plugin/module system (`akasha_modules/`)
- Marketplace integration (`marketplace/`)
- Improved developer experience

## How to Update Your Repo

1. **Backup your repo** (just in case):
   ```bash
   cp -r your-repo your-repo-backup
   ```

2. **Extract this package** into your repo folder:
   ```bash
   unzip AkashaOS_cloudified_full_updated.zip -d your-repo
   ```

3. **Install dependencies** (if any):
   ```bash
   pip install -r requirements.txt
   ```

4. **Use the CLI**:
   ```bash
   python -m akasha.cli --help
   ```

5. **Create a new module**:
   ```bash
   python -m akasha.cli create-module my_module
   ```

6. **List marketplace modules**:
   ```bash
   python -m akasha.cli marketplace list
   ```

---

## Notes

- You can extend the `marketplace/` directory with JSON or metadata for modules.
- Devs can push/pull modules as simple folders with metadata.json files.
- This repo is structured to grow into a monetizable ecosystem.


---

## Publishing to PyPI

1. Install build tools:
   ```bash
   pip install build twine
   ```

2. Build the package:
   ```bash
   python -m build
   ```

3. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```

4. Install globally:
   ```bash
   pip install akashaos
   ```
