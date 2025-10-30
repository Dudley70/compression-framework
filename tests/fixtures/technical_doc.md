# System Architecture: CustomerService Integration

## Overview

The CustomerService integrates with PostgreSQL database, Redis cache, and RabbitMQ message broker. The system uses Docker containers orchestrated by Kubernetes with Kong API Gateway handling external traffic.

## Database Schema

### Customer Table
- CustomerID (Primary Key, UUID)
- FirstName (VARCHAR, Required)
- LastName (VARCHAR, Required) 
- EmailAddress (VARCHAR, Unique Index)
- PhoneNumber (VARCHAR, Optional)
- RegistrationDate (TIMESTAMP, Default NOW())
- LastLoginDate (TIMESTAMP, Nullable)

### Address Table  
- AddressID (Primary Key, UUID)
- CustomerID (Foreign Key → Customer.CustomerID)
- StreetAddress (VARCHAR, Required)
- City (VARCHAR, Required)
- StateProvince (VARCHAR, Required)
- PostalCode (VARCHAR, Required)
- CountryCode (CHAR(2), ISO 3166-1)

## API Endpoints

### CustomerController
- GET /api/v1/customers/{customerID} 
- POST /api/v1/customers (CreateCustomerRequest)
- PUT /api/v1/customers/{customerID} (UpdateCustomerRequest)
- DELETE /api/v1/customers/{customerID}

### AddressController
- GET /api/v1/customers/{customerID}/addresses
- POST /api/v1/customers/{customerID}/addresses (CreateAddressRequest)
- PUT /api/v1/addresses/{addressID} (UpdateAddressRequest)
- DELETE /api/v1/addresses/{addressID}

## Infrastructure Components

### Message Queues (RabbitMQ)
- customer.created.queue → NotificationService
- customer.updated.queue → AuditService  
- customer.deleted.queue → DataArchiveService

### Cache Strategy (Redis)
- Key Pattern: customer:{customerID}
- TTL: 300 seconds
- Invalidation: On customer updates via RabbitMQ events

### Monitoring & Observability
- Prometheus metrics: customer_service_requests_total, customer_service_duration_seconds
- Grafana dashboards: CustomerService Performance, Database Connections
- Jaeger tracing: Distributed request tracing across microservices
- ELK Stack: Centralized logging with structured JSON format

## External Dependencies
- OAuth2Server for authentication (JWT tokens)
- EmailService API for notifications
- GeocodeService API for address validation
- PaymentGateway API for billing integration