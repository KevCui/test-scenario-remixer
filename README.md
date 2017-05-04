# Test Scenario Remixer

Every time when you launch remixer, it will generate a checklist with scenarios which are randomly selected from a prepared markdown file. It provides an interaction mode which can be used to check one by one scenario.

## Requirement

- python3k
- [md_to_json](https://github.com/njvack/markdown-to-json)

## Dependency

```
pip install markdown-to-json
```

## Usage

```
usage: scenarioRemixer.py [-h] [-n NUMBER] [-m] [-d] file

positional arguments:
  file                  input json file

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        number of scenario to display
  -m, --mute            generate checklist without interation
  -d, --debug           active debug log
```
