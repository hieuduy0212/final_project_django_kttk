#!/bin/bash

project_path="/home/hieunguyen/Documents/django/cuoiky"

declare -A services=(
    ["FE"]="8000"
    ["Doctor Service"]="8001"
    ["Patient Service"]="8002"
    ["Room Bed Service"]="8003"
    ["Appointment Service"]="8004"
    ["Medicine Material Service"]="8005"
    ["Invoice Payment Service"]="8006"
    ["Patient Record Service"]="8007"
    ["Staff Service"]="8008"
)

for service in "${!services[@]}"; do
    port="${services[$service]}"
    service_path=$(echo "$service" | tr '[:upper:]' '[:lower:]' | tr ' ' '_')

    gnome-terminal --tab --title="$service" -- bash -c "
        source \"$project_path/bin/activate\" &&
        cd \"$project_path/$service_path\" &&
        python manage.py runserver $port;
        exec bash"
done
