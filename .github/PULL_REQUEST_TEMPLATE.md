# Pull Request

## Description

Please include a summary of the changes and the related issue. Please also include relevant motivation and context.

Fixes # (issue)

## Type of Change

Please delete options that are not relevant.

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] 🎨 Code style update (formatting, renaming)
- [ ] ♻️ Code refactoring (no functional changes)
- [ ] ⚡ Performance improvement
- [ ] ✅ Test update
- [ ] 🔧 Configuration change
- [ ] 🔨 Build/CI change

## Changes Made

Describe the changes in detail:

- Changed X to Y
- Added feature Z
- Removed deprecated functionality

## Testing

Please describe the tests that you ran to verify your changes:

- [ ] Test A
- [ ] Test B
- [ ] Manual testing

**Test Configuration**:
- Python version:
- OS:
- Database used:

## Test Evidence

```bash
# Paste test output here
pytest -v
================================ test session starts =================================
collected 10 items

tests/test_cli.py::test_feature PASSED                                     [ 10%]
tests/test_generation.py::test_new_feature PASSED                          [ 20%]
...
================================ 10 passed in 2.34s ==================================
```

## Generated Project Testing

If your change affects generated projects, please test:

```bash
# Generate a project
python -m fastapi_boilerplate_agent.cli

# Test the generated project
cd test_project
make install
make test
make run
# Visit http://localhost:8000/docs
```

Results:
- [ ] Project generates successfully
- [ ] Project tests pass
- [ ] API starts without errors
- [ ] Swagger documentation works

## Checklist

- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## Code Quality

- [ ] Code is formatted with Black: `black src tests`
- [ ] Code passes linting: `flake8 src tests`
- [ ] Type hints are added where appropriate
- [ ] No commented-out code left behind
- [ ] No unnecessary print statements

## Documentation

- [ ] Updated README.md (if needed)
- [ ] Updated CHANGELOG.md
- [ ] Added/updated docstrings
- [ ] Updated relevant documentation files

## Screenshots (if applicable)

Add screenshots of the feature or bug fix in action.

**Before**:
<!-- Screenshot showing the issue -->

**After**:
<!-- Screenshot showing the fix/feature -->

## Breaking Changes

Does this PR introduce any breaking changes?

- [ ] No
- [ ] Yes (please describe below)

**Breaking Changes Description**:
<!-- If yes, describe what breaks and how to migrate -->

## Dependencies

Does this PR add any new dependencies?

- [ ] No
- [ ] Yes (please list below)

**New Dependencies**:
<!-- List any new packages and justify why they're needed -->

## Performance Impact

Does this change impact performance?

- [ ] No performance impact
- [ ] Improves performance
- [ ] May decrease performance (explain below)

**Performance Notes**:
<!-- Any relevant performance considerations -->

## Rollback Plan

If this change causes issues, how can it be rolled back?

<!-- Describe the rollback procedure -->

## Additional Notes

Add any additional notes, concerns, or questions for reviewers.

## Related Issues

Link related issues here:
- Closes #
- Related to #
- Depends on #

---

## Reviewer Checklist

For reviewers:

- [ ] Code is clear and well-documented
- [ ] Tests are comprehensive
- [ ] No security concerns
- [ ] Performance is acceptable
- [ ] Documentation is updated
- [ ] Changes align with project goals
