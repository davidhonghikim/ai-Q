import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Forward the health check to the main API server
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/health`);
    
    if (response.ok) {
      const data = await response.json();
      return NextResponse.json(data);
    } else {
      return NextResponse.json(
        { status: 'unhealthy', error: 'API server not responding' },
        { status: 503 }
      );
    }
  } catch (error) {
    return NextResponse.json(
      { status: 'unhealthy', error: 'Failed to connect to API server' },
      { status: 503 }
    );
  }
} 