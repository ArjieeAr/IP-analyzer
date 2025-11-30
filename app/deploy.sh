#!/bin/bash
echo "Deploying application to local server..."

# Copy project files to server directory
sudo cp -r . /var/www/my_python_app

# Restart your Python service
sudo systemctl restart my_python_app

