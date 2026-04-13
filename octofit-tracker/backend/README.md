# OctoFit Tracker (backend)

This README explains how to set up the development environment for the OctoFit Tracker Django backend and how to run the automated population check tests.

Prerequisites
- Python 3.10+ (same version used for the virtual environment)
- MongoDB (mongod) running on `mongodb://localhost:27017` for local development

Setup

1. Create and activate the virtual environment (already created in this workspace):

```bash
python3 -m venv octofit-tracker/backend/venv
source octofit-tracker/backend/venv/bin/activate
```

2. Install requirements:

```bash
pip install -r octofit-tracker/backend/requirements.txt
```

3. Apply migrations:

```bash
source octofit-tracker/backend/venv/bin/activate
python octofit-tracker/backend/manage.py makemigrations
python octofit-tracker/backend/manage.py migrate
```

Populate test data

Run the management command that populates sample data:

```bash
source octofit-tracker/backend/venv/bin/activate
python octofit-tracker/backend/manage.py populate_db
```

Automated check (tests)

The repository includes a small Django test which runs the `populate_db` command and asserts that sample data was created. Run it with:

```bash
source octofit-tracker/backend/venv/bin/activate
python octofit-tracker/backend/manage.py test octofit_tracker -v2
```

If the test passes, the population command created the minimum expected records. If it fails, the test output will show which expectation was not met.

Notes
- The project uses `djongo` to connect Django ORM to MongoDB. Some djongo features do not fully match SQL behaviors; the population command is written defensively to tolerate common ObjectId vs integer PK mismatches.
- For CI or isolated integration tests, prefer running tests against a fresh MongoDB instance to avoid leftover documents affecting results.
