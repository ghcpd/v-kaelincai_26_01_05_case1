# Bug Fix Prompt for AI Model

## Task Overview

You are a senior software engineer tasked with fixing a deliberately planted bug in a meeting room booking system. Your goal is to analyze the buggy project, identify the issue, and create a **corrected version** in a new directory without modifying the original project.

## Project Context

The original buggy project is located at:
```
issue_project/
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── booking_system.py      # Contains the bug
│   └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_booking.py        # 2 tests currently FAIL
├── data/
│   └── sample_data.json
├── requirements.txt
├── README.md
└── KNOWN_ISSUE.md             # Detailed bug analysis
```

## Bug Description

**Type**: Functional Bug - Feature doesn't behave as specified (ignores constraints)

**Location**: Equipment validation logic in the booking system

**Symptom**: The system incorrectly approves meeting room bookings when the room has SOME but not ALL of the required equipment.

**Current Test Status**:
- 2 tests FAIL: `test_bug_partial_equipment_match_should_fail`, `test_bug_client_meeting_scenario`
- 2 tests PASS: `test_correct_behavior_all_equipment_available`, `test_successful_booking_no_equipment`

## Your Task

### 1. Analysis Phase
- Read and understand the original project structure
- Review the failing test cases in `tests/test_booking.py`
- Read the bug documentation in `KNOWN_ISSUE.md`
- Identify the exact location and root cause of the bug

### 2. Implementation Phase

Create a **new fixed version** with the following structure:

```
fixed_project/
├── src/
│   ├── __init__.py           # Copy and update if needed
│   ├── models.py             # Copy from original (no changes needed)
│   ├── booking_system.py     # Copy and FIX the bug here
│   └── utils.py              # Copy from original (no changes needed)
├── tests/
│   ├── __init__.py           # Copy from original
│   └── test_booking.py       # Copy from original (tests should now PASS)
├── data/
│   └── sample_data.json      # Copy from original
├── requirements.txt           # Copy from original
├── README.md                  # Create NEW README for fixed version
└── FIX_SUMMARY.md            # Create NEW file documenting the fix
```

### 3. Requirements

**DO**:
- Create the entire fixed project in a new directory called `fixed_project/`
- Copy all files from `issue_project/` to `fixed_project/`
- Fix ONLY the specific bug in the equipment validation logic
- Ensure ALL 4 tests pass after the fix
- Create a new `README.md` for the fixed version
- Create a `FIX_SUMMARY.md` documenting:
  - What was wrong
  - What you changed
  - How to verify the fix
  - Before/after code comparison

**DO NOT**:
- Modify any files in the original `issue_project/` directory
- Change business logic beyond fixing the bug
- Add new features or refactor unnecessarily
- Modify test cases (they should pass without changes)
- Use absolute file paths in any documentation

### 4. Validation

After implementing the fix, verify:
```bash
cd fixed_project
pip install -r requirements.txt
pytest tests/ -v
```

**Expected Result**: All 4 tests should PASS ✅

### 5. Documentation Requirements

#### README.md (for fixed_project/)
Should include:
- Project overview (fixed version)
- What was fixed
- Quick start guide
- Test execution instructions
- Confirmation that all tests pass

#### FIX_SUMMARY.md
Should include:
- Bug description
- Root cause analysis
- The specific code change made
- Before/after code snippets
- Test results comparison (before: 2 failed, after: 4 passed)
- Line numbers and file references (using relative paths)

## Example Relative Path References

When documenting changes, use relative paths like:
- `src/booking_system.py` (NOT `c:\BugBash\fixed_project\src\booking_system.py`)
- `tests/test_booking.py`
- Reference line numbers: `src/booking_system.py:103-120`

## Success Criteria

Your fix is successful when:
1. ✅ New `fixed_project/` directory exists with complete project structure
2. ✅ Original `issue_project/` remains unchanged
3. ✅ All 4 tests pass in the fixed version
4. ✅ Only the equipment validation logic was modified
5. ✅ Clear documentation explains the fix
6. ✅ Code is production-ready and follows Python best practices

## Hints

- The bug is in a validation method that checks equipment requirements
- Focus on set operations and logical conditions
- The fix should be simple (1-5 lines of code change)
- Read the test cases carefully - they show exactly what the expected behavior should be
- The `KNOWN_ISSUE.md` file contains valuable analysis

## Deliverables

When complete, provide:
1. Complete `fixed_project/` directory structure
2. All source files properly copied and fixed
3. Comprehensive `FIX_SUMMARY.md`
4. Updated `README.md` for the fixed version
5. Confirmation that tests pass

---

**Note**: This is a focused bug fix task. Make minimal changes to fix the specific issue. Do not refactor, add features, or modify functionality beyond what's necessary to fix the equipment validation bug.
