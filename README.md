# CRUD-Master

A secure, scalable microservices-based CRUD application built with Flask and PostgreSQL. Features an API Gateway, Inventory Service, and Billing Service with message-driven asynchronous processing.

## Overview

CRUD-Master is a production-ready microservices architecture demonstrating:
- **API Gateway Pattern**: Single entry point for all client requests
- **Database per Service**: Independent databases for inventory and billing services
- **Asynchronous Messaging**: RabbitMQ for inter-service communication
- **Security Hardening**: Network isolation and access control
- **OpenAPI Documentation**: Comprehensive API specifications

## Architecture

```
┌─────────────────────────────────────────────────┐
│          Client Applications                     │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │   API Gateway       │
        │  (Port: 8081)       │
        └──────────┬──────────┘
                   │
        ┌──────────┴──────────────┐
        │                         │
┌───────▼────────┐        ┌───────▼─────────┐
│ Inventory Svc  │        │  Billing Svc    │
│  (Port: 8080)  │        │  (Port: 8082)   │
│                │        │                 │
│  PostgreSQL    │        │  PostgreSQL     │
│  movies_db     │        │  billing_db     │
└────────────────┘        └─────────┬───────┘
                                    │
                          ┌─────────▼────────┐
                          │    RabbitMQ      │
                          │  Message Queue   │
                          └──────────────────┘
```

## Prerequisites

- **VirtualBox** 6.0 or higher
- **Vagrant** 2.0 or higher
- **PostgreSQL** (for database management, optional if using VMs)
- **Python** 3.9+ (for local development)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/ismailsayen/CRUD-Master.git
cd CRUD-Master
```

### 2. Environment Configuration

Copy the example environment file and update it with your configuration:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```bash
# --- Inventory Service ---
INVENTORY_DATABASE_URL=postgresql://user:password@localhost:5432/movies_db
INVENTORY_HOST="127.0.0.1"
INVENTORY_PORT=8080

# --- Billing Service ---
BILLING_DATABASE_URL=postgresql://user:password@localhost:5432/billing_db
BILLING_HOST="127.0.0.1"
BILLING_PORT=8082
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASS=guest
RABBITMQ_VHOST=/
RABBITMQ_QUEUE=billing_queue

# --- API Gateway ---
API_GATEWAY_PORT=8081
API_GATEWAY_HOST="127.0.0.1"
```

### 3. Deploy with Vagrant

Start all microservices in isolated VMs:

```bash
# Start all VMs
vagrant up

# Start specific VM
vagrant up inventory
vagrant up billing
vagrant up api_gateway

# SSH into a VM
vagrant ssh inventory
vagrant ssh billing
vagrant ssh api_gateway

# Shutdown all VMs
vagrant halt

# Destroy all VMs
vagrant destroy
```

### 4. Local Development (Optional)

If you prefer local development without VMs:

```bash
# Navigate to service directory
cd srcs/inventory-app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the service
python server.py
```

Repeat for each service (`billing-app`, `api-gateway-app`).

## Services

### API Gateway (Port 8081)
- Central routing and load balancing
- Request validation and transformation

**Start**: `vagrant up api_gateway`

### Inventory Service (Port 8080)
- Product/Movie CRUD operations
- Database: PostgreSQL `movies_db`
- RESTful API for inventory management

**Start**: `vagrant up inventory`

**Dependencies**:
- Flask
- Flask-SQLAlchemy
- psycopg2-binary
- python-dotenv

### Billing Service (Port 8082)
- Billing and payment processing
- Database: PostgreSQL `billing_db`
- Message queue integration with RabbitMQ

**Start**: `vagrant up billing`

**Dependencies**:
- Flask
- Flask-SQLAlchemy
- psycopg2-binary
- RabbitMQ client (Pika)

## API Documentation

### OpenAPI/Swagger

Full API specifications are available in OpenAPI format:

- **Master OpenAPI**: `openapi.yaml`

```

### Testing the APIs

Use the provided test script:

```bash
# Run inventory API tests
cd srcs/inventory-app
python test_api.py
```

Or use curl:

```bash
# List all inventory items
curl http://localhost:8080/api/items

# Get specific item
curl http://localhost:8080/api/items/1

# Create new item
curl -X POST http://localhost:8080/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "New Movie", "description": "Description"}'
```

## Project Structure

```
CRUD-Master/
├── README.md                      # This file
├── openapi.yaml                   # Master OpenAPI specification
├── Vagrantfile                    # Vagrant configuration for VMs
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
│
├── scripts/                       # VM setup scripts
│   ├── inventory_setup.sh        # Inventory service setup
│   ├── billing_setup.sh          # Billing service setup
│   ├── gateway_setup.sh          # API Gateway setup
│   └── install_requirements.sh   # Dependency installer
│
└── srcs/                         # Source code
    ├── inventory-app/           # Inventory microservice
    │   ├── app/
    │   │   ├── __init__.py
    │   │   ├── models.py        # Database models
    │   │   ├── routes.py        # API endpoints
    │   │   └── config.py        # Service configuration
    │   ├── server.py            # Application entry point
    │   ├── requirements.txt      # Python dependencies
    │   └── test_api.py          # API tests
    │
    ├── billing-app/             # Billing microservice
    │   ├── app/
    │   │   ├── __init__.py
    │   │   ├── model.py         # Database models
    │   │   ├── route.py         # API endpoints
    │   │   └── config.py        # Service configuration
    │   ├── server.py            # Application entry point
    │   └── requirements.txt      # Python dependencies
    │
    └── api-gateway-app/         # API Gateway service
        ├── app/
        │   ├── __init__.py
        │   ├── route.py         # Routing logic
        │   └── config.py        # Gateway configuration
        ├── server.py            # Application entry point
        └── requirements.txt      # Python dependencies
```

## Security Features

✅ Network isolation via private networks  
✅ Service-to-service authentication  
✅ Database access control  
✅ Environment-based configuration (secrets not in code)  
✅ Input validation and sanitization  


## Development Workflow

### Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** in the appropriate service directory

3. **Test locally**:
   ```bash
   # For local testing
   cd srcs/inventory-app
   python -m pytest  # If pytest is configured
   python test_api.py
   ```

4. **Rebuild VMs if needed**:
   ```bash
   vagrant provision inventory  # Re-run provisioning scripts
   ```

5. **Commit and push**:
   ```bash
   git add .
   git commit -m "feat: describe your changes"
   git push origin feature/your-feature-name
   ```

### Debugging

```bash
# SSH into VM and view logs
vagrant ssh inventory

# Inside VM
# Logs are typically in /var/log or service-specific directories
tail -f /var/log/application.log

# Check service status
systemctl status inventory-service
```

## Troubleshooting

### VMs won't start
- Ensure VirtualBox is installed and running
- Check available disk space (each VM needs ~20GB)
- Verify network interfaces aren't in use

### Database connection fails
- Verify PostgreSQL is running on the VM
- Check `.env` database URL is correct
- Ensure `USER_DB` and `PASSWORD_DB` are set in `.env`

### Services can't communicate
- Check VM network configuration (should be 192.168.56.0/24)
- Verify firewall rules allow inter-service traffic
- Check RabbitMQ is running on the billing VM

### Port conflicts
- Verify ports 8080, 8081, 8082 are not in use
- Change ports in `.env` if needed and rebuild VMs

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please follow the existing code style and include tests for new functionality.

## Performance & Monitoring

- **Response Time**: Typical API response < 200ms
- **Database**: Optimized with proper indexing
- **Messaging**: RabbitMQ for reliable async operations



## Support & Contact

For issues, feature requests, or questions:
- Open an issue on GitHub
- Contact the development team

---

**Last Updated**: June 2026  
**Version**: 1.0.0  
**Maintainer**: [Ismail Sayen](https://github.com/ismailsayen), [Hassan El ouaziz](https://github.com/helouazizi) 
