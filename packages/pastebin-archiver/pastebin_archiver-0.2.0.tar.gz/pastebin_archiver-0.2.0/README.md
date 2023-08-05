# Pastebin Archiver
## What is this?
This app retrieves new posts made on Pastebin.com and stores them offline in a database. You can see the latest public posts it will retrieve [here](https://pastebin.com/archive).

## Why?
Some of the pastes posted to Pastebin contain interesting or sensitive data, and sometimes pastes are deleted by their poster or Pastebin staff. Running an instance of this archiver lets you retrieve deleted pastes and build a large dataset to run queries against.

## Pastebin API info
_Important:_ This archiver uses the [Pastebin Scraping API](https://pastebin.com/doc_scraping_api) which requires a whitelisted IP address and a Lifetime Pro account to use. [More info here](https://pastebin.com/faq#17).

## Installation
### Install from PyPI (recommended)
1. Ensure you have Python 3.7+ installed.
2. Run `pip install pastebin_archiver`
3. Done! Jump down to the [Usage](#usage) section to get started.

### Install from source
1. Ensure you have Python 3.7+ and poetry installed
    ```shell
    $ python --version
    Python 3.7.4
    $ poetry --version
    Poetry 0.12.17
    ```
2. Clone the git repository
    ```shell
    git clone https://gitlab.com/jonpavelich/pastebin-archiver.git 
    ```
3. Install the dependencies
    ```shell
    $ cd pastebin-archiver
    $ poetry install
    ``` 
4. Run it!
    ```shell
    $ poetry run pastebin-archiver
    ```

### Run unit tests
1. Install from source (see the section above)
2. Run `poetry run python -m unittest`

## Usage
### Command line usage
If you installed the package using pip, then you can simply run `pastebin-archiver`: 
```shell
$ pastebin-archiver         # Run with default settings
$ pastebin-archiver --help  # Print available command line options
```

### Python usage 
If you'd prefer to use the package in your own code, you can do so like this:
```python
# Import the package
from pastebin_archiver import PastebinArchiver

# (Optional) configure logging
logging.basicConfig(level=logging.DEBUG) 

# Run the application
app = PastebinArchiver()
app.main()
```
_Important:_ `app.main()` does not return, it runs forever looking for new pastes to fetch.

## Configuration
### Database
By default, the fetched data will be saved to a SQLite database file in your working directory called `pastebin.db`. You can change this behaviour by passing in a database connection string using the `--database` option. For example:
```shell
$ pastebin-archiver --database 'postgresql://user:pass@localhost/mydatabase'
```

_Important:_ You'll need extra packages to connect to databases other than SQLite.
For PostgreSQL, you'll need to run `pip install psycopg2-binary` (or if you installed from source, you can run `poetry install -E pgsql`)

For detailed info on connection strings and a list of database packages you can use, see [the SQLAlchemy documentation](https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls).

## Contributing
If you find any bugs or have any suggestions to improve the project, please [open an issue](https://gitlab.com/jonpavelich/pastebin-archiver/issues/new) on GitLab.
