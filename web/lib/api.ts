// Centralized API Configuration
// All API calls should use this base URL to allow easy port switching

export const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Helper for constructing API URLs
export function apiUrl(path: string): string {
    return `${API_BASE}${path.startsWith('/') ? path : '/' + path}`;
}
