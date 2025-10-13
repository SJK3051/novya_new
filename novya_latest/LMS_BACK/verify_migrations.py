#!/usr/bin/env python
"""
Script to verify all migrations are applied
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db.migrations.executor import MigrationExecutor
from django.db import connection

def check_migrations():
    """Check if all migrations are applied"""
    
    print("🔍 Checking Migration Status")
    print("=" * 60)
    
    executor = MigrationExecutor(connection)
    plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
    
    if plan:
        print("\n❌ Unapplied Migrations Found:")
        for migration, backwards in plan:
            print(f"  - {migration.app_label}.{migration.name}")
        print(f"\nTotal unapplied: {len(plan)}")
        return False
    else:
        print("\n✅ All Migrations Applied Successfully!")
        print("\nNo pending migrations found.")
        
        # Show applied migrations summary
        applied = executor.loader.applied_migrations
        print(f"\nTotal Applied Migrations: {len(applied)}")
        
        # Count by app
        apps = {}
        for app, name in applied:
            apps[app] = apps.get(app, 0) + 1
        
        print("\n📊 Migrations by App:")
        for app, count in sorted(apps.items()):
            print(f"  - {app}: {count} migrations")
        
        return True

if __name__ == "__main__":
    success = check_migrations()
    exit(0 if success else 1)

