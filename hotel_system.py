import os
import json
import datetime
from tabulate import tabulate
from colorama import init, Fore, Back, Style
import re

# Initialize colorama
init(autoreset=True)

class Room:
    """Room class to store room information"""
    def __init__(self, room_number, room_type, price, capacity, amenities):
        self.room_number = room_number
        self.room_type = room_type  # Standard, Deluxe, Suite, Presidential
        self.price = price
        self.capacity = capacity  # Max persons
        self.amenities = amenities  # List of amenities
        self.status = "AVAILABLE"  # AVAILABLE, BOOKED, OCCUPIED, MAINTENANCE
        self.current_guest = None
        self.check_in_date = None
        self.check_out_date = None
    
    def book_room(self, guest_name, check_in, check_out):
        """Book room for guest"""
        if self.status == "AVAILABLE":
            self.status = "BOOKED"
            self.current_guest = guest_name
            self.check_in_date = check_in
            self.check_out_date = check_out
            return True
        return False
    
    def check_in(self):
        """Check in guest"""
        if self.status == "BOOKED":
            self.status = "OCCUPIED"
            return True
        return False
    
    def check_out(self):
        """Check out guest"""
        if self.status == "OCCUPIED":
            self.status = "AVAILABLE"
            self.current_guest = None
            self.check_in_date = None
            self.check_out_date = None
            return True
        return False
    
    def to_dict(self):
        """Convert to dictionary for JSON storage"""
        return {
            'room_number': self.room_number,
            'room_type': self.room_type,
            'price': self.price,
            'capacity': self.capacity,
            'amenities': self.amenities,
            'status': self.status,
            'current_guest': self.current_guest,
            'check_in_date': self.check_in_date.isoformat() if self.check_in_date else None,
            'check_out_date': self.check_out_date.isoformat() if self.check_out_date else None
        }
    
    def display(self):
        """Display room info"""
        status_color = {
            "AVAILABLE": Fore.GREEN + "✅ AVAILABLE",
            "BOOKED": Fore.YELLOW + "📅 BOOKED",
            "OCCUPIED": Fore.RED + "👤 OCCUPIED",
            "MAINTENANCE": Fore.RED + "🔧 MAINTENANCE"
        }
        
        return [
            self.room_number,
            self.room_type,
            f"₹{self.price}",
            self.capacity,
            len(self.amenities),
            status_color.get(self.status, self.status)
        ]

class Guest:
    """Guest class to store guest information"""
    def __init__(self, guest_id, name, phone, email, address, id_proof, id_number):
        self.guest_id = guest_id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.id_proof = id_proof  # Passport, DL, Aadhar, etc.
        self.id_number = id_number
        self.registration_date = datetime.datetime.now()
        self.total_stays = 0
        self.total_spent = 0
        self.vip_status = False
        
    def to_dict(self):
        """Convert to dictionary for JSON storage"""
        return {
            'guest_id': self.guest_id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'id_proof': self.id_proof,
            'id_number': self.id_number,
            'registration_date': self.registration_date.isoformat(),
            'total_stays': self.total_stays,
            'total_spent': self.total_spent,
            'vip_status': self.vip_status
        }
    
    def display(self):
        """Display guest info"""
        return [
            self.guest_id,
            self.name,
            self.phone,
            self.email,
            self.id_proof,
            self.total_stays,
            f"₹{self.total_spent}",
            Fore.YELLOW + "👑 VIP" if self.vip_status else "Standard"
        ]

class Booking:
    """Booking class for room reservations"""
    def __init__(self, booking_id, guest_id, room_number, check_in, check_out, 
                 adults, children, total_amount, status="CONFIRMED"):
        self.booking_id = booking_id
        self.guest_id = guest_id
        self.room_number = room_number
        self.check_in = check_in
        self.check_out = check_out
        self.adults = adults
        self.children = children
        self.total_amount = total_amount
        self.booking_date = datetime.datetime.now()
        self.status = status  # CONFIRMED, CHECKED_IN, CHECKED_OUT, CANCELLED
        self.payment_status = "PENDING"  # PENDING, PAID, REFUNDED
        self.payment_method = None
        self.special_requests = ""
    
    def calculate_nights(self):
        """Calculate number of nights"""
        return (self.check_out - self.check_in).days
    
    def to_dict(self):
        """Convert to dictionary for JSON storage"""
        return {
            'booking_id': self.booking_id,
            'guest_id': self.guest_id,
            'room_number': self.room_number,
            'check_in': self.check_in.isoformat(),
            'check_out': self.check_out.isoformat(),
            'adults': self.adults,
            'children': self.children,
            'total_amount': self.total_amount,
            'booking_date': self.booking_date.isoformat(),
            'status': self.status,
            'payment_status': self.payment_status,
            'payment_method': self.payment_method,
            'special_requests': self.special_requests
        }
    
    def display(self):
        """Display booking info"""
        return [
            self.booking_id,
            self.guest_id,
            self.room_number,
            self.check_in.strftime('%d/%m/%Y'),
            self.check_out.strftime('%d/%m/%Y'),
            f"{self.calculate_nights()} nights",
            f"₹{self.total_amount}",
            self.status,
            self.payment_status
        ]

class Staff:
    """Staff class for hotel employees"""
    def __init__(self, staff_id, name, position, department, phone, email, salary):
        self.staff_id = staff_id
        self.name = name
        self.position = position
        self.department = department
        self.phone = phone
        self.email = email
        self.salary = salary
        self.join_date = datetime.datetime.now()
        self.status = "ACTIVE"
        self.attendance = {}
    
    def to_dict(self):
        """Convert to dictionary for JSON storage"""
        return {
            'staff_id': self.staff_id,
            'name': self.name,
            'position': self.position,
            'department': self.department,
            'phone': self.phone,
            'email': self.email,
            'salary': self.salary,
            'join_date': self.join_date.isoformat(),
            'status': self.status
        }
    
    def display(self):
        """Display staff info"""
        return [
            self.staff_id,
            self.name,
            self.position,
            self.department,
            self.phone,
            f"₹{self.salary}",
            self.join_date.strftime('%d/%m/%Y'),
            Fore.GREEN + "ACTIVE" if self.status == "ACTIVE" else Fore.RED + "INACTIVE"
        ]

class Service:
    """Hotel services (Restaurant, Spa, Laundry, etc.)"""
    def __init__(self, service_id, name, category, price, description):
        self.service_id = service_id
        self.name = name
        self.category = category
        self.price = price
        self.description = description
        self.available = True
    
    def to_dict(self):
        """Convert to dictionary for JSON storage"""
        return {
            'service_id': self.service_id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'description': self.description,
            'available': self.available
        }
    
    def display(self):
        """Display service info"""
        return [
            self.service_id,
            self.name,
            self.category,
            f"₹{self.price}",
            self.description[:30] + "..." if len(self.description) > 30 else self.description,
            Fore.GREEN + "✅ Available" if self.available else Fore.RED + "❌ Unavailable"
        ]

class HotelManagementSystem:
    """Main Hotel Management System"""
    
    def __init__(self):
        self.rooms = []
        self.guests = []
        self.bookings = []
        self.staff = []
        self.services = []
        self.next_guest_id = 1001
        self.next_booking_id = 5001
        self.next_staff_id = 2001
        self.next_service_id = 3001
        self.initialize_data()
        self.load_data()
    
    def initialize_data(self):
        """Initialize hotel with sample data"""
        if len(self.rooms) == 0:
            # Add sample rooms
            room_configs = [
                # Standard Rooms
                ("101", "Standard", 2500, 2, ["TV", "AC", "WiFi", "Attached Bathroom"]),
                ("102", "Standard", 2500, 2, ["TV", "AC", "WiFi", "Attached Bathroom"]),
                ("103", "Standard", 2800, 3, ["TV", "AC", "WiFi", "Attached Bathroom", "Mini Fridge"]),
                ("104", "Standard", 2800, 3, ["TV", "AC", "WiFi", "Attached Bathroom", "Mini Fridge"]),
                
                # Deluxe Rooms
                ("201", "Deluxe", 4500, 2, ["TV", "AC", "WiFi", "Mini Bar", "Coffee Maker", "Bathtub"]),
                ("202", "Deluxe", 4500, 2, ["TV", "AC", "WiFi", "Mini Bar", "Coffee Maker", "Bathtub"]),
                ("203", "Deluxe", 5000, 4, ["TV", "AC", "WiFi", "Mini Bar", "Coffee Maker", "Bathtub", "Sofa"]),
                
                # Suite Rooms
                ("301", "Suite", 8000, 2, ["TV", "AC", "WiFi", "Mini Bar", "Coffee Maker", "Bathtub", "Living Area", "Kitchen"]),
                ("302", "Suite", 8500, 4, ["TV", "AC", "WiFi", "Mini Bar", "Coffee Maker", "Bathtub", "Living Area", "Kitchen", "Dining Area"]),
                
                # Presidential Suite
                ("401", "Presidential", 15000, 4, ["TV", "AC", "WiFi", "Mini Bar", "Coffee Maker", "Jacuzzi", "Living Area", "Dining Area", "Kitchen", "Study Room", "Balcony"]),
            ]
            
            for config in room_configs:
                room = Room(config[0], config[1], config[2], config[3], config[4])
                self.rooms.append(room)
        
        if len(self.services) == 0:
            # Add sample services
            service_configs = [
                (3001, "Breakfast Buffet", "Restaurant", 500, "Complimentary breakfast buffet"),
                (3002, "Lunch Buffet", "Restaurant", 800, "Multi-cuisine lunch buffet"),
                (3003, "Dinner Buffet", "Restaurant", 1200, "Premium dinner buffet"),
                (3004, "Spa Massage", "Spa", 2000, "Traditional massage therapy"),
                (3005, "Laundry Service", "Housekeeping", 300, "Wash and fold per item"),
                (3006, "Airport Pickup", "Transport", 1500, "Luxury car airport transfer"),
                (3007, "Gym Access", "Fitness", 500, "Fully equipped gymnasium"),
                (3008, "Swimming Pool", "Recreation", 400, "Indoor heated pool"),
            ]
            
            for config in service_configs:
                service = Service(config[0], config[1], config[2], config[3], config[4])
                self.services.append(service)
            self.next_service_id = 3009
        
        if len(self.staff) == 0:
            # Add sample staff
            staff_configs = [
                (2001, "Rajesh Kumar", "Manager", "Administration", "9876543210", "rajesh@hotel.com", 60000),
                (2002, "Priya Singh", "Receptionist", "Front Office", "9876543211", "priya@hotel.com", 25000),
                (2003, "Amit Shah", "Chef", "Kitchen", "9876543212", "amit@hotel.com", 40000),
                (2004, "Neha Gupta", "Housekeeping", "Housekeeping", "9876543213", "neha@hotel.com", 20000),
                (2005, "Vikram Mehta", "Security", "Security", "9876543214", "vikram@hotel.com", 18000),
            ]
            
            for config in staff_configs:
                staff = Staff(config[0], config[1], config[2], config[3], config[4], config[5], config[6])
                self.staff.append(staff)
            self.next_staff_id = 2006
    
    def display_header(self):
        """Display system header"""
        print(Fore.CYAN + "=" * 70)
        print(Fore.YELLOW + "🏨 HOTEL MANAGEMENT SYSTEM 🏨".center(70))
        print(Fore.CYAN + "=" * 70)
        current_time = datetime.datetime.now().strftime("%A, %d %B %Y - %I:%M %p")
        print(Fore.WHITE + f"{current_time}".center(70))
        print(Fore.CYAN + "=" * 70)
    
    def display_main_menu(self):
        """Display main menu"""
        print(Fore.GREEN + "\n📋 MAIN MENU")
        print(Fore.WHITE + "=" * 50)
        
        print(Fore.CYAN + "\n🏨 ROOM MANAGEMENT")
        print("  1. 📋 View All Rooms")
        print("  2. 🔍 Search Available Rooms")
        print("  3. ➕ Add New Room")
        print("  4. ✏️  Update Room Details")
        print("  5. 🔧 Room Maintenance")
        
        print(Fore.CYAN + "\n👤 GUEST MANAGEMENT")
        print("  6. 📝 New Guest Registration")
        print("  7. 👥 View All Guests")
        print("  8. 🔍 Search Guest")
        print("  9. ✏️  Update Guest Details")
        print(" 10. 👑 VIP Guest Management")
        
        print(Fore.CYAN + "\n📅 BOOKING MANAGEMENT")
        print(" 11. 🎫 New Booking")
        print(" 12. ✅ Check-In")
        print(" 13. ❌ Check-Out")
        print(" 14. 📋 View All Bookings")
        print(" 15. ❌ Cancel Booking")
        print(" 16. 💰 Process Payment")
        
        print(Fore.CYAN + "\n👨‍💼 STAFF MANAGEMENT")
        print(" 17. ➕ Add Staff")
        print(" 18. 👥 View All Staff")
        print(" 19. ✏️  Update Staff")
        print(" 20. 📊 Staff Attendance")
        
        print(Fore.CYAN + "\n🛎️  SERVICES")
        print(" 21. 🍽️  Restaurant Services")
        print(" 22. 💆 Spa Services")
        print(" 23. 🧺 Housekeeping")
        print(" 24. 🚗 Transport")
        
        print(Fore.CYAN + "\n📊 REPORTS")
        print(" 25. 📈 Occupancy Report")
        print(" 26. 💰 Revenue Report")
        print(" 27. 📋 Today's Summary")
        print(" 28. ⭐ Guest Feedback")
        
        print(Fore.RED + "\n 29. 🚪 Exit")
        print(Fore.WHITE + "=" * 50)
    
    # ==================== ROOM MANAGEMENT ====================
    
    def view_all_rooms(self):
        """View all rooms with status"""
        print(Fore.GREEN + "\n📋 ALL ROOMS")
        print(Fore.CYAN + "=" * 90)
        
        # Group by room type
        room_types = ["Standard", "Deluxe", "Suite", "Presidential"]
        
        for room_type in room_types:
            type_rooms = [r for r in self.rooms if r.room_type == room_type]
            if type_rooms:
                print(Fore.YELLOW + f"\n{room_type} Rooms:")
                print(Fore.CYAN + "-" * 90)
                
                rooms_data = []
                for room in type_rooms:
                    rooms_data.append(room.display())
                
                headers = ['Room No', 'Type', 'Price/Night', 'Capacity', 'Amenities', 'Status']
                print(tabulate(rooms_data, headers=headers, tablefmt='grid'))
        
        # Summary
        total_rooms = len(self.rooms)
        available = len([r for r in self.rooms if r.status == "AVAILABLE"])
        booked = len([r for r in self.rooms if r.status == "BOOKED"])
        occupied = len([r for r in self.rooms if r.status == "OCCUPIED"])
        maintenance = len([r for r in self.rooms if r.status == "MAINTENANCE"])
        
        print(Fore.CYAN + "=" * 90)
        print(Fore.YELLOW + f"📊 SUMMARY:")
        print(f"   Total Rooms: {total_rooms}")
        print(Fore.GREEN + f"   ✅ Available: {available}")
        print(Fore.YELLOW + f"   📅 Booked: {booked}")
        print(Fore.RED + f"   👤 Occupied: {occupied}")
        print(Fore.RED + f"   🔧 Maintenance: {maintenance}")
    
    def search_available_rooms(self):
        """Search available rooms by criteria"""
        print(Fore.GREEN + "\n🔍 SEARCH AVAILABLE ROOMS")
        print(Fore.CYAN + "-" * 40)
        
        print("\nSearch by:")
        print("1. Room Type")
        print("2. Price Range")
        print("3. Capacity")
        print("4. Amenities")
        
        choice = input(Fore.YELLOW + "\nEnter your choice (1-4): ")
        
        available_rooms = [r for r in self.rooms if r.status == "AVAILABLE"]
        
        if choice == '1':
            print("\nRoom Types:")
            print("1. Standard")
            print("2. Deluxe")
            print("3. Suite")
            print("4. Presidential")
            
            type_choice = input("Select room type (1-4): ")
            room_types = ['Standard', 'Deluxe', 'Suite', 'Presidential']
            selected_type = room_types[int(type_choice)-1]
            
            results = [r for r in available_rooms if r.room_type == selected_type]
            
        elif choice == '2':
            try:
                min_price = float(input("Enter minimum price: ₹"))
                max_price = float(input("Enter maximum price: ₹"))
                results = [r for r in available_rooms if min_price <= r.price <= max_price]
            except:
                print(Fore.RED + "❌ Invalid price!")
                return
                
        elif choice == '3':
            try:
                capacity = int(input("Enter number of guests: "))
                results = [r for r in available_rooms if r.capacity >= capacity]
            except:
                print(Fore.RED + "❌ Invalid capacity!")
                return
                
        elif choice == '4':
            amenity = input("Enter amenity (e.g., WiFi, AC, TV, Mini Bar): ").title()
            results = [r for r in available_rooms if any(amenity.lower() in a.lower() for a in r.amenities)]
        
        else:
            print(Fore.RED + "❌ Invalid choice!")
            return
        
        if results:
            print(Fore.GREEN + f"\n✅ Found {len(results)} available room(s):")
            print(Fore.CYAN + "=" * 90)
            
            rooms_data = []
            for room in results:
                rooms_data.append([
                    room.room_number,
                    room.room_type,
                    f"₹{room.price}",
                    room.capacity,
                    ", ".join(room.amenities[:3]) + "..." if len(room.amenities) > 3 else ", ".join(room.amenities),
                    Fore.GREEN + "AVAILABLE"
                ])
            
            headers = ['Room No', 'Type', 'Price/Night', 'Capacity', 'Amenities', 'Status']
            print(tabulate(rooms_data, headers=headers, tablefmt='grid'))
        else:
            print(Fore.RED + "❌ No rooms found matching your criteria!")
    
    def add_new_room(self):
        """Add new room to hotel"""
        print(Fore.GREEN + "\n➕ ADD NEW ROOM")
        print(Fore.CYAN + "-" * 40)
        
        room_number = input("Enter Room Number: ")
        
        # Check if room already exists
        for room in self.rooms:
            if room.room_number == room_number:
                print(Fore.RED + "❌ Room number already exists!")
                return
        
        print("\nRoom Types:")
        print("1. Standard")
        print("2. Deluxe")
        print("3. Suite")
        print("4. Presidential")
        
        type_choice = input("Select room type (1-4): ")
        room_types = ['Standard', 'Deluxe', 'Suite', 'Presidential']
        room_type = room_types[int(type_choice)-1]
        
        try:
            price = float(input("Enter price per night: ₹"))
            capacity = int(input("Enter maximum capacity: "))
        except:
            print(Fore.RED + "❌ Invalid input!")
            return
        
        print("\nAmenities (enter comma-separated):")
        print("Example: TV, AC, WiFi, Mini Bar, Bathtub")
        amenities_input = input("Enter amenities: ")
        amenities = [a.strip() for a in amenities_input.split(',')]
        
        room = Room(room_number, room_type, price, capacity, amenities)
        self.rooms.append(room)
        
        print(Fore.GREEN + f"\n✅ Room {room_number} added successfully!")
        self.save_data()
    
    def update_room_details(self):
        """Update room details"""
        print(Fore.GREEN + "\n✏️ UPDATE ROOM DETAILS")
        print(Fore.CYAN + "-" * 40)
        
        room_number = input("Enter Room Number: ")
        
        for room in self.rooms:
            if room.room_number == room_number:
                print(f"\nCurrent Room Details:")
                print(f"Type: {room.room_type}")
                print(f"Price: ₹{room.price}")
                print(f"Capacity: {room.capacity}")
                print(f"Amenities: {', '.join(room.amenities)}")
                
                print(Fore.CYAN + "\nEnter new details (press Enter to skip):")
                
                new_price = input(f"New price (current: ₹{room.price}): ")
                if new_price:
                    room.price = float(new_price)
                
                new_capacity = input(f"New capacity (current: {room.capacity}): ")
                if new_capacity:
                    room.capacity = int(new_capacity)
                
                new_amenities = input(f"New amenities (current: {', '.join(room.amenities)}): ")
                if new_amenities:
                    room.amenities = [a.strip() for a in new_amenities.split(',')]
                
                print(Fore.GREEN + "✅ Room details updated successfully!")
                self.save_data()
                return
        
        print(Fore.RED + "❌ Room not found!")
    
    def room_maintenance(self):
        """Set room under maintenance"""
        print(Fore.GREEN + "\n🔧 ROOM MAINTENANCE")
        print(Fore.CYAN + "-" * 40)
        
        room_number = input("Enter Room Number: ")
        
        for room in self.rooms:
            if room.room_number == room_number:
                if room.status == "AVAILABLE":
                    room.status = "MAINTENANCE"
                    print(Fore.GREEN + f"✅ Room {room_number} is now under maintenance.")
                elif room.status == "MAINTENANCE":
                    room.status = "AVAILABLE"
                    print(Fore.GREEN + f"✅ Room {room_number} is now available.")
                else:
                    print(Fore.RED + f"❌ Cannot change status! Room is {room.status}.")
                
                self.save_data()
                return
        
        print(Fore.RED + "❌ Room not found!")
    
    # ==================== GUEST MANAGEMENT ====================
    
    def register_guest(self):
        """Register new guest"""
        print(Fore.GREEN + "\n📝 NEW GUEST REGISTRATION")
        print(Fore.CYAN + "-" * 40)
        
        name = input("Enter Full Name: ")
        
        # Validate phone
        while True:
            phone = input("Enter Phone Number: ")
            if re.match(r'^\d{10}$', phone):
                break
            else:
                print(Fore.RED + "❌ Please enter valid 10-digit phone number!")
        
        # Validate email
        while True:
            email = input("Enter Email: ")
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                break
            else:
                print(Fore.RED + "❌ Please enter valid email!")
        
        address = input("Enter Address: ")
        
        print("\nID Proof Types:")
        print("1. Passport")
        print("2. Driving License")
        print("3. Aadhar Card")
        print("4. Voter ID")
        
        id_choice = input("Select ID proof (1-4): ")
        id_types = ['Passport', 'Driving License', 'Aadhar Card', 'Voter ID']
        id_proof = id_types[int(id_choice)-1]
        
        id_number = input(f"Enter {id_proof} Number: ")
        
        guest = Guest(self.next_guest_id, name, phone, email, address, id_proof, id_number)
        self.guests.append(guest)
        
        print(Fore.GREEN + f"\n✅ Guest registered successfully!")
        print(Fore.YELLOW + f"👤 Guest ID: {self.next_guest_id}")
        print(f"   Name: {name}")
        print(f"   Phone: {phone}")
        
        self.next_guest_id += 1
        self.save_data()
    
    def view_all_guests(self):
        """View all registered guests"""
        print(Fore.GREEN + "\n👥 ALL GUESTS")
        print(Fore.CYAN + "=" * 120)
        
        if not self.guests:
            print(Fore.YELLOW + "No guests registered.")
            return
        
        guests_data = []
        for guest in self.guests:
            guests_data.append(guest.display())
        
        headers = ['Guest ID', 'Name', 'Phone', 'Email', 'ID Proof', 'Stays', 'Total Spent', 'Status']
        print(tabulate(guests_data, headers=headers, tablefmt='grid'))
        print(Fore.CYAN + "=" * 120)
        print(Fore.YELLOW + f"👥 Total Guests: {len(self.guests)}")
    
    def search_guest(self):
        """Search guest by ID or name"""
        print(Fore.GREEN + "\n🔍 SEARCH GUEST")
        print(Fore.CYAN + "-" * 40)
        
        search_term = input("Enter Guest ID or Name: ").lower()
        results = []
        
        for guest in self.guests:
            if str(guest.guest_id) == search_term or search_term in guest.name.lower():
                results.append(guest)
        
        if results:
            print(Fore.GREEN + f"\n✅ Found {len(results)} guest(s):")
            print(Fore.CYAN + "=" * 120)
            
            guests_data = []
            for guest in results:
                guests_data.append(guest.display())
            
            headers = ['Guest ID', 'Name', 'Phone', 'Email', 'ID Proof', 'Stays', 'Total Spent', 'Status']
            print(tabulate(guests_data, headers=headers, tablefmt='grid'))
            
            # Show booking history for selected guest
            if len(results) == 1:
                guest = results[0]
                guest_bookings = [b for b in self.bookings if b.guest_id == guest.guest_id]
                if guest_bookings:
                    print(Fore.CYAN + f"\n📋 Booking History for {guest.name}:")
                    print("-" * 100)
                    bookings_data = []
                    for b in guest_bookings[-5:]:  # Last 5 bookings
                        bookings_data.append(b.display())
                    
                    headers = ['Booking ID', 'Guest ID', 'Room', 'Check-In', 'Check-Out', 'Nights', 'Amount', 'Status', 'Payment']
                    print(tabulate(bookings_data, headers=headers, tablefmt='grid'))
        else:
            print(Fore.RED + "❌ No guests found!")
    
    def update_guest_details(self):
        """Update guest information"""
        print(Fore.GREEN + "\n✏️ UPDATE GUEST DETAILS")
        print(Fore.CYAN + "-" * 40)
        
        guest_id = int(input("Enter Guest ID: "))
        
        for guest in self.guests:
            if guest.guest_id == guest_id:
                print(f"\nCurrent Details for {guest.name}:")
                print(f"Phone: {guest.phone}")
                print(f"Email: {guest.email}")
                print(f"Address: {guest.address}")
                
                print(Fore.CYAN + "\nEnter new details (press Enter to skip):")
                
                new_phone = input(f"New phone (current: {guest.phone}): ")
                if new_phone and re.match(r'^\d{10}$', new_phone):
                    guest.phone = new_phone
                
                new_email = input(f"New email (current: {guest.email}): ")
                if new_email and re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', new_email):
                    guest.email = new_email
                
                new_address = input(f"New address (current: {guest.address}): ")
                if new_address:
                    guest.address = new_address
                
                print(Fore.GREEN + "✅ Guest details updated successfully!")
                self.save_data()
                return
        
        print(Fore.RED + "❌ Guest not found!")
    
    def vip_management(self):
        """Manage VIP guests"""
        print(Fore.GREEN + "\n👑 VIP GUEST MANAGEMENT")
        print(Fore.CYAN + "-" * 40)
        
        print("1. View VIP Guests")
        print("2. Add VIP")
        print("3. Remove VIP")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            vip_guests = [g for g in self.guests if g.vip_status]
            if vip_guests:
                print(Fore.GREEN + f"\n✅ VIP Guests ({len(vip_guests)}):")
                print(Fore.CYAN + "=" * 80)
                for guest in vip_guests:
                    print(f"   {guest.guest_id} - {guest.name} - {guest.phone} - Total Spent: ₹{guest.total_spent}")
            else:
                print(Fore.YELLOW + "No VIP guests yet.")
        
        elif choice == '2':
            guest_id = int(input("Enter Guest ID to make VIP: "))
            for guest in self.guests:
                if guest.guest_id == guest_id:
                    guest.vip_status = True
                    print(Fore.GREEN + f"✅ {guest.name} is now a VIP guest!")
                    self.save_data()
                    return
            print(Fore.RED + "❌ Guest not found!")
        
        elif choice == '3':
            guest_id = int(input("Enter Guest ID to remove VIP: "))
            for guest in self.guests:
                if guest.guest_id == guest_id:
                    guest.vip_status = False
                    print(Fore.GREEN + f"✅ VIP status removed from {guest.name}!")
                    self.save_data()
                    return
            print(Fore.RED + "❌ Guest not found!")
    
    # ==================== BOOKING MANAGEMENT ====================
    
    def new_booking(self):
        """Create new booking"""
        print(Fore.GREEN + "\n🎫 NEW BOOKING")
        print(Fore.CYAN + "=" * 50)
        
        # Check if guest exists
        guest_id = int(input("Enter Guest ID (0 for new guest): "))
        
        if guest_id == 0:
            self.register_guest()
            guest_id = self.next_guest_id - 1
        
        guest = None
        for g in self.guests:
            if g.guest_id == guest_id:
                guest = g
                break
        
        if not guest:
            print(Fore.RED + "❌ Guest not found!")
            return
        
        print(f"\n👤 Guest: {guest.name}")
        print(f"📞 Phone: {guest.phone}")
        
        # Show available rooms
        available_rooms = [r for r in self.rooms if r.status == "AVAILABLE"]
        
        if not available_rooms:
            print(Fore.RED + "❌ No rooms available!")
            return
        
        print(Fore.GREEN + f"\n✅ Available Rooms: {len(available_rooms)}")
        
        # Get booking details
        print(Fore.CYAN + "\n📅 Enter Booking Details:")
        
        while True:
            try:
                check_in_str = input("Check-In Date (DD/MM/YYYY): ")
                check_in = datetime.datetime.strptime(check_in_str, '%d/%m/%Y')
                
                check_out_str = input("Check-Out Date (DD/MM/YYYY): ")
                check_out = datetime.datetime.strptime(check_out_str, '%d/%m/%Y')
                
                if check_out <= check_in:
                    print(Fore.RED + "❌ Check-out date must be after check-in date!")
                    continue
                
                break
            except:
                print(Fore.RED + "❌ Invalid date format! Use DD/MM/YYYY")
        
        nights = (check_out - check_in).days
        
        # Select room
        print(Fore.CYAN + f"\n📋 Available Rooms for {nights} nights:")
        
        suitable_rooms = []
        for room in available_rooms:
            suitable_rooms.append([
                room.room_number,
                room.room_type,
                f"₹{room.price}",
                f"₹{room.price * nights}",
                room.capacity,
                ", ".join(room.amenities[:3])
            ])
        
        headers = ['Room No', 'Type', 'Price/Night', 'Total', 'Capacity', 'Amenities']
        print(tabulate(suitable_rooms[:10], headers=headers, tablefmt='grid'))
        
        room_number = input("\nEnter Room Number: ")
        
        selected_room = None
        for room in self.rooms:
            if room.room_number == room_number and room.status == "AVAILABLE":
                selected_room = room
                break
        
        if not selected_room:
            print(Fore.RED + "❌ Room not available!")
            return
        
        # Number of guests
        try:
            adults = int(input("Number of Adults: "))
            children = int(input("Number of Children: "))
        except:
            adults = 1
            children = 0
        
        total_amount = selected_room.price * nights
        
        # Apply VIP discount
        if guest.vip_status:
            discount = total_amount * 0.1
            total_amount -= discount
            print(Fore.YELLOW + f"\n👑 VIP Discount: 10% (₹{discount:.2f})")
        
        # Create booking
        booking = Booking(
            self.next_booking_id,
            guest_id,
            room_number,
            check_in,
            check_out,
            adults,
            children,
            total_amount
        )
        
        # Book the room
        selected_room.book_room(guest.name, check_in, check_out)
        self.bookings.append(booking)
        
        print(Fore.GREEN + "\n" + "=" * 50)
        print("✅ BOOKING CONFIRMED!")
        print("=" * 50)
        print(f"📋 Booking ID: {self.next_booking_id}")
        print(f"👤 Guest: {guest.name}")
        print(f"🏨 Room: {room_number} ({selected_room.room_type})")
        print(f"📅 Check-In: {check_in.strftime('%d/%m/%Y')}")
        print(f"📅 Check-Out: {check_out.strftime('%d/%m/%Y')}")
        print(f"🌙 Nights: {nights}")
        print(f"💰 Total Amount: ₹{total_amount:.2f}")
        print(f"💳 Payment Status: {booking.payment_status}")
        print("=" * 50)
        
        self.next_booking_id += 1
        self.save_data()
    
    def check_in(self):
        """Check-in guest"""
        print(Fore.GREEN + "\n✅ CHECK-IN")
        print(Fore.CYAN + "-" * 40)
        
        booking_id = int(input("Enter Booking ID: "))
        
        for booking in self.bookings:
            if booking.booking_id == booking_id and booking.status == "CONFIRMED":
                
                # Find room
                for room in self.rooms:
                    if room.room_number == booking.room_number:
                        room.check_in()
                        booking.status = "CHECKED_IN"
                        
                        print(Fore.GREEN + "\n✅ Check-In Successful!")
                        print(f"Booking ID: {booking_id}")
                        print(f"Room: {room.room_number}")
                        print(f"Guest ID: {booking.guest_id}")
                        print(f"Check-In: {datetime.datetime.now().strftime('%d/%m/%Y %I:%M %p')}")
                        
                        self.save_data()
                        return
        
        print(Fore.RED + "❌ Booking not found or already checked-in!")
    
    def check_out(self):
        """Check-out guest"""
        print(Fore.GREEN + "\n❌ CHECK-OUT")
        print(Fore.CYAN + "-" * 40)
        
        booking_id = int(input("Enter Booking ID: "))
        
        for booking in self.bookings:
            if booking.booking_id == booking_id and booking.status == "CHECKED_IN":
                
                # Find room
                for room in self.rooms:
                    if room.room_number == booking.room_number:
                        room.check_out()
                        booking.status = "CHECKED_OUT"
                        
                        # Update guest stats
                        for guest in self.guests:
                            if guest.guest_id == booking.guest_id:
                                guest.total_stays += 1
                                guest.total_spent += booking.total_amount
                                
                                # Auto VIP for guests who spent > ₹50000
                                if guest.total_spent > 50000 and not guest.vip_status:
                                    guest.vip_status = True
                                    print(Fore.YELLOW + f"👑 Congratulations! {guest.name} is now a VIP guest!")
                                
                                break
                        
                        print(Fore.GREEN + "\n✅ Check-Out Successful!")
                        print(f"Booking ID: {booking_id}")
                        print(f"Room: {room.room_number}")
                        print(f"Total Amount: ₹{booking.total_amount:.2f}")
                        
                        if booking.payment_status != "PAID":
                            print(Fore.RED + "⚠️  Payment Pending!")
                            self.process_payment(booking_id)
                        
                        self.save_data()
                        return
        
        print(Fore.RED + "❌ Booking not found or not checked-in!")
    
    def view_all_bookings(self):
        """View all bookings"""
        print(Fore.GREEN + "\n📋 ALL BOOKINGS")
        print(Fore.CYAN + "=" * 120)
        
        if not self.bookings:
            print(Fore.YELLOW + "No bookings found.")
            return
        
        # Group by status
        statuses = ["CONFIRMED", "CHECKED_IN", "CHECKED_OUT", "CANCELLED"]
        
        for status in statuses:
            status_bookings = [b for b in self.bookings if b.status == status]
            if status_bookings:
                print(Fore.YELLOW + f"\n{status} BOOKINGS:")
                print(Fore.CYAN + "-" * 120)
                
                bookings_data = []
                for booking in status_bookings[-10:]:  # Last 10 of each status
                    bookings_data.append(booking.display())
                
                headers = ['Booking ID', 'Guest ID', 'Room', 'Check-In', 'Check-Out', 'Nights', 'Amount', 'Status', 'Payment']
                print(tabulate(bookings_data, headers=headers, tablefmt='grid'))
        
        # Summary
        total_bookings = len(self.bookings)
        confirmed = len([b for b in self.bookings if b.status == "CONFIRMED"])
        checked_in = len([b for b in self.bookings if b.status == "CHECKED_IN"])
        checked_out = len([b for b in self.bookings if b.status == "CHECKED_OUT"])
        cancelled = len([b for b in self.bookings if b.status == "CANCELLED"])
        
        print(Fore.CYAN + "=" * 120)
        print(Fore.YELLOW + f"📊 SUMMARY:")
        print(f"   Total Bookings: {total_bookings}")
        print(f"   📅 Confirmed: {confirmed}")
        print(f"   ✅ Checked-In: {checked_in}")
        print(f"   ❌ Checked-Out: {checked_out}")
        print(f"   ❌ Cancelled: {cancelled}")
    
    def cancel_booking(self):
        """Cancel booking"""
        print(Fore.GREEN + "\n❌ CANCEL BOOKING")
        print(Fore.CYAN + "-" * 40)
        
        booking_id = int(input("Enter Booking ID: "))
        
        for booking in self.bookings:
            if booking.booking_id == booking_id and booking.status in ["CONFIRMED", "CHECKED_IN"]:
                
                # Find room
                for room in self.rooms:
                    if room.room_number == booking.room_number:
                        room.status = "AVAILABLE"
                        room.current_guest = None
                        room.check_in_date = None
                        room.check_out_date = None
                        break
                
                booking.status = "CANCELLED"
                booking.payment_status = "REFUNDED"
                
                print(Fore.GREEN + "\n✅ Booking cancelled successfully!")
                print(f"Booking ID: {booking_id}")
                print(f"Room: {booking.room_number}")
                print(f"Refund Amount: ₹{booking.total_amount:.2f}")
                
                self.save_data()
                return
        
        print(Fore.RED + "❌ Booking not found or cannot be cancelled!")
    
    def process_payment(self, booking_id=None):
        """Process payment for booking"""
        if not booking_id:
            print(Fore.GREEN + "\n💰 PROCESS PAYMENT")
            print(Fore.CYAN + "-" * 40)
            booking_id = int(input("Enter Booking ID: "))
        
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                
                if booking.payment_status == "PAID":
                    print(Fore.YELLOW + "✅ Payment already completed!")
                    return
                
                print(f"\nBooking Details:")
                print(f"   Booking ID: {booking.booking_id}")
                print(f"   Room: {booking.room_number}")
                print(f"   Total Amount: ₹{booking.total_amount:.2f}")
                print(f"   Current Status: {booking.payment_status}")
                
                print(Fore.CYAN + "\nPayment Methods:")
                print("1. 💳 Credit Card")
                print("2. 💳 Debit Card")
                print("3. 🏦 Net Banking")
                print("4. 📱 UPI")
                print("5. 💵 Cash")
                
                method_choice = input("\nSelect payment method (1-5): ")
                methods = ['Credit Card', 'Debit Card', 'Net Banking', 'UPI', 'Cash']
                payment_method = methods[int(method_choice)-1]
                
                booking.payment_status = "PAID"
                booking.payment_method = payment_method
                
                print(Fore.GREEN + "\n✅ Payment Successful!")
                print(f"   Booking ID: {booking_id}")
                print(f"   Amount: ₹{booking.total_amount:.2f}")
                print(f"   Method: {payment_method}")
                print(f"   Date: {datetime.datetime.now().strftime('%d/%m/%Y %I:%M %p')}")
                
                self.save_data()
                return
        
        if not booking_id:
            print(Fore.RED + "❌ Booking not found!")
    
    # ==================== STAFF MANAGEMENT ====================
    
    def add_staff(self):
        """Add new staff member"""
        print(Fore.GREEN + "\n➕ ADD STAFF")
        print(Fore.CYAN + "-" * 40)
        
        name = input("Enter Staff Name: ")
        position = input("Enter Position: ")
        department = input("Enter Department: ")
        
        # Validate phone
        while True:
            phone = input("Enter Phone Number: ")
            if re.match(r'^\d{10}$', phone):
                break
            else:
                print(Fore.RED + "❌ Please enter valid 10-digit phone number!")
        
        # Validate email
        while True:
            email = input("Enter Email: ")
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                break
            else:
                print(Fore.RED + "❌ Please enter valid email!")
        
        try:
            salary = float(input("Enter Salary: ₹"))
        except:
            print(Fore.RED + "❌ Invalid salary!")
            return
        
        staff = Staff(self.next_staff_id, name, position, department, phone, email, salary)
        self.staff.append(staff)
        
        print(Fore.GREEN + f"\n✅ Staff added successfully!")
        print(Fore.YELLOW + f"👤 Staff ID: {self.next_staff_id}")
        
        self.next_staff_id += 1
        self.save_data()
    
    def view_all_staff(self):
        """View all staff members"""
        print(Fore.GREEN + "\n👥 ALL STAFF")
        print(Fore.CYAN + "=" * 100)
        
        if not self.staff:
            print(Fore.YELLOW + "No staff members.")
            return
        
        # Group by department
        departments = list(set(s.department for s in self.staff))
        
        for dept in departments:
            dept_staff = [s for s in self.staff if s.department == dept]
            print(Fore.YELLOW + f"\n{dept} DEPARTMENT:")
            print(Fore.CYAN + "-" * 100)
            
            staff_data = []
            for staff in dept_staff:
                staff_data.append(staff.display())
            
            headers = ['Staff ID', 'Name', 'Position', 'Department', 'Phone', 'Salary', 'Join Date', 'Status']
            print(tabulate(staff_data, headers=headers, tablefmt='grid'))
        
        print(Fore.CYAN + "=" * 100)
        print(Fore.YELLOW + f"👥 Total Staff: {len(self.staff)}")
    
    def update_staff(self):
        """Update staff details"""
        print(Fore.GREEN + "\n✏️ UPDATE STAFF")
        print(Fore.CYAN + "-" * 40)
        
        staff_id = int(input("Enter Staff ID: "))
        
        for staff in self.staff:
            if staff.staff_id == staff_id:
                print(f"\nCurrent Details for {staff.name}:")
                print(f"Position: {staff.position}")
                print(f"Department: {staff.department}")
                print(f"Phone: {staff.phone}")
                print(f"Email: {staff.email}")
                print(f"Salary: ₹{staff.salary}")
                print(f"Status: {staff.status}")
                
                print(Fore.CYAN + "\nEnter new details (press Enter to skip):")
                
                new_position = input(f"New position (current: {staff.position}): ")
                if new_position:
                    staff.position = new_position
                
                new_department = input(f"New department (current: {staff.department}): ")
                if new_department:
                    staff.department = new_department
                
                new_phone = input(f"New phone (current: {staff.phone}): ")
                if new_phone and re.match(r'^\d{10}$', new_phone):
                    staff.phone = new_phone
                
                new_email = input(f"New email (current: {staff.email}): ")
                if new_email and re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', new_email):
                    staff.email = new_email
                
                new_salary = input(f"New salary (current: ₹{staff.salary}): ")
                if new_salary:
                    staff.salary = float(new_salary)
                
                new_status = input(f"New status (current: {staff.status}) [ACTIVE/INACTIVE]: ").upper()
                if new_status in ['ACTIVE', 'INACTIVE']:
                    staff.status = new_status
                
                print(Fore.GREEN + "✅ Staff details updated successfully!")
                self.save_data()
                return
        
        print(Fore.RED + "❌ Staff not found!")
    
    # ==================== SERVICES ====================
    
    def restaurant_services(self):
        """Restaurant services menu"""
        print(Fore.GREEN + "\n🍽️  RESTAURANT SERVICES")
        print(Fore.CYAN + "=" * 60)
        
        restaurant_services = [s for s in self.services if s.category == "Restaurant"]
        
        if restaurant_services:
            services_data = []
            for service in restaurant_services:
                services_data.append(service.display())
            
            headers = ['Service ID', 'Name', 'Category', 'Price', 'Description', 'Status']
            print(tabulate(services_data, headers=headers, tablefmt='grid'))
        
        # Order service
        print(Fore.CYAN + "\n📝 Place Order:")
        guest_id = int(input("Enter Guest ID: "))
        service_id = int(input("Enter Service ID: "))
        
        # Find guest and service
        guest = None
        for g in self.guests:
            if g.guest_id == guest_id:
                guest = g
                break
        
        service = None
        for s in self.services:
            if s.service_id == service_id:
                service = s
                break
        
        if guest and service:
            print(Fore.GREEN + f"\n✅ Order placed successfully!")
            print(f"   Guest: {guest.name}")
            print(f"   Service: {service.name}")
            print(f"   Amount: ₹{service.price}")
            
            # Add to guest's bill
            booking = None
            for b in self.bookings:
                if b.guest_id == guest_id and b.status in ["CHECKED_IN", "CONFIRMED"]:
                    b.total_amount += service.price
                    break
            
            self.save_data()
        else:
            print(Fore.RED + "❌ Guest or Service not found!")
    
    def spa_services(self):
        """Spa services menu"""
        print(Fore.GREEN + "\n💆 SPA SERVICES")
        print(Fore.CYAN + "=" * 60)
        
        spa_services = [s for s in self.services if s.category == "Spa"]
        
        if spa_services:
            services_data = []
            for service in spa_services:
                services_data.append(service.display())
            
            headers = ['Service ID', 'Name', 'Category', 'Price', 'Description', 'Status']
            print(tabulate(services_data, headers=headers, tablefmt='grid'))
    
    def housekeeping(self):
        """Housekeeping services"""
        print(Fore.GREEN + "\n🧺 HOUSEKEEPING")
        print(Fore.CYAN + "=" * 60)
        
        room_number = input("Enter Room Number: ")
        
        print("\nServices:")
        print("1. Room Cleaning")
        print("2. Laundry Service")
        print("3. Towel Change")
        print("4. Bed Making")
        print("5. Mini Bar Restock")
        
        choice = input("\nSelect service: ")
        
        print(Fore.GREEN + f"\n✅ Housekeeping request sent for Room {room_number}!")
    
    def transport(self):
        """Transport services"""
        print(Fore.GREEN + "\n🚗 TRANSPORT SERVICES")
        print(Fore.CYAN + "=" * 60)
        
        transport_services = [s for s in self.services if s.category == "Transport"]
        
        if transport_services:
            services_data = []
            for service in transport_services:
                services_data.append(service.display())
            
            headers = ['Service ID', 'Name', 'Category', 'Price', 'Description', 'Status']
            print(tabulate(services_data, headers=headers, tablefmt='grid'))
    
    # ==================== REPORTS ====================
    
    def occupancy_report(self):
        """Generate occupancy report"""
        print(Fore.GREEN + "\n📈 OCCUPANCY REPORT")
        print(Fore.CYAN + "=" * 60)
        
        today = datetime.datetime.now()
        
        total_rooms = len(self.rooms)
        occupied = len([r for r in self.rooms if r.status == "OCCUPIED"])
        booked = len([r for r in self.rooms if r.status == "BOOKED"])
        available = len([r for r in self.rooms if r.status == "AVAILABLE"])
        maintenance = len([r for r in self.rooms if r.status == "MAINTENANCE"])
        
        occupancy_rate = (occupied + booked) / total_rooms * 100 if total_rooms > 0 else 0
        
        print(Fore.YELLOW + f"\n📅 Date: {today.strftime('%d/%m/%Y')}")
        print(f"\n📊 OCCUPANCY SUMMARY:")
        print(f"   Total Rooms: {total_rooms}")
        print(Fore.RED + f"   👤 Occupied: {occupied}")
        print(Fore.YELLOW + f"   📅 Booked: {booked}")
        print(Fore.GREEN + f"   ✅ Available: {available}")
        print(Fore.RED + f"   🔧 Maintenance: {maintenance}")
        print(Fore.CYAN + f"   📈 Occupancy Rate: {occupancy_rate:.1f}%")
        
        print(Fore.YELLOW + f"\n📋 ROOM TYPE BREAKDOWN:")
        print(Fore.CYAN + "-" * 40)
        
        room_types = ["Standard", "Deluxe", "Suite", "Presidential"]
        for room_type in room_types:
            type_rooms = [r for r in self.rooms if r.room_type == room_type]
            type_occupied = len([r for r in type_rooms if r.status in ["OCCUPIED", "BOOKED"]])
            type_total = len(type_rooms)
            type_rate = type_occupied / type_total * 100 if type_total > 0 else 0
            
            print(f"   {room_type}: {type_occupied}/{type_total} ({type_rate:.1f}%)")
    
    def revenue_report(self):
        """Generate revenue report"""
        print(Fore.GREEN + "\n💰 REVENUE REPORT")
        print(Fore.CYAN + "=" * 60)
        
        today = datetime.datetime.now()
        first_day = datetime.datetime(today.year, today.month, 1)
        
        # This month's revenue
        monthly_revenue = sum(b.total_amount for b in self.bookings 
                             if b.status == "CHECKED_OUT" and 
                             b.check_out.month == today.month and 
                             b.check_out.year == today.year)
        
        # Today's revenue
        today_revenue = sum(b.total_amount for b in self.bookings 
                           if b.status == "CHECKED_OUT" and 
                           b.check_out.date() == today.date())
        
        # Total revenue
        total_revenue = sum(g.total_spent for g in self.guests)
        
        print(Fore.YELLOW + f"\n📅 Period: {first_day.strftime('%d/%m/%Y')} - {today.strftime('%d/%m/%Y')}")
        print(f"\n📊 REVENUE SUMMARY:")
        print(Fore.GREEN + f"   💰 Today's Revenue: ₹{today_revenue:.2f}")
        print(Fore.CYAN + f"   📅 This Month: ₹{monthly_revenue:.2f}")
        print(Fore.YELLOW + f"   📈 Total Revenue: ₹{total_revenue:.2f}")
        
        # Average per booking
        completed_bookings = [b for b in self.bookings if b.status == "CHECKED_OUT"]
        avg_booking = total_revenue / len(completed_bookings) if completed_bookings else 0
        print(f"   📊 Average per Booking: ₹{avg_booking:.2f}")
    
    def todays_summary(self):
        """Display today's summary"""
        print(Fore.GREEN + "\n📋 TODAY'S SUMMARY")
        print(Fore.CYAN + "=" * 60)
        
        today = datetime.datetime.now().date()
        
        # Today's check-ins
        today_checkins = [b for b in self.bookings 
                         if b.check_in.date() == today and b.status == "CONFIRMED"]
        
        # Today's check-outs
        today_checkouts = [b for b in self.bookings 
                          if b.check_out.date() == today and b.status == "CHECKED_IN"]
        
        # Today's revenue
        today_revenue = sum(b.total_amount for b in self.bookings 
                           if b.status == "CHECKED_OUT" and 
                           b.check_out.date() == today)
        
        print(Fore.YELLOW + f"\n📅 Date: {today.strftime('%d/%m/%Y')}")
        print(f"\n📊 SUMMARY:")
        print(f"   ✅ Expected Check-ins: {len(today_checkins)}")
        print(f"   ❌ Expected Check-outs: {len(today_checkouts)}")
        print(f"   💰 Today's Revenue: ₹{today_revenue:.2f}")
        
        # Occupied rooms
        occupied = len([r for r in self.rooms if r.status == "OCCUPIED"])
        print(f"   👤 Currently Occupied: {occupied}")
        
        # Available rooms
        available = len([r for r in self.rooms if r.status == "AVAILABLE"])
        print(Fore.GREEN + f"   ✅ Available Rooms: {available}")
    
    def guest_feedback(self):
        """Record guest feedback"""
        print(Fore.GREEN + "\n⭐ GUEST FEEDBACK")
        print(Fore.CYAN + "-" * 40)
        
        booking_id = int(input("Enter Booking ID: "))
        
        for booking in self.bookings:
            if booking.booking_id == booking_id and booking.status == "CHECKED_OUT":
                
                print("\nRate your experience (1-5):")
                
                try:
                    cleanliness = int(input("   Cleanliness: "))
                    service = int(input("   Service: "))
                    amenities = int(input("   Amenities: "))
                    value = int(input("   Value for Money: "))
                    
                    overall = (cleanliness + service + amenities + value) / 4
                    
                    comments = input("\nAdditional Comments: ")
                    
                    print(Fore.GREEN + f"\n✅ Thank you for your feedback!")
                    print(f"   Overall Rating: {overall:.1f}/5.0")
                    
                    if overall >= 4.5:
                        print(Fore.YELLOW + "   ⭐⭐⭐⭐⭐ Excellent!")
                    elif overall >= 3.5:
                        print(Fore.CYAN + "   ⭐⭐⭐⭐ Good!")
                    elif overall >= 2.5:
                        print(Fore.WHITE + "   ⭐⭐⭐ Average")
                    else:
                        print(Fore.RED + "   ⭐⭐ Needs Improvement")
                    
                except:
                    print(Fore.RED + "❌ Invalid rating!")
                
                return
        
        print(Fore.RED + "❌ Booking not found or not checked out!")
    
    # ==================== DATA MANAGEMENT ====================
    
    def save_data(self):
        """Save all data to JSON file"""
        data = {
            'rooms': [r.to_dict() for r in self.rooms],
            'guests': [g.to_dict() for g in self.guests],
            'bookings': [b.to_dict() for b in self.bookings],
            'staff': [s.to_dict() for s in self.staff],
            'services': [s.to_dict() for s in self.services],
            'next_guest_id': self.next_guest_id,
            'next_booking_id': self.next_booking_id,
            'next_staff_id': self.next_staff_id,
            'next_service_id': self.next_service_id
        }
        
        with open('hotel_data.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        """Load data from JSON file"""
        try:
            with open('hotel_data.json', 'r') as f:
                data = json.load(f)
            
            # Load rooms
            self.rooms = []
            for r_data in data['rooms']:
                room = Room(
                    r_data['room_number'],
                    r_data['room_type'],
                    r_data['price'],
                    r_data['capacity'],
                    r_data['amenities']
                )
                room.status = r_data['status']
                room.current_guest = r_data['current_guest']
                if r_data['check_in_date']:
                    room.check_in_date = datetime.datetime.fromisoformat(r_data['check_in_date'])
                if r_data['check_out_date']:
                    room.check_out_date = datetime.datetime.fromisoformat(r_data['check_out_date'])
                self.rooms.append(room)
            
            # Load guests
            self.guests = []
            for g_data in data['guests']:
                guest = Guest(
                    g_data['guest_id'],
                    g_data['name'],
                    g_data['phone'],
                    g_data['email'],
                    g_data['address'],
                    g_data['id_proof'],
                    g_data['id_number']
                )
                guest.registration_date = datetime.datetime.fromisoformat(g_data['registration_date'])
                guest.total_stays = g_data['total_stays']
                guest.total_spent = g_data['total_spent']
                guest.vip_status = g_data['vip_status']
                self.guests.append(guest)
            
            # Load bookings
            self.bookings = []
            for b_data in data['bookings']:
                booking = Booking(
                    b_data['booking_id'],
                    b_data['guest_id'],
                    b_data['room_number'],
                    datetime.datetime.fromisoformat(b_data['check_in']),
                    datetime.datetime.fromisoformat(b_data['check_out']),
                    b_data['adults'],
                    b_data['children'],
                    b_data['total_amount']
                )
                booking.booking_date = datetime.datetime.fromisoformat(b_data['booking_date'])
                booking.status = b_data['status']
                booking.payment_status = b_data['payment_status']
                booking.payment_method = b_data['payment_method']
                booking.special_requests = b_data['special_requests']
                self.bookings.append(booking)
            
            # Load staff
            self.staff = []
            for s_data in data['staff']:
                staff = Staff(
                    s_data['staff_id'],
                    s_data['name'],
                    s_data['position'],
                    s_data['department'],
                    s_data['phone'],
                    s_data['email'],
                    s_data['salary']
                )
                staff.join_date = datetime.datetime.fromisoformat(s_data['join_date'])
                staff.status = s_data['status']
                self.staff.append(staff)
            
            # Load services
            self.services = []
            for s_data in data['services']:
                service = Service(
                    s_data['service_id'],
                    s_data['name'],
                    s_data['category'],
                    s_data['price'],
                    s_data['description']
                )
                service.available = s_data['available']
                self.services.append(service)
            
            # Load next IDs
            self.next_guest_id = data['next_guest_id']
            self.next_booking_id = data['next_booking_id']
            self.next_staff_id = data['next_staff_id']
            self.next_service_id = data['next_service_id']
            
        except FileNotFoundError:
            pass
        except Exception as e:
            print(Fore.RED + f"Error loading data: {e}")
    
    def run(self):
        """Main program loop"""
        while True:
            self.display_header()
            self.display_main_menu()
            
            try:
                choice = input(Fore.YELLOW + "\nEnter your choice: ")
                
                # Room Management (1-5)
                if choice == '1':
                    self.view_all_rooms()
                elif choice == '2':
                    self.search_available_rooms()
                elif choice == '3':
                    self.add_new_room()
                elif choice == '4':
                    self.update_room_details()
                elif choice == '5':
                    self.room_maintenance()
                
                # Guest Management (6-10)
                elif choice == '6':
                    self.register_guest()
                elif choice == '7':
                    self.view_all_guests()
                elif choice == '8':
                    self.search_guest()
                elif choice == '9':
                    self.update_guest_details()
                elif choice == '10':
                    self.vip_management()
                
                # Booking Management (11-16)
                elif choice == '11':
                    self.new_booking()
                elif choice == '12':
                    self.check_in()
                elif choice == '13':
                    self.check_out()
                elif choice == '14':
                    self.view_all_bookings()
                elif choice == '15':
                    self.cancel_booking()
                elif choice == '16':
                    self.process_payment()
                
                # Staff Management (17-20)
                elif choice == '17':
                    self.add_staff()
                elif choice == '18':
                    self.view_all_staff()
                elif choice == '19':
                    self.update_staff()
                elif choice == '20':
                    print(Fore.YELLOW + "⏳ Staff Attendance feature coming soon!")
                
                # Services (21-24)
                elif choice == '21':
                    self.restaurant_services()
                elif choice == '22':
                    self.spa_services()
                elif choice == '23':
                    self.housekeeping()
                elif choice == '24':
                    self.transport()
                
                # Reports (25-28)
                elif choice == '25':
                    self.occupancy_report()
                elif choice == '26':
                    self.revenue_report()
                elif choice == '27':
                    self.todays_summary()
                elif choice == '28':
                    self.guest_feedback()
                
                # Exit
                elif choice == '29':
                    print(Fore.GREEN + "\n👋 Thank you for using Hotel Management System!")
                    print(Fore.YELLOW + "🏨 Have a great day!")
                    break
                
                else:
                    print(Fore.RED + "❌ Invalid choice! Please try again.")
                    
            except KeyboardInterrupt:
                print(Fore.RED + "\n\n❌ Interrupted by user")
                break
            except Exception as e:
                print(Fore.RED + f"\n❌ Error: {e}")
            
            input(Fore.CYAN + "\nPress Enter to continue...")

# Main execution
if __name__ == "__main__":
    # Check required modules
    required_modules = ['tabulate', 'colorama']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(Fore.RED + "❌ Missing required modules!")
        print(Fore.YELLOW + f"Please install: {', '.join(missing_modules)}")
        print(Fore.YELLOW + "Run: pip install " + ' '.join(missing_modules))
        exit()
    
    # Run the hotel system
    try:
        hotel = HotelManagementSystem()
        hotel.run()
    except Exception as e:
        print(Fore.RED + f"❌ Fatal Error: {e}")
        print(Fore.YELLOW + "Please check your installation and try again.")
