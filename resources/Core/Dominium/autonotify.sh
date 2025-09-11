#!/data/data/com.termux/files/usr/bin/bash

# Empire AutoNotifications System
# Place in: /data/data/com.termux/files/home/empire/autonotify.sh

EMPIRE_DIR="$HOME/empire"
CONFIG_FILE="$EMPIRE_DIR/config"
LOG_FILE="$EMPIRE_DIR/empire.log"
NOTIFICATION_DIR="$EMPIRE_DIR/notifications"
REQUEST_DIR="$EMPIRE_DIR/requests"

# Load configuration
load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        source "$CONFIG_FILE"
    else
        echo "Config file not found. Creating template..."
        cat > "$CONFIG_FILE" << EOF
# Empire Configuration
GITHUB_TOKEN: <REDACTED>"
TELEGRAM_BOT_TOKEN: <REDACTED>"
TELEGRAM_CHAT_ID=""
ETH_WALLET="0xd0e9B76Eb4B3911281161CF891E3B03DAa77c74b"
EOF
        echo "Please edit $CONFIG_FILE with your Telegram Chat ID"
        exit 1
    fi
}

# Logging function
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
    echo "$1"
}

# Send Telegram notification
send_telegram() {
    local message="$1"
    local priority="${2:-normal}"
    
    if [[ -z "$TELEGRAM_CHAT_ID" ]]; then
        log_message "ERROR: Telegram Chat ID not configured"
        return 1
    fi
    
    # Trigger Tasker via intent
    am broadcast -a net.dinglisch.android.tasker.action.NOTIFICATION \
        --es message "$message" \
        --es priority "$priority" \
        2>/dev/null
    
    # Also send via Telegram API
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
        -d chat_id="$TELEGRAM_CHAT_ID" \
        -d text="🏛️ EMPIRE: $message" \
        -d parse_mode="Markdown" > /dev/null
    
    log_message "NOTIFICATION: $message"
}

# Handle different notification types
handle_notification() {
    local type="$1"
    local data="$2"
    
    case "$type" in
        "critical")
            send_telegram "🚨 CRITICAL: $data" "critical"
            ;;
        "request")
            echo "$data" > "$REQUEST_DIR/$(date +%s).req"
            send_telegram "📋 REQUEST: $data" "high"
            ;;
        "status")
            send_telegram "ℹ️ STATUS: $data" "normal"
            ;;
        "success")
            send_telegram "✅ SUCCESS: $data" "normal"
            ;;
        "error")
            send_telegram "❌ ERROR: $data" "high"
            ;;
        *)
            send_telegram "$data" "normal"
            ;;
    esac
}

# Process AutoDrop commands
handle_autodrop() {
    local command="$1"
    log_message "AutoDrop command received: $command"
    
    case "$command" in
        "thesis_save")
            handle_notification "status" "Thesis section saved to AutoDrop"
            ;;
        "council_debate")
            handle_notification "status" "Council debate initiated"
            ;;
        "git_sync")
            cd "$EMPIRE_DIR/repos" && git add . && git commit -m "AutoDrop sync $(date)"
            handle_notification "success" "Git repositories synchronized"
            ;;
        *)
            handle_notification "request" "Unknown AutoDrop command: $command"
            ;;
    esac
}

# Main execution
main() {
    case "$1" in
        "test")
            load_config
            send_telegram "Empire AutoNotifications System Online" "normal"
            ;;
        "start")
            load_config
            log_message "Empire system starting..."
            send_telegram "Empire system starting up..." "normal"
            # Keep running in background
            while true; do
                sleep 30
                # Check for pending requests
                if [[ -f "$REQUEST_DIR/pending" ]]; then
                    local request=$(cat "$REQUEST_DIR/pending")
                    handle_notification "request" "$request"
                    rm "$REQUEST_DIR/pending"
                fi
            done
            ;;
        "notify")
            load_config
            handle_notification "$2" "$3"
            ;;
        "autodrop")
            load_config
            handle_autodrop "$2"
            ;;
        "critical")
            load_config
            handle_notification "critical" "$2"
            ;;
        *)
            echo "Usage: $0 {test|start|notify|autodrop|critical}"
            echo "Empire AutoNotifications System"
            exit 1
            ;;
    esac
}

# Ensure directories exist
mkdir -p "$NOTIFICATION_DIR" "$REQUEST_DIR"

# Execute main function
main "$@"
