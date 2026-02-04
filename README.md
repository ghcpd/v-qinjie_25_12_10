# User Display System - High-Performance Refactor

This project refactors the original chaotic `user_display_original.py` into a modular, performant, and reliable system.

## Baseline Problems

The original code suffered from:
- O(n²) string concatenation and JSON serialization
- Random delays and corruption
- Linear searches for ID lookups
- Inconsistent filtering and formatting
- No error handling or validation
- Poor scalability beyond 50,000 users

## New Architecture

### Modular Structure
```
user_display/
├── __init__.py          # Package exports
├── store.py             # UserStore with sharding and indexing
├── index.py             # Indexing utilities
├── formatters/          # Output formatting (JSON, table, compact)
├── filters/             # Filtering strategies (exact, regex, composite)
├── validation/          # Data validation and repair
├── config.py            # Configuration management
├── logging_utils.py     # Structured logging
├── metrics.py           # Performance metrics
├── plugins.py           # Dynamic plugin registration
└── errors.py            # Custom exceptions
```

### Key Features
- **Performance**: O(1) ID lookups, single-pass operations, buffered I/O
- **Concurrency**: Thread-safe operations, optional parallel filtering
- **Reliability**: Validation with fallback, structured error handling
- **Extensibility**: Plugin system for custom formatters/filters/validators
- **Observability**: Structured logging and metrics collection

## API Compatibility

The `user_display_optimized.py` maintains the original API:

```python
from user_display_optimized import display_users, get_user_by_id, filter_users, export_users_to_string

# Same usage as original
users = [...]  # List of user dicts
result = display_users(users)
user = get_user_by_id(users, 123)
filtered = filter_users(users, {'role': 'Admin'})
exported = export_users_to_string(users)
```

## Performance Targets

| Operation            | Target   |
| -------------------- | -------- |
| Display 50,000 users | < 1.0 s  |
| Filter 50,000 users  | < 5.0 s  |
| ID lookup            | < 0.001 s |

## Usage Examples

### Basic Usage
```python
from user_display_optimized import display_users, filter_users

users = [
    {'id': 1, 'name': 'Alice', 'role': 'Admin'},
    {'id': 2, 'name': 'Bob', 'role': 'User'}
]

# Display in default format
print(display_users(users))

# Filter by role
admins = filter_users(users, {'role': 'Admin'})
```

### Advanced Usage
```python
from user_display import UserStore, JSONFormatter, RegexFilter

# Use the modular components
store = UserStore()
store.add_users(users)

# Custom formatting
formatter = JSONFormatter()
json_output = formatter.format_users(store.get_all_users())

# Regex filtering
regex_filter = RegexFilter({'name': r'Alice.*'})
matches = store.filter_users(regex_filter.matches)
```

### Configuration
```python
from user_display import config

config.set('parallel_filtering', True)
config.set('shard_count', 8)
config.freeze()  # Prevent further changes
```

### Plugins
```python
from user_display import registry
from user_display.formatters.base import Formatter

class CustomFormatter(Formatter):
    def format_users(self, users, **kwargs):
        return "Custom: " + str(len(users))

registry.register_formatter('custom', CustomFormatter)
```

## Plugin System

The system supports dynamic registration of:
- **Formatters**: Custom output formats
- **Filters**: New filtering strategies
- **Validators**: Data validation rules

## Testing

Run tests with:
```bash
python run_tests.py
```

Tests cover:
- Functional behavior matching original API
- All formatting modes
- Filtering strategies
- Validation and error handling
- Performance benchmarks
- Concurrency correctness

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   python run_tests.py
   ```

## Benchmarking

The system includes built-in metrics. After operations, check:
```python
from user_display import metrics
metrics.report()
```

For large-scale testing, the test suite includes 50,000-user benchmarks.