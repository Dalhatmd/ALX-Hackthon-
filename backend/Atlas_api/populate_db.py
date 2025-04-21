#!/usr/bin/python3
import os
import django
import random
import pytz
from datetime import datetime, timedelta, time
from decimal import Decimal
from django.core.files import File
from django.utils import timezone
from django.db import transaction

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Atlas_api.settings')
django.setup()

# Import models after Django setup
from django.contrib.auth import get_user_model
from workspaces.models import Workspace, WorkspaceType, Amenity
from bookings.models import Booking
from notifications.models import Notification  # Update to your actual app name

User = get_user_model()

# Clear existing data (optional - comment out if you don't want to clear data)
print("Clearing existing data...")
Notification.objects.all().delete()
Booking.objects.all().delete()
Workspace.objects.all().delete()
WorkspaceType.objects.all().delete()
Amenity.objects.all().delete()
User.objects.filter(is_superuser=False).delete()  # Don't delete superusers

@transaction.atomic
def create_sample_data():
    print("Creating sample data...")
    
    # Create user data
    print("Creating users...")
    users = {
        'owners': [],
        'admins': [],
        'general': [],
        'employees': []
    }
    print("Creating teams...")
    teams = []
    team_names = [
        "Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliet"
    ]

    available_leaders = users['employees'] + users['admins']

    for name in team_names:
        if not available_leaders:
            break  # No more leaders available

        leader = available_leaders.pop()  # assign leader

        team = Team.objects.create(
            name=f"Team {name}",
            description=f"Team {name} specializing in workspace excellence.",
            leader=leader
        )

        teams.append(team)
        print(f"Created team: {team.name} led by {leader.email}")
    
    # Create 5 workspace owners
    for i in range(1, 6):
        owner = User.objects.create_user(
            email=f'owner{i}@example.com',
            password='password123',
            phone=f'555-000-{1000+i}',
            user_type=User.UserType.OWNER
        )
        users['owners'].append(owner)
        print(f"Created owner: {owner.email}")
    
    # Create 3 admins
    for i in range(1, 4):
        admin = User.objects.create_user(
            email=f'admin{i}@example.com',
            password='password123',
            phone=f'555-001-{1000+i}',
            user_type=User.UserType.ADMIN
        )
        users['admins'].append(admin)
        print(f"Created admin: {admin.email}")
    
    # Create 10 general users
    for i in range(1, 11):
        general = User.objects.create_user(
            email=f'user{i}@example.com',
            password='password123',
            phone=f'555-002-{1000+i}',
            user_type=User.UserType.GENERAL
        )
        users['general'].append(general)
        print(f"Created general user: {general.email}")
    
    # Create 7 employees
    for i in range(1, 8):
        employee = User.objects.create_user(
            email=f'employee{i}@example.com',
            password='password123',
            phone=f'555-003-{1000+i}',
            user_type=User.UserType.EMPLOYEE
        )
        users['employees'].append(employee)
        print(f"Created employee: {employee.email}")
    
    # Create workspace types
    print("Creating workspace types...")
    workspace_types = [
        WorkspaceType.objects.create(name="Private Office", description="Fully enclosed private workspace"),
        WorkspaceType.objects.create(name="Open Desk", description="Hot desk in open area"),
        WorkspaceType.objects.create(name="Meeting Room", description="Conference room for meetings"),
        WorkspaceType.objects.create(name="Event Space", description="Large space for events"),
        WorkspaceType.objects.create(name="Quiet Zone", description="Silent working area")
    ]
    
    # Create amenities
    print("Creating amenities...")
    amenities = [
        Amenity.objects.create(name="High-Speed WiFi", description="Fast internet connection", icon="wifi"),
        Amenity.objects.create(name="Coffee Machine", description="Free coffee", icon="coffee"),
        Amenity.objects.create(name="Printer", description="Printing services", icon="print"),
        Amenity.objects.create(name="Whiteboard", description="For brainstorming", icon="edit"),
        Amenity.objects.create(name="Monitor", description="External displays", icon="desktop"),
        Amenity.objects.create(name="Standing Desk", description="Adjustable height desk", icon="table"),
        Amenity.objects.create(name="Kitchen Access", description="Full kitchen facilities", icon="utensils"),
        Amenity.objects.create(name="Parking", description="On-site parking", icon="car")
    ]
    
    # Create workspaces
    print("Creating workspaces...")
    locations = [
        "Downtown", "West End", "East Side", "Financial District", 
        "Tech Park", "University Area", "Suburban Mall"
    ]
    
    workspaces = []
    
    for i in range(20):  # Create 20 workspaces
        owner = random.choice(users['owners'])
        workspace_type = random.choice(workspace_types)
        location = random.choice(locations)
        
        # Randomize opening hours
        hour_options = [(time(8, 0), time(18, 0)),  # 8am - 6pm
                        (time(9, 0), time(17, 0)),   # 9am - 5pm
                        (time(7, 0), time(19, 0)),   # 7am - 7pm
                        (time(0, 0), time(23, 59))]  # 24 hours
        
        opening_time, closing_time = random.choice(hour_options)
        
        # Create workspace
        workspace = Workspace.objects.create(
            owner=owner,
            name=f"{location} {workspace_type.name} {i+1}",
            description=f"A great {workspace_type.name.lower()} located in {location}",
            is_available=random.choice([True, True, True, False]),  # 75% available
            opening_time=opening_time,
            closing_time=closing_time,
            location=location,
            address=f"{random.randint(100, 999)} Main St, {location}",
            max_capacity=random.randint(5, 50),
            min_capacity=random.randint(1, 4),
            workspace_type=workspace_type,
            price_per_hour=Decimal(str(random.randint(15, 100)))
        )
        
        # Add random amenities
        num_amenities = random.randint(2, len(amenities))
        selected_amenities = random.sample(amenities, num_amenities)
        workspace.amenities.set(selected_amenities)
        
        workspaces.append(workspace)
        print(f"Created workspace: {workspace.name}")
    
    # Create bookings
    print("Creating bookings...")
    
    # Create dates for past, current, and future bookings
    past_dates = [(timezone.now() - timedelta(days=x)) for x in range(1, 30)]
    future_dates = [(timezone.now() + timedelta(days=x)) for x in range(0, 30)]
    
    # Booking durations
    durations = [1, 2, 3, 4, 8]  # hours
    
    bookings = []
    
    # Create past bookings (mostly completed)
    for _ in range(50):  # 50 past bookings
        user = random.choice(users['general'] + users['employees'] + users['admins'])
        workspace = random.choice(workspaces)
        
        booking_date = random.choice(past_dates)
        
        # Set time to a hour within workspace opening hours
        if workspace.opening_time < workspace.closing_time:
            # Normal hours e.g. 9am-5pm
            hour_range = range(workspace.opening_time.hour, workspace.closing_time.hour - 1)
        else:
            # Overnight hours
            hour_range = list(range(workspace.opening_time.hour, 24)) + list(range(0, workspace.closing_time.hour - 1))
        
        start_hour = random.choice(list(hour_range)) if hour_range else workspace.opening_time.hour
        duration = random.choice(durations)
        
        # Create start and end times
        start_time = booking_date.replace(hour=start_hour, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=duration)
        
        # Most past bookings are completed, some cancelled
        status = random.choices(
            [Booking.Status.COMPLETED, Booking.Status.CANCELLED],
            weights=[0.8, 0.2]
        )[0]
        
        # Create booking (signal will create BOOKING_CREATED notification)
        try:
            # Save with an initial status
            booking = Booking(
                user=user,
                workspace=workspace,
                start_time=start_time,
                end_time=end_time,
                status=Booking.Status.PENDING,  # Start with pending
                notes=f"Past booking for {workspace.name}" if random.random() > 0.5 else ""
            )
            booking.save()
            
            # Then update to final status to trigger notification
            booking.status = status
            booking.save()
            
            bookings.append(booking)
            print(f"Created past booking: {booking}")
        except Exception as e:
            print(f"Error creating past booking: {e}")
    
    # Create future bookings (mix of pending and confirmed)
    for _ in range(30):  # 30 future bookings
        user = random.choice(users['general'] + users['employees'] + users['admins'])
        workspace = random.choice(workspaces)
        
        booking_date = random.choice(future_dates)
        
        # Set time to a hour within workspace opening hours
        if workspace.opening_time < workspace.closing_time:
            # Normal hours e.g. 9am-5pm
            hour_range = range(workspace.opening_time.hour, workspace.closing_time.hour - 1)
        else:
            # Overnight hours
            hour_range = list(range(workspace.opening_time.hour, 24)) + list(range(0, workspace.closing_time.hour - 1))
        
        start_hour = random.choice(list(hour_range)) if hour_range else workspace.opening_time.hour
        duration = random.choice(durations)
        
        # Create start and end times
        start_time = booking_date.replace(hour=start_hour, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=duration)
        
        # Most future bookings are confirmed or pending
        status = random.choices(
            [Booking.Status.CONFIRMED, Booking.Status.PENDING],
            weights=[0.6, 0.4]
        )[0]
        
        # Create booking (signal will create BOOKING_CREATED notification)
        try:
            booking = Booking(
                user=user,
                workspace=workspace,
                start_time=start_time,
                end_time=end_time,
                status=Booking.Status.PENDING,  # Start with pending
                notes=f"Future booking for {workspace.name}" if random.random() > 0.5 else ""
            )
            booking.save()
            
            # For confirmed bookings, update status to trigger notification
            if status == Booking.Status.CONFIRMED:
                booking.status = status
                booking.save()
            
            bookings.append(booking)
            print(f"Created future booking: {booking}")
        except Exception as e:
            print(f"Error creating future booking: {e}")
    
    # Create additional reminder notifications (normally these would be created by the scheduled task)
    print("Creating reminder notifications...")
    future_bookings = [b for b in bookings if b.start_time > timezone.now() and b.status == Booking.Status.CONFIRMED]
    for booking in future_bookings[:15]:  # Add reminders for some future bookings
        # Create reminder notification
        Notification.objects.create(
            user=booking.user,
            booking=booking,
            notification_type=Notification.Type.BOOKING_REMINDER,
            message=f"Reminder: You have a booking for {booking.workspace.name} starting at {booking.start_time.strftime('%Y-%m-%d %H:%M')}"
        )
        print(f"Created reminder notification for booking: {booking}")
    
    # Set some notifications as read
    print("Setting some notifications as read...")
    all_notifications = Notification.objects.all()
    for notification in random.sample(list(all_notifications), k=int(all_notifications.count() * 0.4)):
        notification.mark_as_read()
        print(f"Marked notification as read: {notification}")

if __name__ == "__main__":
    create_sample_data()
    print("Database population complete!")
