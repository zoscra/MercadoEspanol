# 🛠️ PIDS - Setup & Installation Guide

## Prerequisites

### Required Software
- **Python**: 3.8+ (3.9+ recommended)
- **Redis**: 6.0+ (for Pub/Sub and data storage)
- **Git**: For cloning and version control
- **pip**: Python package manager

### System Requirements
- **OS**: Linux, macOS, or Windows (WSL recommended)
- **RAM**: 2GB minimum, 4GB recommended
- **Disk**: 100MB for project + dependencies

---

## Quick Installation (5 minutes)

### Option 1: Docker (Recommended)

```bash
# 1. Install Redis via Docker
docker run -d \
  --name pids-redis \
  -p 6379:6379 \
  redis:alpine

# 2. Clone repository
git clone https://github.com/yourusername/pids.git
cd pids

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Test installation
python quick_start.py
```

### Option 2: Native Installation

#### Linux (Ubuntu/Debian)
```bash
# Install Redis
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis

# Verify Redis
redis-cli ping  # Should return "PONG"

# Clone and setup
git clone https://github.com/yourusername/pids.git
cd pids
pip install -r requirements.txt
python quick_start.py
```

#### macOS
```bash
# Install Redis via Homebrew
brew install redis
brew services start redis

# Verify Redis
redis-cli ping  # Should return "PONG"

# Clone and setup
git clone https://github.com/yourusername/pids.git
cd pids
pip install -r requirements.txt
python quick_start.py
```

#### Windows (WSL)
```bash
# Install WSL first (if not already)
wsl --install

# Inside WSL, follow Linux instructions above
sudo apt update
sudo apt install redis-server python3 python3-pip
redis-server --daemonize yes
python3 -m pip install -r requirements.txt
python3 quick_start.py
```

---

## Detailed Setup

### Step 1: Redis Installation

#### Verify Redis is Running
```bash
redis-cli ping
# Expected: PONG
```

#### Check Redis Port
```bash
redis-cli -p 6379 info server
# Should show Redis version and uptime
```

#### Configure Redis (Optional)
Edit `/etc/redis/redis.conf`:
```conf
# Allow remote connections (use with caution)
bind 0.0.0.0

# Set max memory (optional)
maxmemory 256mb
maxmemory-policy allkeys-lru

# Enable persistence (optional)
save 900 1
save 300 10
```

Restart Redis:
```bash
sudo systemctl restart redis
```

---

### Step 2: Python Environment

#### Create Virtual Environment (Recommended)
```bash
python3 -m venv pids-env
source pids-env/bin/activate  # Linux/macOS
# pids-env\Scripts\activate.bat  # Windows
```

#### Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**requirements.txt contents:**
```txt
redis>=4.5.0
numpy>=1.24.0
matplotlib>=3.7.0
pytest>=7.4.0
```

#### Verify Installation
```python
python -c "import redis; import numpy; import matplotlib; print('All dependencies installed!')"
```

---

### Step 3: Configuration

#### Environment Variables (Optional)
Create `.env` file:
```bash
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=  # Leave empty if no auth

# PIDS Configuration
WORKER_COUNT=5
TASK_COUNT=100
GRAVITATIONAL_CONSTANT=1.0
DISTANCE_OFFSET=1.0
CLAIM_TIMEOUT=60
```

Load in Python:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

### Step 4: Run First Demo

```bash
python quick_start.py
```

**Expected Output:**
```
🚀 PIDS Quick Start Demo
========================
Starting Redis connection...
✓ Connected to Redis at localhost:6379

Initializing workers...
✓ Worker-1 online [Capacity: 100.0, Load: 0.0]
✓ Worker-2 online [Capacity: 100.0, Load: 0.0]
✓ Worker-3 online [Capacity: 100.0, Load: 0.0]

Generating 50 tasks...
✓ Created 50 tasks (weights: 1.0-10.0)

Task assignment in progress...
  [Worker-1] Claimed Task-1 (weight: 5.2) [Load: 0.0 → 5.2]
  [Worker-2] Claimed Task-2 (weight: 3.8) [Load: 0.0 → 3.8]
  ...

Final Statistics:
  Total Tasks: 50
  Assigned: 48 (96.0%)
  Balance Score: 94.2%
  Avg Load: 16.5 ± 0.85
  Max Load: 18.2 (Worker-3)
  Min Load: 14.8 (Worker-1)

✓ Demo completed successfully!
```

---

## Running Examples

### Example 1: Basic Simulation (No Redis)
```bash
python test_physics_distributed.py -k test_simulation
```

### Example 2: Benchmark Comparison
```bash
python benchmark_comparison.py
```

Output:
```
=== PIDS Benchmark Comparison ===

Algorithm: Gravitational
  Balance Score: 94.2%
  Std Dev: ±0.85
  Avg Assignment Time: 1.2ms

Algorithm: Least-Loaded
  Balance Score: 91.5%
  Std Dev: ±1.20
  Avg Assignment Time: 0.8ms

Algorithm: Round-Robin
  Balance Score: 82.4%
  Std Dev: ±2.50
  Avg Assignment Time: 0.5ms

Algorithm: Random
  Balance Score: 76.8%
  Std Dev: ±3.80
  Avg Assignment Time: 0.3ms

Winner: Gravitational (12% better than Round-Robin)
```

### Example 3: Visualizations
```bash
python visualize.py
```

Generates:
- `load_distribution.png` - Bar chart of worker loads
- `force_field.png` - Heatmap of gravitational forces
- `task_timeline.png` - Task assignment over time

---

## Advanced Configuration

### Tuning Physics Parameters

#### Gravitational Constant (`G`)
```python
# Higher G → stronger repulsion (more aggressive balancing)
G = 2.0  # Default: 1.0

# Effect:
# - G = 0.5: Mild balancing (faster, less balanced)
# - G = 1.0: Moderate balancing (recommended)
# - G = 2.0: Aggressive balancing (slower, very balanced)
```

#### Distance Offset (`d_offset`)
```python
# Higher offset → smoother force transitions
d_offset = 2.0  # Default: 1.0

# Effect:
# - d_offset = 0.5: Sharp force changes
# - d_offset = 1.0: Moderate smoothing
# - d_offset = 2.0: Very smooth (slower convergence)
```

#### Force Threshold
```python
# Higher threshold → more selective claiming
threshold = 5.0  # Default: calculated dynamically

# Effect:
# - Low threshold: Workers claim tasks easily
# - High threshold: Workers reject many tasks (slower assignment)
```

### Scaling Workers

#### Horizontal Scaling
```python
# Run workers on different machines
# Machine 1:
worker1 = Worker("worker-1", capacity=100, redis_url="redis://redis-server:6379")

# Machine 2:
worker2 = Worker("worker-2", capacity=100, redis_url="redis://redis-server:6379")

# All workers connect to same Redis instance
```

#### Vertical Scaling
```python
# Adjust capacity based on hardware
worker_weak = Worker("worker-1", capacity=50)   # 2 cores, 4GB RAM
worker_strong = Worker("worker-2", capacity=200) # 8 cores, 16GB RAM

# Tasks distribute proportionally
```

---

## Troubleshooting

### Issue 1: Redis Connection Failed

**Error:**
```
redis.exceptions.ConnectionError: Error connecting to localhost:6379
```

**Solutions:**
```bash
# Check if Redis is running
sudo systemctl status redis

# Start Redis
sudo systemctl start redis

# Check Redis logs
sudo journalctl -u redis -n 50

# Test connection
redis-cli ping
```

### Issue 2: Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'redis'
```

**Solutions:**
```bash
# Verify pip installation
pip list | grep redis

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version  # Should be 3.8+
```

### Issue 3: Slow Performance

**Symptoms:**
- Task assignment takes >5 seconds
- High CPU usage
- Redis memory full

**Solutions:**
```bash
# Reduce worker/task count in demos
python quick_start.py --workers 3 --tasks 20

# Clear Redis data
redis-cli FLUSHALL

# Check Redis memory
redis-cli INFO memory

# Increase Redis max memory
redis-cli CONFIG SET maxmemory 512mb
```

### Issue 4: Port Already in Use

**Error:**
```
Address already in use: 6379
```

**Solutions:**
```bash
# Find process using port
sudo lsof -i :6379

# Kill process
sudo kill -9 <PID>

# Or use different port
python quick_start.py --redis-port 6380
```

---

## Testing

### Run All Tests
```bash
pytest test_physics_distributed.py -v
```

### Run Specific Test
```bash
pytest test_physics_distributed.py::test_gravitational_force -v
```

### Run with Coverage
```bash
pytest test_physics_distributed.py --cov=physics_distributed_system --cov-report=html
open htmlcov/index.html
```

### Expected Test Results
```
test_physics_distributed.py::test_worker_init PASSED          [ 10%]
test_physics_distributed.py::test_task_creation PASSED        [ 20%]
test_physics_distributed.py::test_gravitational_force PASSED  [ 30%]
test_physics_distributed.py::test_claim_task PASSED           [ 40%]
test_physics_distributed.py::test_conflict_resolution PASSED  [ 50%]
test_physics_distributed.py::test_load_balancing PASSED       [ 60%]
test_physics_distributed.py::test_timeout_handling PASSED     [ 70%]
test_physics_distributed.py::test_benchmark PASSED            [ 80%]
test_physics_distributed.py::test_visualization PASSED        [ 90%]
test_physics_distributed.py::test_integration PASSED          [100%]

========== 10 passed in 5.23s ==========
```

---

## Production Deployment

### Docker Compose Setup

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  pids-worker-1:
    build: .
    depends_on:
      - redis
    environment:
      - REDIS_HOST=redis
      - WORKER_ID=worker-1
      - WORKER_CAPACITY=100
    command: python worker.py

  pids-worker-2:
    build: .
    depends_on:
      - redis
    environment:
      - REDIS_HOST=redis
      - WORKER_ID=worker-2
      - WORKER_CAPACITY=100
    command: python worker.py

volumes:
  redis_data:
```

Run:
```bash
docker-compose up -d
docker-compose logs -f
```

### Kubernetes Deployment

Create `deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pids-worker
spec:
  replicas: 5
  selector:
    matchLabels:
      app: pids-worker
  template:
    metadata:
      labels:
        app: pids-worker
    spec:
      containers:
      - name: worker
        image: pids:latest
        env:
        - name: REDIS_HOST
          value: redis-service
        - name: WORKER_CAPACITY
          value: "100"
---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  selector:
    app: redis
  ports:
  - port: 6379
```

Deploy:
```bash
kubectl apply -f deployment.yaml
kubectl get pods
kubectl logs -f pids-worker-xxxxx
```

---

## Performance Tuning

### For High Throughput
```python
# Increase worker count
workers = 50

# Reduce force calculation complexity
use_simple_distance = True

# Batch task assignments
batch_size = 100
```

### For Low Latency
```python
# Reduce claim timeout
claim_timeout = 10  # seconds

# Use faster Redis connection
redis_pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=100
)
```

### For High Task Count
```python
# Use Redis Streams instead of Pub/Sub
redis.xadd('tasks', {'task_id': task_id, 'weight': weight})

# Implement task partitioning
partition = hash(task_id) % num_partitions
```

---

## Next Steps

After successful setup:

1. **Customize**: Edit `quick_start.py` parameters
2. **Experiment**: Run benchmarks, change physics constants
3. **Visualize**: Generate graphs, analyze patterns
4. **Extend**: Add new force models, fault tolerance
5. **Document**: Blog post, conference talk

---

## Resources

- **Redis Documentation**: https://redis.io/docs/
- **Python Threading**: https://docs.python.org/3/library/threading.html
- **Distributed Systems**: https://www.distributed-systems.net/
- **Physics Algorithms**: https://en.wikipedia.org/wiki/Gravitational_algorithm

---

## Support

- **GitHub Issues**: Report bugs, request features
- **Discussions**: Ask questions, share ideas
- **Email**: [maintainer@example.com]

---

**Setup complete? Go to [README.md](README.md) for architecture details!** 🚀
