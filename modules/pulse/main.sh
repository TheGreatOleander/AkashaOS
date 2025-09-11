#!/bin/bash
# Pulse: System heartbeat monitor
echo "=== AkashaOS Pulse ==="
echo "Uptime: $(uptime -p)"
echo "CPU Load: $(uptime | awk -F'load average:' '{ print $2 }')"
echo "Memory Usage:"
free -h
