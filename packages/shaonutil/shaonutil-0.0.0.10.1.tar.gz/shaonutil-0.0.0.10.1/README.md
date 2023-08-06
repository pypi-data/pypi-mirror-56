# Utility Functions for developers
Author: Shaon Majumder

## Utilities
- stats
- network
- image
- string
- file

## Installation
	pip install shaonutil

## Usages

### File
shaonutil.file.get_all_functions(object/file/class)

### Statistics

shaonutil.stats.mean(list of numbers)

shaonutil.stats.median(list of numbers)

shaonutil.stats.mode(list of numbers)

## Versioning

 *major.minor[.maintenance[.build]]* (example: *1.4.3.5249*) 

adoption: major.minor.patch.maintenance.status.trials_for_success

The last position 

- 0 for alpha (status)
- 1 for beta (status)
- 2 for release candidate
- 3 for (final) release

For instance: 

- 1.2.0.1 instead of 1.2-a1
- 1.2.1.2 instead of 1.2-b2 (beta with some bug fixes)
- 1.2.2.3 instead of 1.2-rc3 (release candidate)
- 1.2.3.0 instead of 1.2-r (commercial distribution)
- 1.2.3.5 instead of 1.2-r5 (commercial distribution with many bug fixes)