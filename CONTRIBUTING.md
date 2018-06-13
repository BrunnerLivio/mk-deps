# How to contribute

We love to see your contribution on this repository.

Here are some important resources:

  * [Submit a Bug](https://github.com/Roche/mk-deps/issues/new?template=Bug_report.md)
  * [Request a new feature](https://github.com/Roche/mk-deps/issues/new?template=Feature_request.md)

## Testing

All the tests are built with [pytest](https://docs.pytest.org/en/latest/). Please update these tests when submitting a
pull request.

## Submitting changes

Please send a [GitHub Pull Request to mk-deps](https://github.com/Roche/mk-deps/compare) with a clear list of what you've done (read more about [pull requests](http://help.github.com/pull-requests/)). Please follow our coding conventions (below) and make sure all of your commits are atomic (one feature per commit).

Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:

    $ git commit -m "A brief summary of the commit
    > 
    > A paragraph describing what changed and its impact."

## Coding conventions

Start reading our code and you'll get the hang of it. We optimize for readability:

  * We indent using four spcaes
  * This is open source software. Consider the people who will read your code, and make it look nice for them. It's sort of like driving a car: Perhaps you love doing donuts when you're alone, but with passengers the goal is to make the ride as smooth as possible.
  * Every method / class should be documeneted. Use this [Docstring guidelines](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
