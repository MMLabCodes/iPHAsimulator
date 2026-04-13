# Legacy Code Archive

This directory contains deprecated code from SatisPHAction Simulator that is no longer actively maintained.

## Contents

- **`deprecated_functions.py`** - Legacy functions marked with deprecation warnings
- **`MIGRATION_GUIDE.md`** - Detailed guide for migrating to new implementations

## Why Archived?

These functions are archived because:
1. They have known bugs or limitations
2. Better implementations exist in the new modules
3. They don't follow current coding standards (PEP 8, type hints, docstrings)
4. They're not actively maintained

## Timeline

| Version | Status | Action |
|---------|--------|--------|
| v1.1+ | Deprecated | Functions moved here with warnings |
| v2.0 | Available | Available but prints deprecation warnings |
| v3.0 | Removed | Code will be deleted, use new implementations |

## What Should I Do?

1. **Read** `MIGRATION_GUIDE.md` for specific migration instructions
2. **Update** your imports to use new modules (e.g., `system_builder` instead of `sw_build_systems`)
3. **Run tests** to ensure everything works
4. **Plan migration** before v3.0 is released

## For Contributors

Do NOT add new functionality to this folder. If you need to fix or extend functionality:

1. Move the code to the appropriate new module
2. Refactor according to current standards (docstrings, type hints, PEP 8)
3. Add proper unit tests
4. Update the migration guide

## See Also

- `/README.md` - Main project documentation
- `/REFACTORING.md` - Project refactoring progress report
- `/modules/` - New modules with updated, maintained code

---

**Version**: SatisPHAction Simulator v1.1+
**Last Updated**: 2026-04-04
