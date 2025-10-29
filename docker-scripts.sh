#!/bin/bash

# Food Token Scanner - Docker Build and Deploy Scripts

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to build the application
build_app() {
    print_status "Building Food Token Scanner application..."
    docker build -t food-token-scanner:latest .
    print_success "Application built successfully!"
}

# Function to run the application in development mode
dev_run() {
    print_status "Starting application in development mode..."
    docker-compose -f docker-compose.dev.yml up --build
}

# Function to run the application in production mode
prod_run() {
    print_status "Starting application in production mode..."
    docker-compose up -d --build
    print_success "Application started in production mode!"
    print_status "Access the application at: http://localhost:3000"
    print_status "Admin Dashboard: http://localhost:3000/admin"
    print_status "Scanner Interface: http://localhost:3000/scanner"
}

# Function to stop the application
stop_app() {
    print_status "Stopping Food Token Scanner application..."
    docker-compose down
    docker-compose -f docker-compose.dev.yml down
    print_success "Application stopped!"
}

# Function to view logs
view_logs() {
    print_status "Viewing application logs..."
    docker-compose logs -f food-token-scanner
}

# Function to clean up Docker resources
cleanup() {
    print_status "Cleaning up Docker resources..."
    docker-compose down -v
    docker-compose -f docker-compose.dev.yml down -v
    docker system prune -f
    print_success "Cleanup completed!"
}

# Function to backup data
backup_data() {
    print_status "Creating backup of application data..."
    mkdir -p backups
    BACKUP_NAME="food-scanner-backup-$(date +%Y%m%d-%H%M%S)"
    
    # Create backup directory
    mkdir -p "backups/$BACKUP_NAME"
    
    # Backup database
    docker cp food-token-scanner:/app/database "backups/$BACKUP_NAME/"
    
    # Backup QR codes
    docker cp food-token-scanner:/app/qr-codes "backups/$BACKUP_NAME/"
    
    # Create archive
    tar -czf "backups/$BACKUP_NAME.tar.gz" -C backups "$BACKUP_NAME"
    rm -rf "backups/$BACKUP_NAME"
    
    print_success "Backup created: backups/$BACKUP_NAME.tar.gz"
}

# Function to restore data
restore_data() {
    if [ -z "$1" ]; then
        print_error "Please provide backup file name"
        print_status "Usage: $0 restore <backup-file.tar.gz>"
        exit 1
    fi
    
    BACKUP_FILE="$1"
    if [ ! -f "$BACKUP_FILE" ]; then
        print_error "Backup file not found: $BACKUP_FILE"
        exit 1
    fi
    
    print_status "Restoring data from backup: $BACKUP_FILE"
    
    # Extract backup
    TEMP_DIR=$(mktemp -d)
    tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"
    
    # Stop application
    docker-compose down
    
    # Restore data
    BACKUP_DIR=$(ls "$TEMP_DIR")
    docker-compose up -d
    sleep 5  # Wait for container to start
    
    docker cp "$TEMP_DIR/$BACKUP_DIR/database" food-token-scanner:/app/
    docker cp "$TEMP_DIR/$BACKUP_DIR/qr-codes" food-token-scanner:/app/
    
    # Cleanup
    rm -rf "$TEMP_DIR"
    
    # Restart application
    docker-compose restart
    
    print_success "Data restored successfully!"
}

# Function to show application status
status() {
    print_status "Food Token Scanner Application Status:"
    echo ""
    docker-compose ps
    echo ""
    print_status "Docker images:"
    docker images | grep food-token-scanner
}

# Function to show help
show_help() {
    echo "Food Token Scanner - Docker Management Script"
    echo ""
    echo "Usage: $0 <command>"
    echo ""
    echo "Commands:"
    echo "  build       Build the application Docker image"
    echo "  dev         Start application in development mode"
    echo "  start       Start application in production mode"
    echo "  stop        Stop the application"
    echo "  restart     Restart the application"
    echo "  logs        View application logs"
    echo "  status      Show application status"
    echo "  backup      Create backup of application data"
    echo "  restore     Restore data from backup"
    echo "  cleanup     Clean up Docker resources"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build"
    echo "  $0 dev"
    echo "  $0 start"
    echo "  $0 backup"
    echo "  $0 restore backups/food-scanner-backup-20231028-120000.tar.gz"
}

# Main script logic
case "$1" in
    "build")
        check_docker
        build_app
        ;;
    "dev")
        check_docker
        dev_run
        ;;
    "start")
        check_docker
        prod_run
        ;;
    "stop")
        check_docker
        stop_app
        ;;
    "restart")
        check_docker
        stop_app
        sleep 2
        prod_run
        ;;
    "logs")
        check_docker
        view_logs
        ;;
    "status")
        check_docker
        status
        ;;
    "backup")
        check_docker
        backup_data
        ;;
    "restore")
        check_docker
        restore_data "$2"
        ;;
    "cleanup")
        check_docker
        cleanup
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
