import { useState, useEffect } from 'react';
import Head from 'next/head';

interface ServiceStatus {
  name: string;
  status: 'healthy' | 'unhealthy' | 'starting' | 'unknown';
  url: string;
  port: number;
  description: string;
  lastCheck: string;
}

export default function HealthDashboard() {
  const [services, setServices] = useState<ServiceStatus[]>([
    {
      name: 'API Server',
      status: 'unknown',
      url: 'http://localhost:8000',
      port: 8000,
      description: 'FastAPI backend server',
      lastCheck: 'Never'
    },
    {
      name: 'Web Dashboard',
      status: 'unknown',
      url: 'http://localhost:3000',
      port: 3000,
      description: 'Next.js frontend dashboard',
      lastCheck: 'Never'
    },
    {
      name: 'PostgreSQL',
      status: 'unknown',
      url: 'http://localhost:5432',
      port: 5432,
      description: 'Primary database',
      lastCheck: 'Never'
    },
    {
      name: 'Redis',
      status: 'unknown',
      url: 'http://localhost:6379',
      port: 6379,
      description: 'Cache and session store',
      lastCheck: 'Never'
    },
    {
      name: 'Elasticsearch',
      status: 'unknown',
      url: 'http://localhost:9200',
      port: 9200,
      description: 'Search engine',
      lastCheck: 'Never'
    },
    {
      name: 'Neo4j',
      status: 'unknown',
      url: 'http://localhost:7474',
      port: 7474,
      description: 'Graph database',
      lastCheck: 'Never'
    },
    {
      name: 'Weaviate',
      status: 'unknown',
      url: 'http://localhost:8080',
      port: 8080,
      description: 'Vector database',
      lastCheck: 'Never'
    },
    {
      name: 'MinIO',
      status: 'unknown',
      url: 'http://localhost:9001',
      port: 9001,
      description: 'Object storage',
      lastCheck: 'Never'
    },
    {
      name: 'Prometheus',
      status: 'unknown',
      url: 'http://localhost:9090',
      port: 9090,
      description: 'Metrics monitoring',
      lastCheck: 'Never'
    },
    {
      name: 'Grafana',
      status: 'unknown',
      url: 'http://localhost:3001',
      port: 3001,
      description: 'Monitoring dashboard',
      lastCheck: 'Never'
    }
  ]);

  const [selectedService, setSelectedService] = useState<string | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const checkServiceHealth = async (service: ServiceStatus): Promise<ServiceStatus> => {
    try {
      const startTime = Date.now();
      const response = await fetch(`${service.url}/health`, {
        method: 'GET',
        timeout: 5000
      });
      const endTime = Date.now();
      
      return {
        ...service,
        status: response.ok ? 'healthy' : 'unhealthy',
        lastCheck: new Date().toLocaleTimeString()
      };
    } catch (error) {
      return {
        ...service,
        status: 'unhealthy',
        lastCheck: new Date().toLocaleTimeString()
      };
    }
  };

  const refreshAllServices = async () => {
    setIsRefreshing(true);
    const updatedServices = await Promise.all(
      services.map(service => checkServiceHealth(service))
    );
    setServices(updatedServices);
    setIsRefreshing(false);
  };

  useEffect(() => {
    refreshAllServices();
    const interval = setInterval(refreshAllServices, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'bg-green-500';
      case 'unhealthy': return 'bg-red-500';
      case 'starting': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'healthy': return 'Healthy';
      case 'unhealthy': return 'Unhealthy';
      case 'starting': return 'Starting';
      default: return 'Unknown';
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>AI-Q Health Dashboard</title>
        <meta name="description" content="AI-Q Unified Container Health Dashboard" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">AI-Q Health Dashboard</h1>
              <p className="text-gray-600 mt-2">Unified Container System Status</p>
            </div>
            <button
              onClick={refreshAllServices}
              disabled={isRefreshing}
              className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg flex items-center space-x-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span>{isRefreshing ? 'Refreshing...' : 'Refresh Status'}</span>
            </button>
          </div>
        </div>

        {/* Service Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
          {services.map((service, index) => (
            <div
              key={index}
              className="bg-white rounded-lg shadow-md p-6 cursor-pointer hover:shadow-lg transition-shadow"
              onClick={() => setSelectedService(service.name)}
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">{service.name}</h3>
                <div className={`w-3 h-3 rounded-full ${getStatusColor(service.status)}`}></div>
              </div>
              <p className="text-sm text-gray-600 mb-2">{service.description}</p>
              <div className="text-xs text-gray-500">
                <p>Port: {service.port}</p>
                <p>Last Check: {service.lastCheck}</p>
                <p>Status: {getStatusText(service.status)}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Service Detail Modal */}
        {selectedService && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl h-3/4 flex flex-col">
              <div className="flex justify-between items-center p-6 border-b">
                <h2 className="text-2xl font-bold text-gray-900">
                  {selectedService} - Service Details
                </h2>
                <button
                  onClick={() => setSelectedService(null)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <div className="flex-1 p-6">
                <iframe
                  src={services.find(s => s.name === selectedService)?.url}
                  className="w-full h-full border-0 rounded"
                  title={`${selectedService} Interface`}
                />
              </div>
            </div>
          </div>
        )}

        {/* Quick Access Links */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Access Links</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {services.map((service, index) => (
              <a
                key={index}
                href={service.url}
                target="_blank"
                rel="noopener noreferrer"
                className="block p-3 bg-gray-50 hover:bg-gray-100 rounded-lg text-center transition-colors"
              >
                <div className="text-sm font-medium text-gray-900">{service.name}</div>
                <div className="text-xs text-gray-500">{service.port}</div>
              </a>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
} 