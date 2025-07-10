// AI-Q Dashboard Configuration
// Reads environment variables for dynamic host/port configuration

class DashboardConfig {
    constructor() {
        // Default to localhost if not specified
        this.host = this.getEnvVar('DASHBOARD_HOST') || 'localhost';
        this.protocol = this.getEnvVar('DASHBOARD_PROTOCOL') || 'http';
        
        // Service configuration from environment
        this.services = {
            huggingface: {
                host: this.getEnvVar('HUGGINGFACE_HOST') || this.host,
                port: this.getEnvVar('HUGGINGFACE_PORT') || '8082',
                name: 'HuggingFace Inference'
            },
            ollama: {
                host: this.getEnvVar('OLLAMA_HOST') || this.host,
                port: this.getEnvVar('OLLAMA_PORT') || '11434',
                name: 'Ollama LLM'
            },
            openwebui: {
                host: this.getEnvVar('OPENWEBUI_HOST') || this.host,
                port: this.getEnvVar('OPENWEBUI_PORT') || '3003',
                name: 'OpenWebUI Chat Interface'
            },
            weaviate: {
                host: this.getEnvVar('WEAVIATE_HOST') || this.host,
                port: this.getEnvVar('WEAVIATE_PORT') || '8080',
                name: 'Weaviate Vector DB'
            },
            postgres: {
                host: this.getEnvVar('POSTGRES_HOST') || this.host,
                port: this.getEnvVar('POSTGRES_PORT') || '5432',
                name: 'PostgreSQL'
            },
            redis: {
                host: this.getEnvVar('REDIS_HOST') || this.host,
                port: this.getEnvVar('REDIS_PORT') || '6379',
                name: 'Redis Cache'
            },
            neo4j: {
                host: this.getEnvVar('NEO4J_HOST') || this.host,
                port: this.getEnvVar('NEO4J_BROWSER_PORT') || '7474',
                name: 'Neo4j Graph DB'
            },
            elasticsearch: {
                host: this.getEnvVar('ELASTICSEARCH_HOST') || this.host,
                port: this.getEnvVar('ELASTICSEARCH_PORT') || '9200',
                name: 'Elasticsearch'
            },
            minio: {
                host: this.getEnvVar('MINIO_HOST') || this.host,
                apiPort: this.getEnvVar('MINIO_API_PORT') || '9000',
                consolePort: this.getEnvVar('MINIO_CONSOLE_PORT') || '9001',
                name: 'MinIO Storage'
            },
            grafana: {
                host: this.getEnvVar('GRAFANA_HOST') || this.host,
                port: this.getEnvVar('GRAFANA_PORT') || '3001',
                name: 'Grafana'
            },
            prometheus: {
                host: this.getEnvVar('PROMETHEUS_HOST') || this.host,
                port: this.getEnvVar('PROMETHEUS_PORT') || '9090',
                name: 'Prometheus'
            },
            cadvisor: {
                host: this.getEnvVar('CADVISOR_HOST') || this.host,
                port: this.getEnvVar('CADVISOR_PORT') || '8081',
                name: 'cAdvisor'
            },
            gitea: {
                host: this.getEnvVar('GITEA_HOST') || this.host,
                port: this.getEnvVar('GITEA_PORT') || '3002',
                name: 'Gitea Git Server'
            },
            n8n: {
                host: this.getEnvVar('N8N_HOST') || this.host,
                port: this.getEnvVar('N8N_PORT') || '5678',
                name: 'n8n Workflow Automation'
            },
            penpot: {
                host: this.getEnvVar('PENPOT_HOST') || this.host,
                port: this.getEnvVar('PENPOT_PORT') || '9002',
                name: 'Penpot Design Tool'
            },
            nextcloud: {
                host: this.getEnvVar('NEXTCLOUD_HOST') || this.host,
                port: this.getEnvVar('NEXTCLOUD_PORT') || '8083',
                name: 'NextCloud File Storage'
            },
            admin_panel: {
                host: this.getEnvVar('ADMIN_PANEL_HOST') || this.host,
                port: this.getEnvVar('ADMIN_PANEL_PORT') || '9003',
                name: 'Admin Panel'
            },
            registry: {
                host: this.getEnvVar('REGISTRY_HOST') || this.host,
                port: this.getEnvVar('REGISTRY_PORT') || '5000',
                name: 'Docker Registry'
            },
            nginx: {
                host: this.getEnvVar('NGINX_HOST') || this.host,
                port: this.getEnvVar('NGINX_PORT') || '80',
                name: 'Nginx Load Balancer'
            }
        };
    }

    getEnvVar(name) {
        // Read from root .env file
        // In a real environment, this would read from actual env vars
        // For now, returning null to use defaults
        return null;
    }

    getServiceUrl(serviceName, path = '') {
        const service = this.services[serviceName];
        if (!service) return '#';
        
        const port = service.port || service.apiPort;
        return `${this.protocol}://${service.host}:${port}${path}`;
    }

    getMinioConsoleUrl() {
        const service = this.services.minio;
        return `${this.protocol}://${service.host}:${service.consolePort}`;
    }

    async checkServiceHealth(serviceName) {
        try {
            const url = this.getServiceUrl(serviceName, '/health');
            const response = await fetch(url, { 
                method: 'GET',
                mode: 'no-cors' // Handle CORS issues
            });
            return response.ok;
        } catch (error) {
            return false;
        }
    }

    async getAllServiceStatuses() {
        const statuses = {};
        for (const serviceName of Object.keys(this.services)) {
            statuses[serviceName] = await this.checkServiceHealth(serviceName);
        }
        return statuses;
    }
}

// Export for use in dashboard
window.DashboardConfig = DashboardConfig; 