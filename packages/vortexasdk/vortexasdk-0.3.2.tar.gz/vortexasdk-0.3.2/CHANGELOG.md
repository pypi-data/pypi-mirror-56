# Changelog

## [Unreleased](https://github.com/V0RT3X4/python-sdk/tree/HEAD)

[Full Changelog](https://github.com/V0RT3X4/python-sdk/compare/0.2.3...HEAD)

**Implemented enhancements:**

- Allow for filtering by product name in vessel endpoint filters  [\#31](https://github.com/V0RT3X4/python-sdk/issues/31)

**Merged pull requests:**

- fix: Move to pytest, run mock setup before each test [\#52](https://github.com/V0RT3X4/python-sdk/pull/52) ([KitBurgess](https://github.com/KitBurgess))
- ci: Add git change log [\#51](https://github.com/V0RT3X4/python-sdk/pull/51) ([KitBurgess](https://github.com/KitBurgess))
- feat: Filter vessels using products name [\#50](https://github.com/V0RT3X4/python-sdk/pull/50) ([KitBurgess](https://github.com/KitBurgess))

## [0.2.3](https://github.com/V0RT3X4/python-sdk/tree/0.2.3) (2019-11-19)

[Full Changelog](https://github.com/V0RT3X4/python-sdk/compare/0.2.2...0.2.3)

## [0.2.2](https://github.com/V0RT3X4/python-sdk/tree/0.2.2) (2019-11-19)

[Full Changelog](https://github.com/V0RT3X4/python-sdk/compare/0.2.1...0.2.2)

**Implemented enhancements:**

- Create Products endpoint [\#7](https://github.com/V0RT3X4/python-sdk/issues/7)

**Fixed bugs:**

- Tried to pull out a reference df of all vessels but only got 200 results? [\#29](https://github.com/V0RT3X4/python-sdk/issues/29)

**Closed issues:**

- searching vessel reference database only ever gives me back 100 results [\#30](https://github.com/V0RT3X4/python-sdk/issues/30)

## [0.2.1](https://github.com/V0RT3X4/python-sdk/tree/0.2.1) (2019-11-18)

[Full Changelog](https://github.com/V0RT3X4/python-sdk/compare/0.2.0...0.2.1)

**Closed issues:**

- filter arguments for origins/destinations must be passed as vortexa ids \(a user will not know what our ID's are\) [\#17](https://github.com/V0RT3X4/python-sdk/issues/17)

**Merged pull requests:**

- fix: Return all vessels from search, not just arbitrary 100 [\#41](https://github.com/V0RT3X4/python-sdk/pull/41) ([KitBurgess](https://github.com/KitBurgess))
- test: Correctly set client in tests [\#23](https://github.com/V0RT3X4/python-sdk/pull/23) ([KitBurgess](https://github.com/KitBurgess))
- Products endpoint test [\#11](https://github.com/V0RT3X4/python-sdk/pull/11) ([dstarkey23](https://github.com/dstarkey23))

## [0.2.0](https://github.com/V0RT3X4/python-sdk/tree/0.2.0) (2019-11-18)

[Full Changelog](https://github.com/V0RT3X4/python-sdk/compare/0.1.0...0.2.0)

**Closed issues:**

- Importing entities does not work \(or maybe im doing this wrong\)? [\#18](https://github.com/V0RT3X4/python-sdk/issues/18)
- filter arguments must be passed in array form \(this is not made clear to the user\) [\#16](https://github.com/V0RT3X4/python-sdk/issues/16)

**Merged pull requests:**

- perf: Call API in parallel [\#44](https://github.com/V0RT3X4/python-sdk/pull/44) ([KitBurgess](https://github.com/KitBurgess))
- style: Remove status token from README [\#32](https://github.com/V0RT3X4/python-sdk/pull/32) ([KitBurgess](https://github.com/KitBurgess))
- test: Fix global client state [\#28](https://github.com/V0RT3X4/python-sdk/pull/28) ([KitBurgess](https://github.com/KitBurgess))
- Filter on name [\#27](https://github.com/V0RT3X4/python-sdk/pull/27) ([KitBurgess](https://github.com/KitBurgess))
- Run tests against live API in circle ci [\#26](https://github.com/V0RT3X4/python-sdk/pull/26) ([KitBurgess](https://github.com/KitBurgess))
- Revert "ci: Run live tests in circleci" [\#24](https://github.com/V0RT3X4/python-sdk/pull/24) ([KitBurgess](https://github.com/KitBurgess))
- ci: Run live tests in circleci [\#22](https://github.com/V0RT3X4/python-sdk/pull/22) ([KitBurgess](https://github.com/KitBurgess))
- feat: Allow user to search cargo movements with single filter, fixes \#16 [\#21](https://github.com/V0RT3X4/python-sdk/pull/21) ([KitBurgess](https://github.com/KitBurgess))

## [0.1.0](https://github.com/V0RT3X4/python-sdk/tree/0.1.0) (2019-11-13)

[Full Changelog](https://github.com/V0RT3X4/python-sdk/compare/f34a5627d0047e9a9a56ecf4b19cb4af91395d01...0.1.0)

**Merged pull requests:**

- ci: Add export packages [\#15](https://github.com/V0RT3X4/python-sdk/pull/15) ([KitBurgess](https://github.com/KitBurgess))
- docs: Add tips to contributing docs [\#13](https://github.com/V0RT3X4/python-sdk/pull/13) ([KitBurgess](https://github.com/KitBurgess))
- refactor: Rename root dir from vortexa to vortexasdk [\#12](https://github.com/V0RT3X4/python-sdk/pull/12) ([KitBurgess](https://github.com/KitBurgess))
- docs: Improve the contributing guide [\#9](https://github.com/V0RT3X4/python-sdk/pull/9) ([KitBurgess](https://github.com/KitBurgess))
- refactor: Allow clients to import classes without knowledge of internals [\#8](https://github.com/V0RT3X4/python-sdk/pull/8) ([KitBurgess](https://github.com/KitBurgess))
- docs: Add quickstart to docs [\#5](https://github.com/V0RT3X4/python-sdk/pull/5) ([KitBurgess](https://github.com/KitBurgess))
- ci: Create the setup.py file [\#4](https://github.com/V0RT3X4/python-sdk/pull/4) ([KitBurgess](https://github.com/KitBurgess))
- test: Vessel dataframe test actually does something [\#3](https://github.com/V0RT3X4/python-sdk/pull/3) ([KitBurgess](https://github.com/KitBurgess))
- Consistent types [\#2](https://github.com/V0RT3X4/python-sdk/pull/2) ([KitBurgess](https://github.com/KitBurgess))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
