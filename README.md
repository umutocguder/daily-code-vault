# 🚀 Daily Code & Engineering Vault

An automated, daily code and engineering journal that curates clean, well-tested algorithms, architectural patterns, and software design insights.

---

## 📌 Features

- **Automated Daily Push**: Runs via GitHub Actions cron scheduler every day.
- **High-Quality Code**: Includes full type annotations, docstrings, and comprehensive unit tests.
- **Zero Temp/Junk Code**: Carefully structured modules across:
  - `algorithms/`: Data structures & fundamental algorithms.
  - `patterns/`: System design, resiliency, and architectural patterns.
  - `notes/`: Technical breakdowns and engineering principles.
- **Activity Log**: Automatically tracked in [`JOURNAL.md`](./JOURNAL.md).
- **Dual Execution**: Runs both in the cloud via GitHub Actions and locally via `local_runner.sh`.

---

## 🛠️ Project Structure

```text
├── .github/
│   └── workflows/
│       └── daily-push.yml     # Automated cloud cron pipeline
├── algorithms/                # Algorithmic implementations & tests
├── patterns/                  # Design and resiliency patterns
├── notes/                     # Engineering notes & documentation
├── generator.py               # Core generator engine
├── JOURNAL.md                 # Daily activity index log
├── local_runner.sh            # Local runner for macOS / Linux
└── README.md
```

---

## 🚀 Usage

### 1. Cloud (GitHub Actions)
The workflow runs automatically every day at `09:15 UTC` (customizable in `.github/workflows/daily-push.yml`). You can also trigger it manually anytime under the **Actions** tab on GitHub (`workflow_dispatch`).

### 2. Local Manual Trigger
```bash
./local_runner.sh
```

### 3. Running Tests
```bash
python3 -m unittest discover -s . -p "test_*.py"
```
