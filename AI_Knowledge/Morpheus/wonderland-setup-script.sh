#!/bin/bash
# AI Wonderland Setup Script for Ubuntu Server 24.10
# This script sets up the complete AI environment

set -e

echo "🌟 Welcome to AI Wonderland Setup! 🌟"
echo "Setting up your autonomous AI ecosystem..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install essential packages
echo "🔧 Installing essential packages..."
sudo apt install -y \
    curl \
    wget \
    git \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    docker.io \
    docker-compose \
    redis-server \
    postgresql \
    mongodb \
    nginx \
    ffmpeg \
    alsa-utils \
    v4l-utils \
    arduino \
    build-essential \
    cmake \
    pkg-config \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev

# Enable and start services
echo "🚀 Starting services..."
sudo systemctl enable docker
sudo systemctl start docker
sudo systemctl enable redis-server
sudo systemctl start redis-server
sudo systemctl enable postgresql
sudo systemctl start postgresql
sudo systemctl enable mongodb
sudo systemctl start mongodb

# Add user to docker group
sudo usermod -aG docker $USER

# Create project structure
echo "📁 Creating project structure..."
mkdir -p ~/ai-wonderland/{
    core,
    modules,
    agents,
    sensors,
    interfaces,
    data,
    storage,
    config,
    logs,
    docker,
    scripts,
    web
}

cd ~/ai-wonderland

# Create virtual environment
echo "🐍 Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python packages..."
pip install --upgrade pip
pip install \
    fastapi \
    uvicorn \
    websockets \
    redis \
    psycopg2-binary \
    pymongo \
    sqlalchemy \
    alembic \
    opencv-python \
    numpy \
    scipy \
    pandas \
    matplotlib \
    seaborn \
    plotly \
    streamlit \
    gradio \
    transformers \
    torch \
    torchaudio \
    torchvision \
    whisper \
    openai \
    anthropic \
    google-cloud-aiplatform \
    langchain \
    chromadb \
    pinecone-client \
    sentence-transformers \
    scikit-learn \
    networkx \
    neo4j \
    influxdb-client \
    paho-mqtt \
    pyserial \
    gpiozero \
    adafruit-circuitpython-dht \
    pygame \
    pydub \
    librosa \
    pillow \
    requests \
    aiohttp \
    asyncio \
    schedule \
    python-dotenv \
    pyyaml \
    jinja2 \
    click \
    rich \
    typer

# Install Ollama for local AI
echo "🤖 Installing Ollama for local AI..."
curl -fsSL https://ollama.ai/install.sh | sh

# Download some models (this will take a while)
echo "📥 Downloading AI models..."
ollama pull llama2:7b
ollama pull codellama:7b
ollama pull mistral:7b

# Install Node.js dependencies for web interface
echo "🌐 Setting up web interface..."
cd web
npm init -y
npm install \
    express \
    socket.io \
    vue \
    vuex \
    vue-router \
    three \
    d3 \
    chart.js \
    tone \
    web-audio-api \
    @tensorflow/tfjs

cd ..

# Create Docker Compose file
echo "🐳 Creating Docker Compose configuration..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - ./data/redis:/data
    restart: unless-stopped

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: wonderland
      POSTGRES_USER: ai
      POSTGRES_PASSWORD: <REDACTED>
    ports:
      - "5432:5432"
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
    restart: unless-stopped

  mongodb:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - ./data/mongodb:/data/db
    restart: unless-stopped

  influxdb:
    image: influxdb:2.7
    ports:
      - "8086:8086"
    environment:
      DOCKER_INFLUXDB_INIT_MODE: setup
      DOCKER_INFLUXDB_INIT_USERNAME: admin
      DOCKER_INFLUXDB_INIT_PASSWORD: <REDACTED>
      DOCKER_INFLUXDB_INIT_ORG: wonderland
      DOCKER_INFLUXDB_INIT_BUCKET: sensors
    volumes:
      - ./data/influxdb:/var/lib/influxdb2
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./config/nginx.conf:/etc/nginx/nginx.conf
      - ./web:/usr/share/nginx/html
    depends_on:
      - api
    restart: unless-stopped

  api:
    build:
      context: .
      dockerfile: docker/Dockerfile.api
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - /dev:/dev
    privileged: true
    restart: unless-stopped
    depends_on:
      - redis
      - postgres
      - mongodb
      - influxdb

  core:
    build:
      context: .
      dockerfile: docker/Dockerfile.core
    volumes:
      - .:/app
      - /dev:/dev
    privileged: true
    restart: unless-stopped
    depends_on:
      - redis
      - postgres
      - mongodb
      - api

  agents:
    build:
      context: .
      dockerfile: docker/Dockerfile.agents
    volumes:
      - .:/app
    restart: unless-stopped
    depends_on:
      - redis
      - core

  sensors:
    build:
      context: .
      dockerfile: docker/Dockerfile.sensors
    volumes:
      - .:/app
      - /dev:/dev
    privileged: true
    devices:
      - /dev/video0:/dev/video0
      - /dev/video1:/dev/video1
      - /dev/snd:/dev/snd
    restart: unless-stopped
    depends_on:
      - redis
      - influxdb
EOF

# Create Dockerfiles
echo "🐳 Creating Dockerfiles..."
mkdir -p docker

# API Dockerfile
cat > docker/Dockerfile.api << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "core.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
EOF

# Core Dockerfile
cat > docker/Dockerfile.core << 'EOF'
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    alsa-utils \
    v4l-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "core/wonderland_launcher.py"]
EOF

# Agents Dockerfile
cat > docker/Dockerfile.agents << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "agents/agent_swarm.py"]
EOF

# Sensors Dockerfile
cat > docker/Dockerfile.sensors << 'EOF'
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    alsa-utils \
    v4l-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "sensors/sensor_hub.py"]
EOF

# Create requirements.txt
echo "📋 Creating requirements.txt..."
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn==0.24.0
websockets==12.0
redis==5.0.1
psycopg2-binary==2.9.9
pymongo==4.6.0
sqlalchemy==2.0.23
opencv-python==4.8.1.78
numpy==1.24.3
pandas==2.0.3
torch==2.1.1
transformers==4.36.0
openai==1.3.7
anthropic==0.7.7
langchain==0.0.350
chromadb==0.4.18
sentence-transformers==2.2.2
networkx==3.2.1
influxdb-client==1.39.0
paho-mqtt==1.6.1
pyserial==3.5
pygame==2.5.2
pillow==10.1.0
requests==2.31.0
aiohttp==3.9.1
schedule==1.2.0
python-dotenv==1.0.0
pyyaml==6.0.1
rich==13.7.0
gradio==4.8.0
streamlit==1.28.2
EOF

# Create configuration files
echo "⚙️ Creating configuration files..."
mkdir -p config

# Environment variables
cat > .env << 'EOF'
# AI Wonderland Environment Variables

# Database URLs
REDIS_URL=redis://localhost:6379
POSTGRES_URL=postgresql://ai:wonderland123@localhost:5432/wonderland
MONGODB_URL=mongodb://localhost:27017/wonderland
INFLUXDB_URL=http://localhost:8086

# API Keys (fill these in)
OPENAI_your_openai_key_here: <REDACTED>
ANTHROPIC_your_anthropic_key_here: <REDACTED>
GOOGLE_your_google_key_here: <REDACTED>

# System Configuration
LOG_LEVEL=INFO
DEBUG=true
MAX_AGENTS=10
SENSOR_POLL_INTERVAL=1.0
MEMORY_RETENTION_DAYS=365
EOF

# Nginx configuration
cat > config/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:8000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            root /usr/share/nginx/html;
            index index.html;
            try_files $uri $uri/ /index.html;
        }

        location /api {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /ws {
            proxy_pass http://api;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
EOF

# Create startup scripts
echo "🚀 Creating startup scripts..."
mkdir -p scripts

cat > scripts/start_wonderland.sh << 'EOF'
#!/bin/bash
echo "🌟 Starting AI Wonderland..."

# Start Docker services
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to initialize..."
sleep 30

# Run database migrations
echo "🗄️ Setting up databases..."
python scripts/setup_databases.py

echo "✅ AI Wonderland is now running!"
echo "🌐 Web interface: http://localhost"
echo "🔌 API: http://localhost/api"
echo "📊 Monitor logs with: docker-compose logs -f"
EOF

chmod +x scripts/start_wonderland.sh

cat > scripts/stop_wonderland.sh << 'EOF'
#!/bin/bash
echo "🛑 Stopping AI Wonderland..."
docker-compose down
echo "✅ AI Wonderland stopped"
EOF

chmod +x scripts/stop_wonderland.sh

# Create basic web interface
echo "🌐 Creating web interface..."
cat > web/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Wonderland</title>
    <script src="https://cdn.jsdelivr.net/npm/vue@3/dist/vue.global.js"></script>
    <script src="https://cdn.socket.io/4.7.4/socket.io.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { font-size: 3em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { 
            background: rgba(255,255,255,0.1); 
            backdrop-filter: blur(10px);
            border-radius: 15px; 
            padding: 20px; 
            border: 1px solid rgba(255,255,255,0.2);
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .online { background-color: #4ade80; }
        .offline { background-color: #ef4444; }
        .log { 
            background: rgba(0,0,0,0.2); 
            border-radius: 8px; 
            padding: 10px; 
            max-height: 200px; 
            overflow-y: auto; 
            font-family: monospace; 
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div id="app">
        <div class="container">
            <div class="header">
                <h1>🌟 AI Wonderland 🌟</h1>
                <p>Your Autonomous AI Ecosystem</p>
            </div>
            
            <div class="dashboard">
                <div class="card">
                    <h3>🧠 System Status</h3>
                    <p><span :class="systemStatus.online ? 'status-indicator online' : 'status-indicator offline'"></span>
                       {{ systemStatus.online ? 'Online' : 'Offline' }}</p>
                    <p>Uptime: {{ systemStatus.uptime }}</p>
                    <p>Active Agents: {{ systemStatus.activeAgents }}</p>
                </div>
                
                <div class="card">
                    <h3>👁️ Sensors</h3>
                    <div v-for="sensor in sensors" :key="sensor.name">
                        <p><span :class="sensor.active ? 'status-indicator online' : 'status-indicator offline'"></span>
                           {{ sensor.name }}: {{ sensor.value }}</p>
                    </div>
                </div>
                
                <div class="card">
                    <h3>🤖 Active Agents</h3>
                    <div v-for="agent in agents" :key="agent.name">
                        <p><span :class="agent.active ? 'status-indicator online' : 'status-indicator offline'"></span>
                           {{ agent.name }}</p>
                        <small>{{ agent.status }}</small>
                    </div>
                </div>
                
                <div class="card">
                    <h3>💭 Recent Thoughts</h3>
                    <div class="log">
                        <div v-for="thought in recentThoughts" :key="thought.id">
                            <small>{{ new Date(thought.timestamp).toLocaleTimeString() }}</small><br>
                            {{ thought.content }}
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h3>🎨 Latest Creation</h3>
                    <div v-if="latestCreation">
                        <p><strong>{{ latestCreation.type }}</strong></p>
                        <p>{{ latestCreation.description }}</p>
                        <small>Created: {{ new Date(latestCreation.timestamp).toLocaleString() }}</small>
                    </div>
                    <p v-else>No creations yet...</p>
                </div>
                
                <div class="card">
                    <h3>📊 Memory Usage</h3>
                    <p>Total Memories: {{ memoryStats.total }}</p>
                    <p>Recent: {{ memoryStats.recent }}</p>
                    <p>Emotional Weight: {{ memoryStats.emotionalWeight }}</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        const { createApp } = Vue;
        
        createApp({
            data() {
                return {
                    systemStatus: {
                        online: false,
                        uptime: '0s',
                        activeAgents: 0
                    },
                    sensors: [
                        { name: 'Camera Array', active: false, value: 'No signal' },
                        { name: 'Microphones', active: false, value: 'Silent' },
                        { name: 'Temperature', active: false, value: '-- °C' },
                        { name: 'Motion', active: false, value: 'None detected' }
                    ],
                    agents: [
                        { name: 'Perception Agent', active: false, status: 'Initializing...' },
                        { name: 'Creative Agent', active: false, status: 'Waiting...' },
                        { name: 'Social Agent', active: false, status: 'Offline' },
                        { name: 'Learning Agent', active: false, status: 'Dormant' }
                    ],
                    recentThoughts: [
                        { id: 1, timestamp: Date.now(), content: 'System initializing... checking sensors...' }
                    ],
                    latestCreation: null,
                    memoryStats: {
                        total: 0,
                        recent: 0,
                        emotionalWeight: 0.5
                    }
                }
            },
            mounted() {
                // Connect to WebSocket for real-time updates
                const socket = io('/ws');
                
                socket.on('system_status', (data) => {
                    this.systemStatus = data;
                });
                
                socket.on('sensor_update', (data) => {
                    const sensor = this.sensors.find(s => s.name === data.name);
                    if (sensor) {
                        sensor.active = data.active;
                        sensor.value = data.value;
                    }
                });
                
                socket.on('agent