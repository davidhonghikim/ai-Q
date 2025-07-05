# Comprehensive System Monitoring - AI-Q Knowledge Library System

## Overview

This enhanced system monitoring solution provides comprehensive hardware monitoring across Windows, Mac, and Linux platforms. It automatically detects and reports all GPUs, CPUs, memory, disks, and network interfaces with detailed metrics.

## Features

### 🖥️ **Multi-GPU Support**
- **Automatic Detection**: Detects all NVIDIA GPUs using NVML and GPUtil
- **AMD GPU Support**: Platform-specific detection for AMD GPUs
- **Integrated Graphics**: Detects Intel/AMD integrated graphics
- **Real-time Metrics**: GPU utilization, memory usage, temperature, power consumption
- **Capability Detection**: Compute, video encode/decode, 3D, overlay, security features

### 🧠 **Enhanced CPU Monitoring**
- **Utilization**: Real-time CPU usage percentage
- **Core Information**: Physical cores, logical cores, threads, sockets
- **Frequency**: Current, min, max frequencies
- **Process Statistics**: Active processes, handles, threads
- **Virtualization**: Detection of virtualization environment
- **Uptime**: System uptime tracking

### 💾 **Detailed Memory Analysis**
- **Virtual Memory**: Total, used, free, available, cached, buffers
- **Swap Memory**: Total, used, free, swap in/out rates
- **Memory Types**: Active, inactive, wired, shared, slab memory
- **Platform-specific**: Windows, Linux, and macOS specific memory metrics

### 💿 **Comprehensive Disk Monitoring**
- **All Disks**: Detects and monitors all disk partitions
- **Usage Metrics**: Total, used, free space and percentages
- **I/O Statistics**: Read/write speeds, transfer rates, response times
- **Disk Types**: SSD, HDD, NVMe detection
- **File Systems**: Support for various file systems

### 🌐 **Network Interface Monitoring**
- **All Interfaces**: WiFi, Ethernet, virtual interfaces
- **Connection Info**: IP addresses, DNS, signal strength (WiFi)
- **I/O Statistics**: Send/receive rates, packet counts
- **Interface Types**: Connection type detection

## API Endpoints

### Legacy Endpoint (Backward Compatible)
```
GET /api/metrics
```
Returns basic system metrics in the original format.

### New Comprehensive Endpoints

#### All Metrics
```
GET /api/metrics/comprehensive
```
Returns complete system information including all GPUs, detailed CPU, memory, disk, and network data.

#### Individual Component Endpoints
```
GET /api/metrics/gpus      # All GPU information
GET /api/metrics/cpu       # Detailed CPU metrics
GET /api/metrics/memory    # Memory information
GET /api/metrics/disks     # All disk information
GET /api/metrics/network   # Network interface data
```

## Data Models

### GPU Information
```json
{
  "id": 0,
  "name": "NVIDIA GeForce GTX 1070",
  "vendor": "NVIDIA",
  "type": "discrete",
  "memory": {
    "total": 8589934592,
    "used": 2147483648,
    "free": 6442450944,
    "percent": 25.0
  },
  "utilization": {
    "gpu": 45.2,
    "memory": 25.0
  },
  "temperature": 65,
  "power": 120.5,
  "driver_version": "471.11",
  "capabilities": {
    "compute": true,
    "video_encode": true,
    "video_decode": true,
    "3d": true,
    "overlay": true,
    "security": true
  }
}
```

### CPU Information
```json
{
  "utilization": 25.6,
  "count": {
    "physical": 8,
    "logical": 16,
    "cores": 8,
    "threads": 16
  },
  "frequency": {
    "current": 3200.0,
    "min": 800.0,
    "max": 4200.0
  },
  "stats": {
    "ctx_switches": 1234567,
    "interrupts": 987654,
    "soft_interrupts": 54321
  },
  "times": {
    "user": 15.2,
    "system": 8.4,
    "idle": 76.4
  },
  "processes": 245,
  "uptime": 86400.5,
  "virtualization": {
    "detected": false,
    "type": null
  }
}
```

## Installation

### Prerequisites
- Python 3.8+
- Windows: WMI support (included with Python)
- Linux: Standard system utilities
- macOS: system_profiler (built-in)

### Dependencies
```bash
pip install -r requirements.txt
```

### Optional Dependencies
- **NVIDIA GPUs**: `pynvml` and `GPUtil` for detailed GPU monitoring
- **Windows**: `wmi` for enhanced Windows-specific monitoring
- **Linux**: Standard system utilities (no additional packages needed)
- **macOS**: Built-in system_profiler (no additional packages needed)

## Usage

### Starting the Server
```bash
cd Q/frontend
python api_server.py
```

The server will start on `http://localhost:8000` with the following features:

1. **Automatic Hardware Detection**: Scans and detects all hardware components
2. **Real-time Monitoring**: Live updates of system metrics
3. **Multi-GPU Support**: Displays all detected GPUs with individual charts
4. **Comprehensive API**: RESTful endpoints for all system data

### Dashboard Features

#### System Health Tab
- **Live Charts**: Real-time scrolling graphs for CPU, memory, disk usage
- **Multi-GPU Display**: Individual charts for each detected GPU
- **Detailed Metrics**: Temperature, power, memory usage per GPU
- **Auto-refresh**: Configurable update intervals (1s to 5min)

#### GPU Performance Section
- **Individual GPU Cards**: Each GPU gets its own performance card
- **Real-time Metrics**: Usage, memory, temperature display
- **Historical Data**: 60-point rolling window for trend analysis
- **Capability Indicators**: Shows supported GPU features

## Platform Support

### Windows
- ✅ NVIDIA GPUs (via NVML/GPUtil)
- ✅ AMD GPUs (via WMI)
- ✅ Intel Integrated Graphics
- ✅ CPU, Memory, Disk monitoring
- ✅ Network interface detection

### Linux
- ✅ NVIDIA GPUs (via NVML/GPUtil)
- ✅ AMD GPUs (via sysfs)
- ✅ Intel Integrated Graphics
- ✅ CPU, Memory, Disk monitoring
- ✅ Network interface detection

### macOS
- ✅ Apple Silicon GPUs
- ✅ Intel Integrated Graphics
- ✅ AMD GPUs (limited)
- ✅ CPU, Memory, Disk monitoring
- ✅ Network interface detection

## Limitations

### GPU Monitoring
- **AMD GPUs on Windows**: Limited to basic info via WMI
- **AMD GPUs on Linux**: Requires ROCm for detailed metrics
- **Apple Silicon**: Limited to basic GPU information
- **Integrated Graphics**: Basic detection and utilization

### Platform-specific Features
- **Windows**: Full WMI integration for detailed hardware info
- **Linux**: sysfs and procfs for comprehensive monitoring
- **macOS**: system_profiler for hardware detection

## Troubleshooting

### GPU Not Detected
1. **NVIDIA GPUs**: Ensure NVIDIA drivers are installed
2. **AMD GPUs**: Check if ROCm is installed (Linux)
3. **Integrated Graphics**: May show as CPU-only on some systems

### Permission Issues
- **Linux**: May need to run with elevated privileges for some metrics
- **Windows**: WMI access may require admin privileges
- **macOS**: system_profiler should work without special permissions

### Performance Impact
- **Monitoring Overhead**: Minimal impact (<1% CPU usage)
- **Memory Usage**: ~50MB for monitoring system
- **Network**: Only local API calls, no external traffic

## Future Enhancements

### Planned Features
- **GPU Process Monitoring**: Show which processes are using each GPU
- **Historical Data Storage**: Persistent metrics storage
- **Alert System**: Configurable thresholds and notifications
- **Power Management**: GPU power state monitoring
- **Fan Speed**: GPU fan speed monitoring (where available)

### Platform Improvements
- **AMD ROCm**: Enhanced AMD GPU support on Linux
- **Apple Metal**: Better Apple Silicon GPU monitoring
- **Virtual Machines**: Enhanced VM detection and monitoring

## Contributing

This system monitoring solution is designed to be extensible. To add support for new hardware or platforms:

1. **Extend SystemMonitor class**: Add new detection methods
2. **Update Pydantic models**: Add new data structures
3. **Enhance API endpoints**: Add new endpoints for new metrics
4. **Update frontend**: Add UI components for new data

## License

This monitoring system is part of the AI-Q Knowledge Library System and follows the same licensing terms as the main project. 