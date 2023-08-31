= Contributing to i75 =

Welcome! Thank you for thinking about contributing to `i75`! We'd love to merge your code changes into the project, and to discuss any improvements or bugs you might have found. Feel free to create PRs or Issues and we'll happily help you to get changes ready merge. The details in this document will help make this process a little smoother, so thank you for taking the time to read it.

= Pull Requests and Commits =

Please keep pull requests as small and as specific as possible, and avoid combining unrelated changes into one PR. We use Python Semantic Release, which uses the [Angular Commit Guidelines](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commits). Please try to follow this to make the automatic change log generation and release process smoother.

= Code Changes =

Please make sure to run `code_style.sh` and `run_tests.sh` and fix any issues before committing any changes. We aim to keep the output from `pycodestyle` clean.

For smaller changes feel free to just submit the PR. If your change involves a more substantial change, please discuss in an issue first just to avoid extra rework.

= Areas for improvment =

`i75` has quite a few areas for improvement, and any contributions in these areas would be greatly appreciated. If there are
other features we could add, or bugs to fix, that would be useful to you, please do contribute those to. This is not an
exhaustive list!

* Creating a graphics layer that can be used with MicroPython, avoiding the need to use Python 3.
* Limiting performance to more accurately represent the physical hardware.
* Adding to or improving the emulation of built-in modules.
* Adding support for sensors or additional hardware.
