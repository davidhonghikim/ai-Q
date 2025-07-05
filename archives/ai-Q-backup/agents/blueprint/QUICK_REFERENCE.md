# AI-Q Knowledge Library System - Quick Reference

## System Overview
- **System Name**: AI-Q Knowledge Library System (AI-Q KLS)
- **Version**: 2.1.0
- **Architecture**: Hardware Auto-Detection + Feature Flagging
- **Environment**: Development/Production Ready

---

## Directory Structure

### System Root (Writable) - `E:\kos\griot-main-win11\Q\`
```
Q/
├── frontend/                    # Web interface and API server
│   ├── api/                    # API modules and services
│   │   ├── models.py          # Data models and schemas
│   │   ├── content_service.py # File analysis service
│   │   ├── search_service.py  # RAG and search service
│   │   ├── services.py        # Service management
│   │   └── scheduled_updater.py # Background updates
│   ├── static/                 # Web assets (CSS, JS, images)
│   ├── api_server_modular.py  # Main API server
│   ├── test_server.py         # Simple test server
│   └── system_monitor.py      # System monitoring
├── scripts/                    # Utility scripts
│   ├── hardware_detector.py   # Hardware auto-detection
│   ├── system_execution_guide.py # System startup guide
│   ├── gpu_setup.py          # GPU optimization
│   └── enhanced_gpu_setup.py # Advanced GPU setup
├── config/                     # Configuration files
│   ├── hardware_detection.json # Hardware analysis results
│   ├── feature_flags.yml      # Auto-generated feature flags
│   ├── system_config.yml      # System configuration
│   └── content_service_config.json # Content service config
├── data/                       # Generated data and indexes
│   ├── search_indexes/        # Vector and keyword indexes
│   └── embeddings/            # Document embeddings
├── logs/                       # System logs
│   ├── system_execution.log   # Main system logs
│   ├── hardware_detection.log # Hardware analysis logs
│   ├── api_server.log         # API server logs
│   └── search_service.log     # Search service logs
└── search_indexes/            # Search service indexes
    ├── embeddings.npy         # Vector embeddings
    ├── bm25_index.pkl         # Keyword search index
    ├── document_hashes.json   # Document change tracking
    └── metadata.json          # Index metadata
```

### Reference Root (Read-Only) - `E:\kos\griot-main\`
```
griot-main/
├── ai-q/                      # AI-Q specifications and documentation
├── agents/                    # Agent system documentation
├── apps/                      # Application modules
├── packages/                  # Core packages and libraries
├── docs/                      # Project documentation
└── scripts/                   # Reference scripts
```

---

## Services & Ports

### Core Services
| Service | Port | Status | Description | Health Check |
|---------|------|--------|-------------|--------------|
| API Server | 8000 | Active | FastAPI REST API | `GET /api/status` |
| Content Service | N/A | Active | File analysis & indexing | Internal |
| Search Service | N/A | Active | RAG & semantic search | Internal |
| System Monitor | N/A | Active | Performance monitoring | Internal |
| Scheduled Updater | N/A | Active | Background updates | Internal |

### External Services (Future)
| Service | Port | Status | Description | Default Credentials |
|---------|------|--------|-------------|-------------------|
| PostgreSQL | 5432 | Planned | Primary database | `postgres/postgres` |
| Redis | 6379 | Planned | Cache layer | None |
| Elasticsearch | 9200 | Planned | Search engine | None |
| MinIO | 9000 | Planned | Object storage | `minioadmin/minioadmin` |
| Weaviate | 8080 | Planned | Vector database | None |
| Neo4j | 7474 | Planned | Graph database | `neo4j/neo4j` |
| Grafana | 3000 | Planned | Monitoring dashboard | `admin/admin` |

---

## Web Interface URLs

### Main Interface
- **Dashboard**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

### API Endpoints

#### System Status & Health
```
GET  /api/status                    # System status overview
GET  /api/services                  # Service information
GET  /api/metrics                   # Performance metrics
GET  /api/metrics/comprehensive     # Detailed system metrics
GET  /api/metrics/gpus              # GPU metrics
GET  /api/metrics/cpu               # CPU metrics
GET  /api/metrics/memory            # Memory metrics
GET  /api/metrics/disks             # Disk metrics
GET  /api/metrics/network           # Network metrics
```

#### Content Management
```
GET  /api/content/summary           # Content analysis summary
GET  /api/content/performance       # Content processing metrics
GET  /api/content/file-types        # File type distribution
GET  /api/content/update-status     # Update status
GET  /api/content/indexing-status   # Indexing status
POST /api/content/refresh           # Refresh content database
```

#### Search & RAG
```
POST /api/rag/query                 # RAG search query
POST /api/rag/query/stream          # Streaming RAG results
GET  /api/search                    # General search
```

#### Scheduled Updates
```
POST /api/content/scheduled-update/start    # Start scheduled updates
POST /api/content/scheduled-update/stop     # Stop scheduled updates
GET  /api/content/scheduled-update/status   # Update service status
POST /api/content/scheduled-update/force    # Force immediate update
```

#### System Management
```
GET  /api/logs                      # System logs
DELETE /api/logs                    # Clear logs
POST /api/services/restart          # Restart services
```

---

## Configuration Files

### System Configuration (`config/system_config.yml`)
```yaml
system:
  name: "AI-Q Knowledge Library System"
  version: "2.1.0"
  environment: "development"

server:
  host: "0.0.0.0"
  port: 8000
  workers: 4
  timeout: 30

content_service:
  scan_interval_hours: 1
  max_file_size_mb: 10
  supported_extensions: [".md", ".yml", ".yaml", ".json", ".py", ".js", ".ts"]

search_service:
  embedding_model: "all-MiniLM-L6-v2"
  batch_size: 64
  update_frequency_hours: 1
  similarity_threshold: 0.1
```

### Hardware Detection (`config/hardware_detection.json`)
```json
{
  "system_info": {
    "platform": "Windows",
    "architecture": "x86_64",
    "python_version": "3.9.0"
  },
  "hardware_capabilities": {
    "cpu": {
      "logical_cores": 8,
      "performance_tier": "medium"
    },
    "memory": {
      "total_gb": 16,
      "performance_tier": "high"
    },
    "gpu": {
      "gpu_count": 1,
      "gpu_available": true
    }
  },
  "feature_flags": {
    "gpu_acceleration": true,
    "parallel_processing": true
  }
}
```

### Feature Flags (`config/feature_flags.yml`)
```yaml
hardware:
  cpu:
    high_performance: true
    multi_core_optimization: true
  gpu:
    cuda_available: true
    multi_gpu_support: false
  memory:
    high_capacity: true
  storage:
    fast_storage: true

services:
  search_acceleration: true
  parallel_processing: true
  gpu_embeddings: true
```

---

## Environment Variables

### Server Configuration
```bash
AIQ_SERVER_HOST=0.0.0.0
AIQ_SERVER_PORT=8000
AIQ_SERVER_WORKERS=4
AIQ_SERVER_TIMEOUT=30
```

### Content Service
```bash
AIQ_CONTENT_SCAN_INTERVAL=1
AIQ_CONTENT_MAX_FILE_SIZE=10
AIQ_CONTENT_SUPPORTED_EXTENSIONS=.md,.yml,.yaml,.json,.py,.js,.ts
```

### Search Service
```bash
AIQ_SEARCH_MODEL=all-MiniLM-L6-v2
AIQ_SEARCH_BATCH_SIZE=64
AIQ_SEARCH_UPDATE_FREQUENCY=1
AIQ_SEARCH_SIMILARITY_THRESHOLD=0.1
```

### Hardware Configuration
```bash
AIQ_GPU_MEMORY_FRACTION=0.8
AIQ_MAX_WORKERS=8
AIQ_ENABLE_GPU_ACCELERATION=true
AIQ_MULTI_GPU_SUPPORT=false
```

### Storage Configuration
```bash
AIQ_INDEX_PATH=search_indexes
AIQ_DATA_PATH=data
AIQ_LOGS_PATH=logs
AIQ_MAX_INDEX_SIZE_GB=10
```

### Monitoring Configuration
```bash
AIQ_METRICS_INTERVAL=30
AIQ_HEALTH_CHECK_INTERVAL=60
AIQ_LOG_LEVEL=INFO
AIQ_ENABLE_ALERTING=false
```

---

## Default Logins & Authentication

### Current System
- **Authentication**: None (development mode)
- **API Access**: Open (no authentication required)
- **Admin Interface**: None (planned for future)

### Planned Authentication (Future)
```yaml
authentication:
  method: "oauth2"
  providers:
    - name: "local"
      username: "admin"
      password: "admin123"
    - name: "ldap"
      server: "ldap://localhost:389"
      base_dn: "dc=example,dc=com"
  jwt:
    secret: "your-secret-key"
    algorithm: "HS256"
    expiration_hours: 24
```

---

## Log Files & Monitoring

### Log Locations
```
logs/
├── system_execution.log       # Main system logs
├── hardware_detection.log     # Hardware analysis logs
├── api_server.log            # API server logs
├── search_service.log        # Search service logs
├── content_service.log       # Content service logs
└── error.log                 # Error logs
```

### Log Levels
- **DEBUG**: Detailed debugging information
- **INFO**: General information messages
- **WARNING**: Warning messages
- **ERROR**: Error messages
- **CRITICAL**: Critical error messages

### Monitoring Endpoints
```
GET /api/metrics/comprehensive  # Full system metrics
GET /api/metrics/gpus          # GPU utilization
GET /api/metrics/cpu           # CPU utilization
GET /api/metrics/memory        # Memory usage
GET /api/metrics/disks         # Disk usage
GET /api/metrics/network       # Network metrics
```

---

## Startup & Shutdown

### Startup Commands
```bash
# Full system startup
cd Q/scripts
python system_execution_guide.py

# Quick API server only
cd Q/frontend
python api_server_modular.py

# Test server
cd Q/frontend
python test_server.py
```

### Shutdown Commands
```bash
# Graceful shutdown (Ctrl+C in terminal)
# Or kill process by PID
taskkill /PID <PID> /F

# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Health Check Commands
```bash
# Check if server is running
curl http://localhost:8000/api/status

# Check system metrics
curl http://localhost:8000/api/metrics

# Check content status
curl http://localhost:8000/api/content/summary
```

---

## Troubleshooting

### Common Issues

#### Port 8000 Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F

# Or use different port
set AIQ_SERVER_PORT=8001
```

#### Hardware Detection Failures
```bash
# Run hardware detection manually
cd Q/scripts
python hardware_detector.py

# Check logs
tail -f logs/hardware_detection.log
```

#### Search Service Issues
```bash
# Check search service status
curl http://localhost:8000/api/content/indexing-status

# Force content refresh
curl -X POST http://localhost:8000/api/content/refresh
```

#### Memory Issues
```bash
# Check memory usage
curl http://localhost:8000/api/metrics/memory

# Reduce batch size in config
# Edit config/system_config.yml
```

### Debug Mode
```bash
# Enable debug logging
set AIQ_LOG_LEVEL=DEBUG

# Start with debug output
python -u api_server_modular.py
```

---

## Performance Tuning

### High-Performance Configuration
```yaml
hardware:
  gpu_memory_fraction: 0.9
  max_workers: 16
  enable_gpu_acceleration: true

search_service:
  batch_size: 128
  embedding_model: "all-mpnet-base-v2"

content_service:
  max_workers: 8
  chunk_size: 2000
```

### Resource-Constrained Configuration
```yaml
hardware:
  gpu_memory_fraction: 0.5
  max_workers: 2
  enable_gpu_acceleration: false

search_service:
  batch_size: 16
  embedding_model: "all-MiniLM-L6-v2"

content_service:
  max_workers: 2
  chunk_size: 500
```

---

## API Examples

### RAG Query
```bash
curl -X POST http://localhost:8000/api/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does the agent system work?",
    "search_type": "hybrid",
    "top_k": 10,
    "alpha": 0.5
  }'
```

### Content Refresh
```bash
curl -X POST http://localhost:8000/api/content/refresh
```

### System Status
```bash
curl http://localhost:8000/api/status
```

### Search
```bash
curl "http://localhost:8000/api/search?q=agent&search_type=hybrid&k=5"
```

---

## File Extensions & Types

### Supported File Types
- **Markdown**: `.md`, `.markdown`
- **YAML**: `.yml`, `.yaml`
- **JSON**: `.json`
- **Python**: `.py`
- **JavaScript**: `.js`
- **TypeScript**: `.ts`
- **Text**: `.txt`
- **Configuration**: `.conf`, `.config`

### Excluded Patterns
- `*.log`
- `*.tmp`
- `node_modules/`
- `.git/`
- `__pycache__/`
- `*.pyc`

---

## Data Storage

### Index Files
```
search_indexes/
├── embeddings.npy         # Vector embeddings (NumPy array)
├── bm25_index.pkl         # BM25 keyword index (Pickle)
├── document_hashes.json   # Document change tracking
└── metadata.json          # Index metadata
```

### Data Files
```
data/
├── embeddings/            # Document embeddings
├── cache/                 # Temporary cache files
└── exports/               # Data exports
```

### Configuration Files
```
config/
├── hardware_detection.json # Hardware analysis results
├── feature_flags.yml      # Auto-generated feature flags
├── system_config.yml      # System configuration
└── content_service_config.json # Content service config
```

---

## Security Considerations

### Current Security Status
- **Authentication**: None (development mode)
- **Authorization**: None
- **Encryption**: None
- **Rate Limiting**: None
- **CORS**: Enabled for all origins

### Planned Security Features
- OAuth2/JWT authentication
- Role-based access control
- API rate limiting
- Request validation
- Audit logging
- Data encryption

---

## Backup & Recovery

### Backup Locations
```
backups/
├── config/                 # Configuration backups
├── data/                   # Data backups
├── indexes/                # Index backups
└── logs/                   # Log backups
```

### Backup Commands
```bash
# Backup configuration
cp -r config/ backups/config/$(date +%Y%m%d_%H%M%S)/

# Backup data
cp -r data/ backups/data/$(date +%Y%m%d_%H%M%S)/

# Backup indexes
cp -r search_indexes/ backups/indexes/$(date +%Y%m%d_%H%M%S)/
```

---

## Version History

### Current Version: 2.1.0
- Hardware auto-detection
- Feature flagging
- Modular API architecture
- Enhanced search capabilities
- System monitoring

### Previous Versions
- **2.0.0**: Initial modular release
- **1.0.0**: Basic functionality

---

## Support & Contact

### Documentation
- **Main README**: `README.md`
- **API Documentation**: http://localhost:8000/docs
- **System Guide**: `scripts/system_execution_guide.py`

### Logs & Debugging
- **System Logs**: `logs/system_execution.log`
- **API Logs**: Console output
- **Error Logs**: `logs/error.log`

### Issues & Questions
- Check troubleshooting section above
- Review system logs
- Consult API documentation
- Create issue in project repository

---

*Last Updated: 2025-01-27*
*Version: 2.1.0* 