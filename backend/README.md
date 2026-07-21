# CargoFlow Backend

CargoFlow is a modern logistics and delivery management platform built with **Django REST Framework**. It enables customers to create shipments, automatically assigns available drivers, securely verifies package pickup and delivery using QR codes, and provides complete shipment tracking with an audit trail.

The goal of CargoFlow is to simplify delivery operations for businesses while ensuring transparency, accountability, and security throughout the delivery lifecycle.

---

# Features

## Authentication

- User registration
- Secure login using JWT
- Refresh tokens
- Role-based access
- Customer accounts
- Driver accounts
- Administrator accounts

---

## Shipment Management

Customers can:

- Create shipments
- View shipment history
- Track shipment status
- Cancel shipments before pickup
- View pickup QR code and pickup information

Each shipment includes:

- Tracking number
- UUID
- Package details
- Goods type
- Pickup address
- Delivery address
- Estimated delivery price
- Receiver information

---

## Automatic Driver Assignment

When a shipment is created, CargoFlow automatically assigns the most suitable available driver based on:

- Verification status
- Availability
- Delivery history
- Driver rating

Once assigned:

- Driver becomes BUSY
- Customer is notified
- Driver is notified
- Assignment event is recorded

---

## Secure Pickup Verification

Pickup is verified using a unique QR token.

Only the assigned driver can:

- Scan the pickup QR
- Confirm pickup
- Update shipment status

The system records:

- Pickup time
- Driver
- Shipment event

---

## Secure Delivery Verification

Delivery is completed using:

- Delivery QR token
- Delivery verification code

During delivery the system records:

- Receiver name
- Receiver phone number
- Delivery time
- Driver
- Shipment completion event

---

## Shipment Tracking

Customers can track shipments using the tracking number.

Tracking includes:

- Current shipment status
- Driver assigned
- Shipment timeline
- Shipment history
- Audit events

---

## Shipment Event History

Every important action creates an immutable shipment event.

Examples include:

- Shipment created
- Driver assigned
- Pickup completed
- Delivery completed
- Shipment cancelled

Each event records:

- Event type
- Description
- User who performed the action
- Timestamp

This provides a complete audit trail.

---

## Driver Dashboard

Drivers can:

- View assigned deliveries
- View delivery details
- Confirm pickup
- Confirm delivery

---

## Administrator Dashboard

Administrators can:

- View all shipments
- View platform statistics
- View all customers
- View all drivers

---

# Technology Stack

| Technology | Purpose |
|------------|---------|
| Python 3.12 | Programming language |
| Django 6 | Backend framework |
| Django REST Framework | REST API |
| PostgreSQL | Database |
| JWT | Authentication |
| Pipenv | Dependency management |
| drf-spectacular | OpenAPI documentation |

---

# Project Structure

```
backend/
│
├── apps/
│   ├── accounts/
│   ├── shipments/
│   └── common/
│
├── config/
│
├── manage.py
│
├── Pipfile
│
└── README.md
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/yourusername/CargoFlow.git

cd CargoFlow/backend
```

---

## Create virtual environment

```bash
pipenv install

pipenv shell
```

---

## Configure environment variables

Create a `.env` file.

Example:

```env
SECRET_KEY=your_secret_key

DEBUG=True

DB_NAME=cargoflow

DB_USER=postgres

DB_PASSWORD=your_password

DB_HOST=localhost

DB_PORT=5432
```

---

## Apply migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

---

## Create superuser

```bash
python manage.py createsuperuser
```

---

## Start the server

```bash
python manage.py runserver
```

The API will be available at:

```
http://127.0.0.1:8000/
```

---

# API Documentation

Swagger UI

```
http://127.0.0.1:8000/api/docs/
```

OpenAPI Schema

```
http://127.0.0.1:8000/api/schema/
```

ReDoc

```
http://127.0.0.1:8000/api/redoc/
```

---

# Shipment Workflow

```
Customer

↓

Create Shipment

↓

Automatic Driver Assignment

↓

Driver Receives Notification

↓

Driver Confirms Pickup (QR)

↓

Shipment In Transit

↓

Driver Confirms Delivery
(QR + Delivery Code)

↓

Receiver Information Recorded

↓

Shipment Completed

↓

Shipment History Updated
```

---

# Security

CargoFlow uses:

- JWT Authentication
- Role-based permissions
- UUIDs for public resources
- Secure QR verification
- Delivery verification codes
- Shipment audit logging

---

# Future Improvements

Planned features include:

- Live GPS tracking
- Google Maps integration
- Route optimization
- AI-powered driver assignment
- Push notifications
- Email notifications
- SMS notifications
- Digital signatures
- Payment gateway integration
- Company accounts
- Multi-branch logistics
- Driver mobile application
- Customer mobile application
- Analytics dashboard
- Reporting and exports

---

# Contributing

Contributions are welcome.

1. Fork the repository.

2. Create a feature branch.

```bash
git checkout -b feature/new-feature
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push to GitHub.

```bash
git push origin feature/new-feature
```

5. Open a Pull Request.

---

# License

MIT License

Copyright (c) 2026 samsonmorara-maker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


---

# Author

**Samson Manoti**


GitHub: https://github.com/samsonmorara-maker/CargoFlow.git

---

Built  using Django REST Framework.