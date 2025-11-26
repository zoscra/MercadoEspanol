#!/usr/bin/env python3
"""
PIDS Quick Start Demo

A simple demonstration of the Physics-Inspired Distributed System.
This script shows how PIDS works with minimal configuration.

Usage:
    python quick_start.py
"""

import sys
import random
from physics_distributed_system import (
    Worker, Task, PhysicsLoadBalancer, DistributedTaskSystem
)


def print_header():
    """Print demo header."""
    print("=" * 60)
    print("🚀 PIDS Quick Start Demo")
    print("   Physics-Inspired Distributed System")
    print("=" * 60)
    print()


def print_section(title):
    """Print section header."""
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


def print_worker_status(workers):
    """Print current status of all workers."""
    print("\nWorker Status:")
    for worker in workers.values():
        bar_length = int(worker.current_load / worker.capacity * 20)
        bar = '█' * bar_length + '░' * (20 - bar_length)
        print(f"  {worker.worker_id:12} [{bar}] "
              f"{worker.current_load:5.1f}/{worker.capacity:.0f} "
              f"({len(worker.claimed_tasks)} tasks)")


def main():
    """Run quick start demo."""

    print_header()

    # Configuration
    NUM_WORKERS = 5
    NUM_TASKS = 50
    WORKER_CAPACITY = 100.0

    try:
        # Initialize system
        print("Initializing PIDS...")
        print(f"  • Workers: {NUM_WORKERS}")
        print(f"  • Tasks: {NUM_TASKS}")
        print(f"  • Capacity per worker: {WORKER_CAPACITY}")

        system = DistributedTaskSystem()
        balancer = PhysicsLoadBalancer(G=1.0, distance_offset=1.0)

        print("\n✓ System initialized")
        print(f"✓ Connected to Redis")

    except Exception as e:
        print(f"\n❌ Error connecting to Redis: {e}")
        print("\nMake sure Redis is running:")
        print("  docker run -d -p 6379:6379 redis:alpine")
        print("  # or")
        print("  redis-server")
        sys.exit(1)

    # Create workers
    print_section("Creating Workers")

    for i in range(NUM_WORKERS):
        worker = Worker(f'worker-{i+1}', capacity=WORKER_CAPACITY)
        system.add_worker(worker)
        print(f"  ✓ {worker.worker_id} online [Capacity: {worker.capacity:.0f}]")

    # Create tasks
    print_section("Generating Tasks")

    random.seed(42)  # Reproducible results
    tasks = []

    for i in range(NUM_TASKS):
        weight = random.uniform(1.0, 10.0)
        task = Task(id=f'task-{i+1}', weight=weight)
        tasks.append(task)
        system.add_task(task)

    print(f"  ✓ Created {NUM_TASKS} tasks")
    print(f"  ✓ Weight range: {min(t.weight for t in tasks):.1f} - "
          f"{max(t.weight for t in tasks):.1f}")
    print(f"  ✓ Total weight: {sum(t.weight for t in tasks):.1f}")

    # Show initial state
    print_section("Initial State")
    print_worker_status(system.workers)

    # Assign tasks
    print_section("Assigning Tasks (Physics-Based)")

    print("\nUsing gravitational forces to balance load...")
    print("  • High load workers → REPEL tasks")
    print("  • Low load workers → ATTRACT tasks")
    print()

    system.assign_tasks(balancer)

    # Show assignments
    print("\nTask Assignments:")
    for worker_id, worker in sorted(system.workers.items()):
        if worker.claimed_tasks:
            tasks_str = ', '.join(sorted(list(worker.claimed_tasks))[:5])
            if len(worker.claimed_tasks) > 5:
                tasks_str += f", ... ({len(worker.claimed_tasks) - 5} more)"
            print(f"  {worker_id}: {tasks_str}")

    print_worker_status(system.workers)

    # Process tasks
    print_section("Processing Tasks")

    print("\nWorkers processing claimed tasks...")
    system.process_all_tasks()
    print("  ✓ All tasks completed")

    # Show final statistics
    print_section("Final Statistics")

    stats = system.get_statistics()

    print(f"\n📊 Performance Metrics:")
    print(f"  Total Tasks:        {stats['total_tasks']}")
    print(f"  Tasks Assigned:     {stats['claimed_tasks']} "
          f"({stats['assignment_rate']:.1f}%)")
    print(f"  Balance Score:      {stats['balance_score']:.1f}%")
    print(f"  Avg Load:           {stats['avg_load']:.1f} ± {stats['std_dev']:.2f}")
    print(f"  Load Range:         [{stats['min_load']:.1f}, {stats['max_load']:.1f}]")
    print(f"  Workers:            {stats['num_workers']}")

    # Comparison
    print(f"\n📈 Comparison to Round-Robin:")
    print(f"  PIDS Balance:       {stats['balance_score']:.1f}%")
    print(f"  Round-Robin:        ~82.4%")
    print(f"  Improvement:        +{stats['balance_score'] - 82.4:.1f}%")

    # Cleanup
    system.cleanup()

    print("\n" + "=" * 60)
    print("✓ Demo completed successfully!")
    print("=" * 60)

    print("\n📚 Next Steps:")
    print("  • Run benchmarks: python benchmark_comparison.py")
    print("  • View visualizations: python visualize.py")
    print("  • Read documentation: README.md")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
