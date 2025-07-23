# API Stress Test Tool 🚀

A simple, user-friendly tool to stress test any API endpoint with concurrent requests. Perfect for testing API performance, reliability, and finding bottlenecks.

## ✨ Features

- **Easy to use**: Interactive mode for beginners, command-line for advanced users
- **Any HTTP method**: GET, POST, PUT, DELETE, PATCH, etc.
- **Concurrent requests**: Test with multiple simultaneous requests
- **Detailed analytics**: Response times, percentiles, success rates
- **Flexible configuration**: Command-line args, config files, or interactive setup
- **Beautiful output**: Clear, emoji-enhanced results

## 🛠️ Installation

1. **Install Python** (3.7 or higher) from [python.org](https://python.org)

2. **Install required libraries**:
   ```bash
   pip install aiohttp
   ```

3. **Download the script** and save as `main.py`

## 🚀 How to Use

### Option 1: Interactive Mode (Easiest)
Just run the script and follow the prompts:
```bash
python main.py
```

The script will ask you:
- API URL
- HTTP method (GET, POST, etc.)
- Number of concurrent requests
- Timeout duration
- Headers (optional)
- Request body data (optional)

### Option 2: Command Line Arguments
For quick testing:
```bash
python main.py --url "https://api.example.com/users" --requests 50 --timeout 30
```

### Option 3: Configuration File
Create a JSON config file (see example below) and use:
```bash
python main.py --config my_test.json
```

## 📝 Examples

### Testing a GET endpoint:
```bash
python main.py --url "https://jsonplaceholder.typicode.com/posts" --requests 20 --method GET
```

### Testing a POST endpoint with data:
```bash
python main.py --url "https://api.example.com/users" --method POST --data '{"name":"John","email":"john@example.com"}' --requests 10
```

### Using headers (like authentication):
```bash
python main.py --url "https://api.example.com/protected" --headers '{"Authorization":"Bearer your-token"}' --requests 5
```

## ⚙️ Configuration File Format

Create a `.json` file with your test configuration:

```json
{
  "url": "https://api.example.com/endpoint",
  "method": "POST",
  "requests": 25,
  "timeout": 60,
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer your-token"
  },
  "data": {
    "key": "value"
  }
}
```

**Configuration Options:**
- `url`: Your API endpoint (required)
- `method`: HTTP method - GET, POST, PUT, DELETE, etc. (default: GET)
- `requests`: Number of concurrent requests (default: 10)
- `timeout`: Request timeout in seconds (default: 30)
- `headers`: HTTP headers as key-value pairs (optional)
- `data`: Request body data for POST/PUT requests (optional)

## 📊 Understanding the Results

The tool provides comprehensive results:

```
📊 TEST RESULTS
===============================================
⏱️  Total test duration: 5.23 seconds
✅ Successful requests: 48/50 (96.0%)
❌ Failed requests: 2
📈 Average response time: 0.85 seconds
🚀 Requests per second: 9.18

📊 Response Time Percentiles:
   P50 (median): 0.82s
   P95: 1.24s
   P99: 1.67s

📋 Status Code Breakdown:
   200: 48
   500: 2
```

**What this means:**
- **Total duration**: How long the entire test took
- **Success rate**: Percentage of requests that succeeded (status 200-299)
- **Average response time**: Mean time for successful requests
- **RPS**: Requests per second your API handled
- **Percentiles**: P50 means 50% of requests were faster than this time
- **Status codes**: Breakdown of HTTP response codes

## 🎯 Common Use Cases

### 1. **Load Testing**
Test how many concurrent users your API can handle:
```bash
python main.py --url "https://your-api.com/endpoint" --requests 100
```

### 2. **Performance Benchmarking**
Measure response times under different loads:
```bash
python main.py --url "https://your-api.com/endpoint" --requests 10  # Light load
python main.py --url "https://your-api.com/endpoint" --requests 100 # Heavy load
```

### 3. **Authentication Testing**
Test authenticated endpoints:
```bash
python main.py --url "https://api.example.com/protected" --headers '{"Authorization":"Bearer token123"}' --requests 20
```

### 4. **Different HTTP Methods**
Test POST, PUT, DELETE endpoints:
```bash
python main.py --url "https://api.example.com/users" --method POST --data '{"name":"Test User"}' --requests 15
```

## 📁 Output Files

Results are automatically saved to `stress_test_results/` folder with detailed logs including:
- Configuration used
- Individual request results
- Timing data
- Error details

## ⚠️ Best Practices

1. **Start small**: Begin with 5-10 requests, then increase
2. **Test in staging**: Don't stress test production APIs without permission
3. **Monitor your API**: Watch server logs during tests
4. **Respect rate limits**: Some APIs have rate limiting
5. **Clean up**: If testing POST/PUT, consider cleanup afterward

## 🔧 Troubleshooting

**Problem**: "Module not found: aiohttp"
**Solution**: Install with `pip install aiohttp`

**Problem**: Connection errors
**Solution**: Check URL, internet connection, and API availability

**Problem**: All requests failing
**Solution**: Verify URL, method, headers, and API requirements

**Problem**: Slow responses
**Solution**: Increase timeout or reduce concurrent requests

## 🤝 Need Help?

If you run into issues:
1. Try interactive mode first - it's more forgiving
2. Start with small numbers (5-10 requests)
3. Test a simple GET endpoint first (like `https://jsonplaceholder.typicode.com/posts`)
4. Check that your API endpoint works in a browser or Postman first

Happy testing! 🎉