# Contribution Tracker

A small command-line app for keeping track of open-source repositories, issues,
and pull requests you want to contribute to. It stores data in a local JSON file
and uses only the Python standard library.

This project is also a place to practice Git and GitHub: work from issues, make
small branches, open pull requests, and review contributions.

## Requirements

- Python 3.9 or newer

## Run it

From this directory:

```bash
python3 -m contribution_tracker add \
  --repo owner/project \
  --url https://github.com/owner/project/issues/1 \
  --title "Example contribution"

python3 -m contribution_tracker list
python3 -m contribution_tracker view
```

By default, the app saves your entries to `.contribution-tracker.json` in this
project directory. Git ignores this local data file, so your entries won't be
committed. To use a different file (for example, in a test directory), pass
`--data-file` before the command:

```bash
python3 -m contribution_tracker --data-file ./tracker.json list
```

The `view` command creates a local HTML page next to the data file and opens it
in your browser. The generated page is also ignored by Git.

Update an entry by its ID:

```bash
python3 -m contribution_tracker update ID --status in-progress
python3 -m contribution_tracker update ID --notes "Waiting for maintainer feedback"
```

Available statuses are `planned`, `in-progress`, `pr-open`, `merged`, and
`closed`.

## Run the tests

```bash
python3 -m unittest discover -s tests -v
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development and pull request
workflow. Bug reports and feature ideas are welcome through GitHub Issues.

## License

This project is licensed under the [MIT License](LICENSE).

