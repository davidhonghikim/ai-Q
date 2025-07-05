'use client';

import { useState, useEffect } from 'react';
import { Search, BookOpen, Brain, Database, Settings, BarChart3 } from 'lucide-react';

export default function HomePage() {
  const [systemStatus, setSystemStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkSystemStatus = async () => {
      try {
        const response = await fetch('/api/health');
        const data = await response.json();
        setSystemStatus(data);
      } catch (error) {
        console.error('Failed to fetch system status:', error);
      } finally {
        setLoading(false);
      }
    };

    checkSystemStatus();
  }, []);

  const navigationItems = [
    { name: 'Knowledge Base', icon: BookOpen, href: '/knowledge' },
    { name: 'RAG Search', icon: Search, href: '/rag' },
    { name: 'AI Models', icon: Brain, href: '/ai' },
    { name: 'Data Sources', icon: Database, href: '/data' },
    { name: 'Analytics', icon: BarChart3, href: '/analytics' },
    { name: 'Settings', icon: Settings, href: '/settings' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-2xl font-bold text-gray-900">AI-Q</h1>
              </div>
              <div className="ml-4">
                <p className="text-sm text-gray-500">Knowledge Library System</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              {systemStatus && (
                <div className="flex items-center space-x-2">
                  <div className={`w-2 h-2 rounded-full ${systemStatus.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'}`} />
                  <span className="text-sm text-gray-600">
                    {systemStatus.status === 'healthy' ? 'System Online' : 'System Offline'}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
          </div>
        ) : (
          <div className="px-4 py-6 sm:px-0">
            {/* Welcome Section */}
            <div className="mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                Welcome to AI-Q Knowledge Library
              </h2>
              <p className="text-lg text-gray-600">
                Manage your knowledge with dual-representation storage and AI-powered search capabilities.
              </p>
            </div>

            {/* Navigation Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {navigationItems.map((item) => (
                <div
                  key={item.name}
                  className="card hover:shadow-md transition-shadow duration-200 cursor-pointer"
                >
                  <div className="flex items-center space-x-4">
                    <div className="flex-shrink-0">
                      <item.icon className="h-8 w-8 text-primary-600" />
                    </div>
                    <div>
                      <h3 className="text-lg font-medium text-gray-900">{item.name}</h3>
                      <p className="text-sm text-gray-500">Access {item.name.toLowerCase()}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* System Status */}
            {systemStatus && (
              <div className="card">
                <h3 className="text-lg font-medium text-gray-900 mb-4">System Status</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-primary-600">{systemStatus.agent || 'AI-Q'}</div>
                    <div className="text-sm text-gray-500">Agent</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-900">{systemStatus.version || '1.0.0'}</div>
                    <div className="text-sm text-gray-500">Version</div>
                  </div>
                  <div className="text-center">
                    <div className={`text-2xl font-bold ${systemStatus.status === 'healthy' ? 'text-green-600' : 'text-red-600'}`}>
                      {systemStatus.status === 'healthy' ? 'Online' : 'Offline'}
                    </div>
                    <div className="text-sm text-gray-500">Status</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
} 