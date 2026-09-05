# Learning Log — Customer Support Analytics

## Project purpose

This portfolio project simulates a customer-support analytics workflow using fictional data.

The goal is to:

1. Generate realistic fictional support tickets.
2. Expose them through a local REST API.
3. Retrieve the data with Python.
4. Validate, clean and transform it with pandas.
5. Calculate support KPIs and prepare data for Power BI.

The project is developed on a laptop and a desktop PC. GitHub is the shared source of truth.

---

## Project setup

### Main tools

* Python 3.14
* Git 2.55
* VS Code
* FastAPI
* Uvicorn
* requests
* pandas
* scikit-learn
* pytest
* Power BI (later stage)

### Virtual environment

Each computer has its own local Python virtual environment:

```text
.venv
```

It contains the project libraries and is not uploaded to GitHub.

Create it once per computer:

```powershell
py -m venv .venv
```

Activate it in each new PowerShell terminal:

```powershell
.\.venv\Scripts\Activate.ps1
```

When it is active, the terminal starts with:

```text
(.venv)
```

In Git Bash, the activation command is:

```bash
source .venv/Scripts/activate
```

### Dependencies

The project dependencies are recorded in:

```text
requirements.txt
```

To install them in a new `.venv`:

```powershell
python -m pip install -r requirements.txt
```

This must be done once per computer and project, not every day.

If Python says:

```text
No module named pytest
```

the environment does not have the registered dependencies available. Activate `.venv` and run:

```powershell
python -m pip install -r requirements.txt
```

---

## Git and GitHub workflow

### Starting a session

```powershell
.\.venv\Scripts\Activate.ps1
git status
git pull
python -m pytest
```

`git pull` should only be used when there are no unfinished local changes.

### Saving completed work

A commit is created after one complete logical change, not after every small command.

```powershell
git status
git add FILE_OR_FOLDER_NAME
git commit -m "type: short description"
git push
```

### Before switching computers

1. Run `git status`.
2. Commit completed work.
3. Run `git push`.
4. On the other computer, start with `git pull`.

`git clone` is only used once per computer and project.

### Commit prefixes

These are conventions for readable project history. Git does not interpret them as commands.

* `feat:` new functionality.
* `fix:` bug fix.
* `test:` automated tests.
* `docs:` documentation.
* `chore:` configuration or maintenance.

Examples:

```text
feat: add tickets API endpoint
test: add ticket generator test
docs: add project Git workflow
chore: add project dependencies
```

### Important Git learning: amend

```powershell
git commit --amend -m "new commit message"
```

This changes the most recent local commit. It is useful when a file was forgotten or the commit message needs correction before the commit is pushed to GitHub.

Example:

```powershell
git add data/tickets.json
git commit --amend -m "fix: generate exactly 10 percent data quality issues"
```

### Important Git learning: rebase

If Git rejects a push with:

```text
non-fast-forward
```

it means GitHub has newer commits that are not yet on the local computer.

Safe solution:

```powershell
git status
git pull --rebase
git push
```

`git pull --rebase` downloads the remote changes and reapplies local commits on top of them without creating an unnecessary merge commit.

Do not use:

```powershell
git push --force
```

to solve this normal synchronization situation, because it could overwrite remote work.

---

## Current project structure

```text
Customer-Support-Analytics/
├── data/
│   └── tickets.json
├── docs/
│   ├── git-workflow.md
│   └── learning-log.md
├── exports/
├── src/
│   ├── api.py
│   ├── fetch_tickets.py
│   └── generate_tickets.py
├── tests/
│   └── test_generate_tickets.py
├── .gitignore
├── README.md
└── requirements.txt
```

### Folder responsibilities

| Folder or file            | Purpose                                            |
| ------------------------- | -------------------------------------------------- |
| `data/tickets.json`       | Raw fictional ticket dataset.                      |
| `src/generate_tickets.py` | Creates the fictional tickets.                     |
| `src/api.py`              | Provides tickets through a local FastAPI endpoint. |
| `src/fetch_tickets.py`    | Requests tickets from the API using `requests`.    |
| `tests/`                  | Automated tests.                                   |
| `exports/`                | Future CSV files for Power BI.                     |
| `docs/`                   | Project documentation and learning notes.          |
| `requirements.txt`        | Reproducible list of Python dependencies.          |

Git does not track empty folders. A common temporary solution is a file called `.gitkeep`, but this project creates real files inside folders as they become necessary.

---

## Dataset generation

The ticket generator is located in:

```text
src/generate_tickets.py
```

Run it with:

```powershell
python src/generate_tickets.py
```

It creates or replaces:

```text
data/tickets.json
```

The project uses one official raw dataset file. When the generator is run again, it replaces the old version.

Before experimenting with a dataset used for a presentation, create a commit. Git can then restore that committed version later.

### Reproducibility with a random seed

The generator uses:

```python
RANDOM_SEED = 42
```

A random seed makes Python produce the same “random” sequence every time.

```text
Same code + same seed + same number of tickets
= same tickets.json
```

This makes the dataset reproducible on the laptop and desktop PC.

Changing the seed creates a different dataset.

### Dataset content

The generator creates 350 fictional support tickets.

Each ticket contains fields such as:

* `ticket_id`
* `customer_id`
* `created_at`
* `first_response_at`
* `resolved_at`
* `status`
* `channel`
* `priority`
* `subject`
* `message`

The tickets use realistic support scenarios, including:

* Payment failed.
* Password reset.
* Invoice request.
* Login error `E401`.
* Account cancellation.
* Feature unavailable.
* Plan information.
* Duplicate charge.
* Integration error `E503`.
* Update contact details.

The dataset has 110 fictional customers, so some customers appear more than once. This will help later when detecting repeat contacts.

### Controlled data-quality issues

The dataset intentionally includes exactly 35 problematic tickets, which is 10% of 350.

| Problem                 | Quantity | Example                                   |
| ----------------------- | -------: | ----------------------------------------- |
| Missing first response  |       11 | `first_response_at = null`                |
| Invalid resolution date |        8 | `"resolved_at": "not_available"`          |
| Inconsistent priority   |        8 | `"priority": "HIGH "`                     |
| Invalid time order      |        8 | Resolution happens before ticket creation |

The dataset remains reproducible because the same random seed selects the same records each time.

The raw JSON is never the final dataset for Power BI. Later, pandas will create cleaned and transformed export files without replacing the original raw data.

### Safe dataset saving

The generator first writes to a temporary file and only replaces `tickets.json` after the generation succeeds. This reduces the risk of leaving a partially written JSON file if something fails during saving.

---

## Automated tests

The first test is located in:

```text
tests/test_generate_tickets.py
```

Run all tests with:

```powershell
python -m pytest
```

Expected result:

```text
1 passed
```

The current test checks that:

1. Requesting 7 tickets creates exactly 7 tickets.
2. The first ID is `TICKET-0001`.
3. The last ID is `TICKET-0007`.

This is a unit test. It does not modify `data/tickets.json`; it creates small temporary data in Python memory.

Later tests can verify that the official JSON file contains 350 tickets and the expected 35 controlled data-quality issues.

---

## Local REST API

The API is located in:

```text
src/api.py
```

It uses FastAPI and reads:

```text
data/tickets.json
```

The endpoint is:

```text
GET /api/v1/tickets
```

Start the API server with:

```powershell
python -m uvicorn src.api:app --reload
```

The server runs locally at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

A successful response returns:

```text
200 OK
```

This means that the API found the JSON dataset, read it correctly and returned the ticket data.

If the dataset file is missing, the API returns an HTTP 404 response with a clear message instead of closing unexpectedly.

### API concepts learned

```text
tickets.json → api.py → fetch_tickets.py
   data         offers       requests and receives
```

* `tickets.json` stores the data.
* `api.py` is the local service that offers the data.
* `fetch_tickets.py` is a client that requests the data.

`localhost` or `127.0.0.1` means the local computer. The API is not publicly available on the internet.

---

## API client

The client is located in:

```text
src/fetch_tickets.py
```

It uses the `requests` library to send an HTTP GET request to:

```text
http://127.0.0.1:8000/api/v1/tickets
```

Run it while the API server is active:

```powershell
python src/fetch_tickets.py
```

Expected output:

```text
Received 350 tickets from the API.
First ticket ID: TICKET-0001
```

The API server and client must run in separate terminals:

```text
Terminal 1: API server
Terminal 2: API client
```

The API terminal remains occupied while the server is active. Stop it safely with:

```text
Ctrl + C
```

---

## Python concepts learned

### Functions

A function is a named block of instructions:

```python
def generate_tickets(total: int, seed: int) -> list[dict]:
```

The function receives a number of tickets and a random seed, then returns a list of ticket dictionaries.

### Indentation

Python uses indentation to show which lines belong inside a function.

```python
def example():
    instruction_inside_function()
    another_instruction_inside_function()
```

The indented lines are instructions “inside” the function.

### Comments

Use `#` for ordinary comments:

```python
# Generate 350 valid tickets.
```

Use triple quotes for docstrings that describe a file or function:

```python
"""Generate reproducible fictional support tickets."""
```

### `assert`

`assert` means “this must be true.”

```python
assert len(tickets) == 7
```

If it is not true, pytest marks the test as failed and shows the problem.

---

## Current progress

Completed:

* GitHub repository created and synchronized across laptop and PC.
* Git identity configured with a private GitHub noreply email.
* Python virtual environments created.
* Dependencies installed and recorded in `requirements.txt`.
* Git workflow documented.
* 350 reproducible fictional support tickets generated.
* Exactly 35 controlled data-quality issues added.
* Automated generator test created and passed.
* Local FastAPI endpoint created and manually verified with `200 OK`.
* Python client created with `requests`.
* Client successfully received 350 tickets from the local API.
* Changes saved progressively with commits and pushed to GitHub.

---

## Next steps

1. Use pandas to request tickets from the API and create a DataFrame.
2. Profile the raw data and detect the 35 data-quality issues.
3. Clean and normalize dates, priorities and missing values.
4. Export a cleaned dataset to CSV.
5. Calculate response time, resolution time and SLA breaches.
6. Classify contact reasons from ticket text.
7. Extract error codes, urgency, escalation and cancellation indicators.
8. Detect repeat contacts using TF-IDF and cosine similarity.
9. Build an explainable Customer Effort Risk Score.
10. Create Power BI dashboard KPIs and drilldowns.
