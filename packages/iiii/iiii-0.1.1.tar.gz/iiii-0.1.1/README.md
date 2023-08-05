# iiii [Four Eyes] Search Engine

Four Eyes is a search engine that helps you look wider and deeper.

## Installation

Use Python's virtual environment module to create your build environment, then with  [pip](https://pip.pypa.io/en/stable/) install the requirements file. Next, install Rust-nightly from the official website and ensure your `$PATH` is properly configured for your system. With the Rust package manager [cargo](https://crates.io/), build the binary folder targets.

```bash
python3 -m venv . && source bin/activate
python3 -m pip install -r requirements.txt
cargo build --release
cargo install --path .
```

## Usage

```bash
user@computer$ iiii
[iiii]: <cool internet thing>
...
[RESULTS]
...
user@computer$ sudo iiii -f <random thing on file system>
...
[FILE MATCHES]
...
user@computer$ iiii -dl <favorite memes>
...
[RESULTS]
...
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
