// AI Latency Monitor JavaScript
class LatencyMonitor {
    constructor() {
        this.autoRefreshEnabled = true;
        this.autoRefreshInterval = null;
        this.chart = null;
        this.latencyHistory = {
            openai: [],
            azure: [],
            gemini: [],
            deepseek: []
        };
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.initChart();
        this.loadIPInfo();
        this.loadLatencyData();
        this.startAutoRefresh();
    }
    
    setupEventListeners() {
        // Refresh button
        document.getElementById('refresh-btn').addEventListener('click', () => {
            this.loadLatencyData();
        });
        
        // Toggle auto-refresh
        document.getElementById('toggle-auto-refresh').addEventListener('click', () => {
            this.toggleAutoRefresh();
        });
    }
    
    async loadIPInfo() {
        try {
            const response = await fetch('/api/ip');
            const data = await response.json();
            
            if (data.error) {
                document.getElementById('ip-info').innerHTML = 
                    `<div class="info-item"><span class="info-label">Error:</span><span class="info-value">${data.error}</span></div>`;
                return;
            }
            
            document.getElementById('ip-info').innerHTML = `
                <div class="info-item">
                    <span class="info-label">IP Address:</span>
                    <span class="info-value">${data.ip}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Location:</span>
                    <span class="info-value">${data.city}, ${data.region}, ${data.country}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Coordinates:</span>
                    <span class="info-value">${data.latitude.toFixed(4)}, ${data.longitude.toFixed(4)}</span>
                </div>
            `;
        } catch (error) {
            console.error('Failed to load IP info:', error);
            document.getElementById('ip-info').innerHTML = 
                '<div class="info-item"><span class="info-label">Error:</span><span class="info-value">Failed to load IP information</span></div>';
        }
    }
    
    async loadLatencyData() {
        // Show loading indicators
        this.setLoadingState();
        
        try {
            const response = await fetch('/api/latency');
            const data = await response.json();
            
            // Update each platform
            this.updatePlatform('openai', data.openai);
            this.updatePlatform('azure', data.azure);
            this.updatePlatform('gemini', data.gemini);
            this.updatePlatform('deepseek', data.deepseek);
            
            // Update chart
            this.updateChart();
            
            // Update footer timestamp
            document.getElementById('footer-timestamp').textContent = new Date().toLocaleString();
            document.getElementById('last-update').textContent = 'Last updated: ' + new Date().toLocaleTimeString();
            
        } catch (error) {
            console.error('Failed to load latency data:', error);
            this.setErrorState('Failed to connect to monitoring service');
        }
    }
    
    updatePlatform(platform, data) {
        const card = document.getElementById(`${platform}-card`);
        const latencyElement = document.getElementById(`${platform}-latency`);
        const statusElement = document.getElementById(`${platform}-status`);
        const timestampElement = document.getElementById(`${platform}-timestamp`);
        const errorElement = document.getElementById(`${platform}-error`);
        
        if (!data) {
            // Platform not configured
            latencyElement.textContent = '-';
            latencyElement.className = 'latency-value';
            statusElement.className = 'status-indicator';
            timestampElement.textContent = 'Never';
            errorElement.textContent = 'Not configured';
            return;
        }
        
        if (data.success) {
            // Successful test
            const latency = Math.round(data.response_time_ms);
            latencyElement.textContent = latency;
            latencyElement.className = `latency-value ${this.getLatencyClass(latency)}`;
            statusElement.className = 'status-indicator online';
            timestampElement.textContent = new Date(data.timestamp * 1000).toLocaleTimeString();
            errorElement.textContent = 'Online';
            
            // Add to history
            this.addToHistory(platform, data);
        } else {
            // Failed test
            const latency = Math.round(data.response_time_ms);
            latencyElement.textContent = latency;
            latencyElement.className = 'latency-value slow';
            statusElement.className = 'status-indicator error';
            timestampElement.textContent = new Date(data.timestamp * 1000).toLocaleTimeString();
            errorElement.textContent = data.error_message || 'Connection failed';
        }
    }
    
    getLatencyClass(latency) {
        if (latency < 1000) return 'fast';
        if (latency < 3000) return 'medium';
        return 'slow';
    }
    
    addToHistory(platform, data) {
        const timestamp = new Date(data.timestamp * 1000);
        this.latencyHistory[platform].push({
            time: timestamp,
            value: data.response_time_ms
        });
        
        // Keep only last 20 data points
        if (this.latencyHistory[platform].length > 20) {
            this.latencyHistory[platform].shift();
        }
    }
    
    setLoadingState() {
        const platforms = ['openai', 'azure', 'gemini', 'deepseek'];
        platforms.forEach(platform => {
            const statusElement = document.getElementById(`${platform}-status`);
            statusElement.className = 'status-indicator loading';
        });
    }
    
    setErrorState(message) {
        const platforms = ['openai', 'azure', 'gemini', 'deepseek'];
        platforms.forEach(platform => {
            const errorElement = document.getElementById(`${platform}-error`);
            errorElement.textContent = message;
            const statusElement = document.getElementById(`${platform}-status`);
            statusElement.className = 'status-indicator error';
        });
    }
    
    initChart() {
        const ctx = document.getElementById('latencyChart').getContext('2d');
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'OpenAI',
                        data: [],
                        borderColor: '#4285F4',
                        backgroundColor: 'rgba(66, 133, 244, 0.1)',
                        tension: 0.4
                    },
                    {
                        label: 'Azure OpenAI',
                        data: [],
                        borderColor: '#0078D4',
                        backgroundColor: 'rgba(0, 120, 212, 0.1)',
                        tension: 0.4
                    },
                    {
                        label: 'Google Gemini',
                        data: [],
                        borderColor: '#34A853',
                        backgroundColor: 'rgba(52, 168, 83, 0.1)',
                        tension: 0.4
                    },
                    {
                        label: 'DeepSeek',
                        data: [],
                        borderColor: '#FF6D01',
                        backgroundColor: 'rgba(255, 109, 1, 0.1)',
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Response Time (ms)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'AI Platform Latency Over Time'
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                }
            }
        });
    }
    
    updateChart() {
        // Get the longest history to determine time labels
        let maxLength = 0;
        const platforms = ['openai', 'azure', 'gemini', 'deepseek'];
        
        platforms.forEach(platform => {
            if (this.latencyHistory[platform].length > maxLength) {
                maxLength = this.latencyHistory[platform].length;
            }
        });
        
        if (maxLength === 0) return;
        
        // Create time labels from the platform with most data
        const labels = [];
        let referenceHistory = null;
        for (const platform of platforms) {
            if (this.latencyHistory[platform].length === maxLength) {
                referenceHistory = this.latencyHistory[platform];
                break;
            }
        }
        
        if (referenceHistory) {
            referenceHistory.forEach(point => {
                labels.push(point.time.toLocaleTimeString());
            });
        }
        
        // Update chart data
        this.chart.data.labels = labels;
        
        platforms.forEach((platform, index) => {
            const data = this.latencyHistory[platform].map(point => point.value);
            this.chart.data.datasets[index].data = data;
        });
        
        this.chart.update();
    }
    
    startAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
        }
        
        this.autoRefreshInterval = setInterval(() => {
            if (this.autoRefreshEnabled) {
                this.loadLatencyData();
            }
        }, 10000); // 10 seconds
    }
    
    toggleAutoRefresh() {
        this.autoRefreshEnabled = !this.autoRefreshEnabled;
        const button = document.getElementById('toggle-auto-refresh');
        const statusSpan = document.getElementById('auto-refresh-status');
        
        if (this.autoRefreshEnabled) {
            button.innerHTML = '⏸️ Pause Auto-refresh';
            statusSpan.textContent = 'Auto-refresh: ON';
        } else {
            button.innerHTML = '▶️ Resume Auto-refresh';
            statusSpan.textContent = 'Auto-refresh: OFF';
        }
    }
}

// Initialize the monitor when page loads
document.addEventListener('DOMContentLoaded', () => {
    new LatencyMonitor();
});

// Handle visibility change to pause/resume when tab is not visible
document.addEventListener('visibilitychange', () => {
    // You could implement logic here to pause updates when tab is not visible
    // to save resources
});