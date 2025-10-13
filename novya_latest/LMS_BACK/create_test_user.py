#!/usr/bin/env python3
"""
Create test users for NOVYA LMS
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from authentication.models import User, Class, Parent, Student

def create_test_users():
    """Create test users for development"""
    
    # Create a test class
    test_class, created = Class.objects.get_or_create(
        class_name="Class 7",
        defaults={'class_name': 'Class 7'}
    )
    print(f"Class: {'Created' if created else 'Exists'} - {test_class.class_name}")
    
    # Create test student user
    student_user, created = User.objects.get_or_create(
        username='student123',
        defaults={
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'student@test.com',
            'phonenumber': '9876543210',
            'role': 'Student',
            'password': 'pbkdf2_sha256$600000$dummy$dummy'  # This will be hashed properly
        }
    )
    
    if created:
        student_user.set_password('studentpass')
        student_user.save()
        print(f"Student user created: {student_user.username}")
    else:
        print(f"Student user exists: {student_user.username}")
    
    # Create test parent user
    parent_user, created = User.objects.get_or_create(
        username='parent456',
        defaults={
            'firstname': 'Jane',
            'lastname': 'Doe',
            'email': 'parent@test.com',
            'phonenumber': '9876543211',
            'role': 'Parent',
            'password': 'pbkdf2_sha256$600000$dummy$dummy'  # This will be hashed properly
        }
    )
    
    if created:
        parent_user.set_password('parentpass')
        parent_user.save()
        print(f"Parent user created: {parent_user.username}")
    else:
        print(f"Parent user exists: {parent_user.username}")
    
    # Create parent profile
    parent_profile, created = Parent.objects.get_or_create(
        parent_id=parent_user,
        defaults={'parent_id': parent_user}
    )
    print(f"Parent profile: {'Created' if created else 'Exists'}")
    
    # Create student profile
    student_profile, created = Student.objects.get_or_create(
        student_id=student_user,
        defaults={
            'student_id': student_user,
            'class_id': test_class,
            'parent_id': parent_profile
        }
    )
    print(f"Student profile: {'Created' if created else 'Exists'}")
    
    print("\n" + "="*50)
    print("TEST USERS CREATED SUCCESSFULLY!")
    print("="*50)
    print("Student Login:")
    print("  Username: student123")
    print("  Password: studentpass")
    print("\nParent Login:")
    print("  Username: parent456")
    print("  Password: parentpass")
    print("="*50)

if __name__ == '__main__':
    create_test_users()

