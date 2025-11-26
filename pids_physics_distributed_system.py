"""
PIDS: Physics-Inspired Distributed System

A distributed task coordination system that uses gravitational physics
for autonomous load balancing.

Author: Jose
License: MIT
"""

import redis
import json
import time
import uuid
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Task:
    """Represents a task to be processed."""
    id: str
    weight: float
    data: Optional[Dict] = None

    def __repr__(self):
        return f"Task(id={self.id}, weight={self.weight:.2f})"


class PhysicsLoadBalancer:
    """
    Calculates gravitational forces for load balancing.

    Uses Newton's law of gravity: F = G * (m1 * m2) / r²
    where:
    - m1 = worker load (mass)
    - m2 = task weight (mass)
    - r = distance (constant for simplicity)
    - G = gravitational constant (tuning parameter)
    """

    def __init__(self, G: float = 1.0, distance_offset: float = 1.0):
        """
        Initialize physics-based load balancer.

        Args:
            G: Gravitational constant (higher = stronger repulsion)
            distance_offset: Prevents division by zero, smooths forces
        """
        self.G = G
        self.distance_offset = distance_offset

    def calculate_force(self, worker_load: float, task_weight: float,
                       distance: float = 1.0) -> float:
        """
        Calculate gravitational force between worker and task.

        High load + heavy task = HIGH force = REPEL
        Low load + light task = LOW force = ATTRACT

        Args:
            worker_load: Current load of worker
            task_weight: Weight of task
            distance: Distance between worker and task

        Returns:
            Gravitational force (higher = more repulsion)
        """
        force = (self.G * worker_load * task_weight) / \
                ((distance + self.distance_offset) ** 2)
        return force

    def calculate_threshold(self, avg_load: float, task_weight: float) -> float:
        """
        Calculate dynamic threshold for claiming tasks.

        Workers claim task if force < threshold.

        Args:
            avg_load: Average load across all workers
            task_weight: Weight of task being considered

        Returns:
            Force threshold
        """
        # Threshold scales with average load and task weight
        # 0.8 factor means workers claim if force is < 80% of expected
        return avg_load * task_weight * 0.8

    def should_claim(self, worker_load: float, task_weight: float,
                    avg_load: float, distance: float = 1.0) -> bool:
        """
        Decide whether worker should claim task.

        Args:
            worker_load: Current load of worker
            task_weight: Weight of task
            avg_load: Average load across all workers
            distance: Distance to task

        Returns:
            True if worker should claim task
        """
        force = self.calculate_force(worker_load, task_weight, distance)
        threshold = self.calculate_threshold(avg_load, task_weight)

        return force < threshold


class Worker:
    """
    Autonomous worker that claims and processes tasks.
    """

    def __init__(self, worker_id: str, capacity: float = 100.0):
        """
        Initialize worker.

        Args:
            worker_id: Unique identifier
            capacity: Maximum load capacity
        """
        self.worker_id = worker_id
        self.capacity = capacity
        self.current_load = 0.0
        self.claimed_tasks: Set[str] = set()
        self.completed_tasks: Dict[str, any] = {}

    def claim_task(self, task: Task) -> bool:
        """
        Claim a task (add to claimed set).

        Args:
            task: Task to claim

        Returns:
            True if claimed successfully
        """
        if task.id in self.claimed_tasks:
            return False

        if self.current_load + task.weight > self.capacity:
            logger.warning(f"{self.worker_id} at capacity, can't claim {task.id}")
            return False

        self.claimed_tasks.add(task.id)
        self.current_load += task.weight
        logger.info(f"{self.worker_id} claimed {task.id} "
                   f"[Load: {self.current_load - task.weight:.1f} → {self.current_load:.1f}]")
        return True

    def process_task(self, task: Task) -> Dict:
        """
        Process a task (simulate work).

        Args:
            task: Task to process

        Returns:
            Task result
        """
        if task.id not in self.claimed_tasks:
            raise ValueError(f"Task {task.id} not claimed by {self.worker_id}")

        # Simulate processing
        time.sleep(0.01)  # 10ms of "work"

        result = {
            'task_id': task.id,
            'worker_id': self.worker_id,
            'result': f'Processed by {self.worker_id}',
            'timestamp': time.time()
        }

        self.completed_tasks[task.id] = result
        logger.info(f"{self.worker_id} completed {task.id}")

        return result

    def release_task(self, task_id: str):
        """Release a claimed task (if failed or timeout)."""
        if task_id in self.claimed_tasks:
            self.claimed_tasks.remove(task_id)
            # Note: current_load not decreased here
            # In real system, need to track task weights
            logger.info(f"{self.worker_id} released {task_id}")

    def __repr__(self):
        return f"Worker(id={self.worker_id}, load={self.current_load:.1f}/{self.capacity})"


class DistributedTaskSystem:
    """
    Coordinates workers using Redis for communication.
    """

    def __init__(self, redis_url: str = 'redis://localhost:6379'):
        """
        Initialize distributed system.

        Args:
            redis_url: Redis connection URL
        """
        self.redis = redis.from_url(redis_url)
        self.pubsub = self.redis.pubsub()
        self.workers: Dict[str, Worker] = {}
        self.tasks: Dict[str, Task] = {}
        self.claims: Dict[str, Dict] = {}  # task_id -> claim info

        # Subscribe to claim channel
        self.pubsub.subscribe('task_claims')

        logger.info(f"Connected to Redis at {redis_url}")

    def add_worker(self, worker: Worker):
        """Add worker to system."""
        self.workers[worker.worker_id] = worker
        logger.info(f"Added {worker}")

    def add_task(self, task: Task):
        """Add task to pool."""
        self.tasks[task.id] = task
        logger.debug(f"Added {task}")

    def broadcast_claim(self, worker_id: str, task_id: str):
        """
        Broadcast task claim to all workers (async).

        Args:
            worker_id: ID of worker claiming task
            task_id: ID of task being claimed
        """
        message = {
            'type': 'CLAIM',
            'worker': worker_id,
            'task': task_id,
            'timestamp': time.time()
        }

        self.redis.publish('task_claims', json.dumps(message))
        self.claims[task_id] = message

        logger.debug(f"Broadcasted claim: {worker_id} → {task_id}")

    def store_result(self, task_id: str, result: Dict):
        """
        Store task result in Redis.

        Args:
            task_id: Task ID
            result: Task result data
        """
        key = f'result:{task_id}'
        self.redis.set(key, json.dumps(result))
        logger.debug(f"Stored result for {task_id}")

    def fetch_result(self, task_id: str) -> Optional[Dict]:
        """
        Fetch task result (lazy).

        Args:
            task_id: Task ID

        Returns:
            Task result or None if not found
        """
        key = f'result:{task_id}'
        result = self.redis.get(key)

        if result:
            return json.loads(result)
        return None

    def is_task_claimed(self, task_id: str) -> bool:
        """Check if task is already claimed."""
        return task_id in self.claims

    def get_avg_load(self) -> float:
        """Calculate average load across all workers."""
        if not self.workers:
            return 0.0
        return sum(w.current_load for w in self.workers.values()) / len(self.workers)

    def assign_tasks(self, balancer: PhysicsLoadBalancer):
        """
        Assign tasks to workers using physics-based balancing.

        Args:
            balancer: PhysicsLoadBalancer instance
        """
        avg_load = self.get_avg_load()

        for task in self.tasks.values():
            if self.is_task_claimed(task.id):
                continue

            # Each worker decides independently
            for worker in self.workers.values():
                if balancer.should_claim(
                    worker.current_load,
                    task.weight,
                    avg_load
                ):
                    if worker.claim_task(task):
                        self.broadcast_claim(worker.worker_id, task.id)
                        break

            # Recalculate avg_load after each assignment
            avg_load = self.get_avg_load()

    def process_all_tasks(self):
        """Process all claimed tasks."""
        for worker in self.workers.values():
            for task_id in list(worker.claimed_tasks):
                task = self.tasks.get(task_id)
                if task:
                    result = worker.process_task(task)
                    self.store_result(task_id, result)

    def get_statistics(self) -> Dict:
        """
        Calculate system statistics.

        Returns:
            Dict with balance score, load distribution, etc.
        """
        if not self.workers:
            return {}

        loads = [w.current_load for w in self.workers.values()]
        avg_load = sum(loads) / len(loads)

        # Standard deviation
        variance = sum((load - avg_load) ** 2 for load in loads) / len(loads)
        std_dev = variance ** 0.5

        # Balance score: 100% = perfect balance
        balance_score = 100 * (1 - std_dev / avg_load) if avg_load > 0 else 100

        # Task assignment rate
        total_tasks = len(self.tasks)
        claimed_tasks = len(self.claims)
        assignment_rate = (claimed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        return {
            'total_tasks': total_tasks,
            'claimed_tasks': claimed_tasks,
            'assignment_rate': assignment_rate,
            'avg_load': avg_load,
            'std_dev': std_dev,
            'balance_score': balance_score,
            'max_load': max(loads) if loads else 0,
            'min_load': min(loads) if loads else 0,
            'num_workers': len(self.workers)
        }

    def cleanup(self):
        """Cleanup Redis connections."""
        self.pubsub.close()
        self.redis.close()


def main():
    """Example usage of PIDS."""

    # Initialize system
    system = DistributedTaskSystem()
    balancer = PhysicsLoadBalancer(G=1.0, distance_offset=1.0)

    # Create workers
    for i in range(5):
        worker = Worker(f'worker-{i+1}', capacity=100.0)
        system.add_worker(worker)

    # Create tasks with varying weights
    import random
    random.seed(42)

    for i in range(50):
        task = Task(
            id=f'task-{i+1}',
            weight=random.uniform(1.0, 10.0)
        )
        system.add_task(task)

    # Assign tasks
    logger.info("\n=== Task Assignment ===")
    system.assign_tasks(balancer)

    # Process tasks
    logger.info("\n=== Processing Tasks ===")
    system.process_all_tasks()

    # Statistics
    stats = system.get_statistics()
    logger.info("\n=== Final Statistics ===")
    logger.info(f"Total Tasks: {stats['total_tasks']}")
    logger.info(f"Claimed: {stats['claimed_tasks']} ({stats['assignment_rate']:.1f}%)")
    logger.info(f"Balance Score: {stats['balance_score']:.1f}%")
    logger.info(f"Avg Load: {stats['avg_load']:.1f} ± {stats['std_dev']:.2f}")
    logger.info(f"Load Range: [{stats['min_load']:.1f}, {stats['max_load']:.1f}]")

    # Cleanup
    system.cleanup()


if __name__ == '__main__':
    main()
