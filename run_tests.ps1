# Run tests for user display system
# This script sets up the environment and runs all tests

Write-Host "Setting up Python environment..."

# Check if Python is available
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not in PATH"
    exit 1
}

# Install requirements if requirements.txt exists
if (Test-Path "requirements.txt") {
    Write-Host "Installing requirements..."
    pip install -r requirements.txt
}

# Run tests
Write-Host "Running tests..."
python -m pytest tests/ -v --tb=short

# If pytest not available, try unittest
if ($LASTEXITCODE -ne 0) {
    Write-Host "Pytest failed, trying unittest..."
    python -m unittest discover tests/ -v
}

# Run performance benchmarks
Write-Host "Running performance benchmarks..."
python -c "
import time
from user_display_optimized import display_users, filter_users, get_user_by_id, export_users_to_string
from user_display import metrics

# Generate test data
users = [
    {
        'id': i,
        'name': f'User{i}',
        'email': f'user{i}@example.com',
        'role': 'Admin' if i % 10 == 0 else 'User',
        'status': 'Active',
        'join_date': '2023-01-01',
        'last_login': '2025-11-26'
    }
    for i in range(1, 50001)
]

print('Testing with 50,000 users...')

# Test display
start = time.time()
result = display_users(users, show_all=False)
display_time = time.time() - start
print(f'Display time: {display_time:.3f}s (target <0.120s)')

# Test filter
start = time.time()
filtered = filter_users(users, {'role': 'Admin'})
filter_time = time.time() - start
print(f'Filter time: {filter_time:.3f}s (target <0.015s)')

# Test ID lookup
start = time.time()
user = get_user_by_id(users, 25000)
lookup_time = time.time() - start
print(f'ID lookup time: {lookup_time:.6f}s (target <0.0005s)')

# Test export
start = time.time()
exported = export_users_to_string(users)
export_time = time.time() - start
print(f'Export time: {export_time:.3f}s')

print('\\nMetrics summary:')
metrics.report()
"

Write-Host "Test run complete."