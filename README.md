# LIGHTER

LIGHTER is a tool for bulk testing of sites for SQL injection, using dorks obtained from search engines such as Google.

## Description

The program reads a file with dorks, then searches for sites based on them and checks them for vulnerabilities. It is important to note that the program does not make changes to sites and is not capable of harming them. You should also be aware that the program's results may not be accurate since it only performs a superficial check.
## Installation

1. Clone the repository:
```console
git clone https://github.com/LolzPrince/lighter.git
```
2. Go to the project directory:
```console
cd lighter/lighter
```
3. Install the necessary dependencies:
```console
pip install -r requirements.txt
```
## Usage

```console
python3 lighter.py path [options]
```
### Arguments

- path: Path to the file with dorks.

### Options
```console
- -h, --help: Show help.
- -r, --random-agent: Use random user-agent.
- -s SLEEP_INTERVAL, --sleep-interval SLEEP_INTERVAL: Specify an integer parameter for the time interval between requests to dorks.
- -t TIMEOUT, --timeout TIMEOUT: Specify an integer parameter for the time interval between page requests.
- -c COUNT, --count COUNT: Specify an integer parameter for the number of links received in one request to the dork. Default: 20.
- -l LANG, --lang LANG: Select a language to search for dorks. Example: en. Default: en.
- -w, --write-result: Use this flag to write the successful URL to a file.
- -p PROXY_LIST, --proxy-list PROXY_LIST: Path to the proxy file [http, https].
```
## License

This project is licensed under the terms of the MIT License - see file [LICENSE](LICENSE) for details
