"""
General API Stress Testing Tool
===============================

How to run:
    python main.py
    
Follow the interactive prompts to configure your test, or use command line arguments:
    
    python main.py --url "https://api.example.com/endpoint" --method GET --requests 50 --timeout 30
    
Available arguments:
    --url: API endpoint URL
    --method: HTTP method (GET, POST, PUT, DELETE, etc.)
    --requests: Number of concurrent requests (default: 10)
    --timeout: Request timeout in seconds (default: 30)
    --headers: Headers in JSON format (optional)
    --data: Request body data in JSON format (optional)
    --config: Path to JSON config file (optional)
"""

import asyncio
import aiohttp
import argparse
import time
import json
import os
from datetime import datetime
from typing import List

class APIStressTester:
    def __init__(self):
        self.results = []
        self.url = ""
        self.method = "GET"
        self.headers = {}
        self.data = None
        self.num_requests = 10
        self.timeout = 30
        
    def load_config_file(self, config_path: str):
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.url = config.get('url', '')
                self.method = config.get('method', 'GET').upper()
                self.headers = config.get('headers', {})
                self.data = config.get('data', None)
                self.num_requests = config.get('requests', 10)
                self.timeout = config.get('timeout', 30)
                print(f"✅ Configuration loaded from {config_path}")
        except Exception as e:
            print(f"❌ Error loading config file: {e}")
            return False
        return True
    
    def interactive_setup(self):
        """Interactive setup for users not familiar with command line."""
        print("\n🚀 API Stress Test Tool")
        print("=" * 50)
        
        # Get URL
        self.url = input("Enter API URL (e.g., https://api.example.com/users): ").strip()
        if not self.url:
            print("❌ URL is required!")
            return False
            
        # Get HTTP method
        method_input = input("Enter HTTP method [GET]: ").strip().upper()
        self.method = method_input if method_input else "GET"
        
        # Get number of requests
        try:
            requests_input = input("Number of concurrent requests [10]: ").strip()
            self.num_requests = int(requests_input) if requests_input else 10
        except ValueError:
            print("⚠️  Invalid number, using default (10)")
            self.num_requests = 10
            
        # Get timeout
        try:
            timeout_input = input("Request timeout in seconds [30]: ").strip()
            self.timeout = int(timeout_input) if timeout_input else 30
        except ValueError:
            print("⚠️  Invalid timeout, using default (30)")
            self.timeout = 30
            
        # Get headers
        headers_input = input("Headers in JSON format (optional, press Enter to skip): ").strip()
        if headers_input:
            try:
                self.headers = json.loads(headers_input)
            except json.JSONDecodeError:
                print("⚠️  Invalid JSON format for headers, skipping...")
                
        # Get request body data
        if self.method in ['POST', 'PUT', 'PATCH']:
            data_input = input("Request body data in JSON format (optional, press Enter to skip): ").strip()
            if data_input:
                try:
                    self.data = json.loads(data_input)
                except json.JSONDecodeError:
                    print("⚠️  Invalid JSON format for data, skipping...")
                    
        return True
    
    def parse_arguments(self):
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(
            description='General API Stress Testing Tool',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python main.py --url "https://jsonplaceholder.typicode.com/posts" --requests 20
  python main.py --config my_test_config.json
  python main.py --url "https://api.example.com/users" --method POST --data '{"name":"John"}'
            """
        )
        
        parser.add_argument('--url', type=str, help='API endpoint URL')
        parser.add_argument('--method', type=str, default='GET', help='HTTP method (default: GET)')
        parser.add_argument('--requests', type=int, default=10, help='Number of concurrent requests (default: 10)')
        parser.add_argument('--timeout', type=int, default=30, help='Request timeout in seconds (default: 30)')
        parser.add_argument('--headers', type=str, help='Headers in JSON format')
        parser.add_argument('--data', type=str, help='Request body data in JSON format')
        parser.add_argument('--config', type=str, help='Path to JSON configuration file')
        
        return parser.parse_args()
    
    def setup_from_args(self, args):
        """Setup configuration from command line arguments."""
        if args.config:
            if not self.load_config_file(args.config):
                return False
                
        if args.url:
            self.url = args.url
        if args.method:
            self.method = args.method.upper()
        if args.requests:
            self.num_requests = args.requests
        if args.timeout:
            self.timeout = args.timeout
            
        if args.headers:
            try:
                self.headers = json.loads(args.headers)
            except json.JSONDecodeError:
                print("❌ Invalid JSON format for headers")
                return False
                
        if args.data:
            try:
                self.data = json.loads(args.data)
            except json.JSONDecodeError:
                print("❌ Invalid JSON format for data")
                return False
                
        if not self.url:
            print("❌ URL is required! Use --url or run interactively.")
            return False
            
        return True
    
    def calculate_percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile of a list of numbers."""
        if not data:
            return 0
        data_sorted = sorted(data)
        k = (len(data_sorted) - 1) * (percentile / 100.0)
        f = int(k)
        c = k - f
        if f == len(data_sorted) - 1:
            return data_sorted[f]
        return data_sorted[f] * (1 - c) + data_sorted[f + 1] * c
    
    async def make_request(self, session: aiohttp.ClientSession, request_num: int):
        """Make a single async HTTP request."""
        start_time = time.time()
        
        try:
            # Prepare request parameters
            request_kwargs = {
                'url': self.url,
                'headers': self.headers if self.headers else None
            }
            
            if self.data and self.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                request_kwargs['json'] = self.data
            
            print(f"📤 Request {request_num}: {self.method} {self.url}")
            
            # Make the request
            async with session.request(self.method, **request_kwargs) as response:
                end_time = time.time()
                duration = end_time - start_time
                
                # Get response data
                try:
                    if response.content_type == 'application/json':
                        response_data = await response.json()
                    else:
                        response_data = await response.text()
                except:
                    response_data = f"Response size: {response.headers.get('content-length', 'unknown')} bytes"
                
                success = 200 <= response.status < 300
                status_emoji = "✅" if success else "❌"
                
                print(f"{status_emoji} Request {request_num}: {response.status} ({duration:.2f}s)")
                
                self.results.append({
                    "request_num": request_num,
                    "status_code": response.status,
                    "duration_s": duration,
                    "success": success,
                    "response_size": len(str(response_data)) if response_data else 0,
                    "error": None
                })
                
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"❌ Request {request_num}: Error - {str(e)}")
            
            self.results.append({
                "request_num": request_num,
                "status_code": None,
                "duration_s": duration,
                "success": False,
                "response_size": 0,
                "error": str(e)
            })
    
    async def run_test(self):
        """Run the stress test."""
        print(f"\n🎯 Starting stress test...")
        print(f"   URL: {self.url}")
        print(f"   Method: {self.method}")
        print(f"   Concurrent requests: {self.num_requests}")
        print(f"   Timeout: {self.timeout}s")
        print("=" * 60)
        
        overall_start_time = time.time()
        
        # Configure HTTP client
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        connector = aiohttp.TCPConnector(
            limit=self.num_requests + 10,
            limit_per_host=self.num_requests + 10,
        )
        
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            # Create and run all requests concurrently
            tasks = [self.make_request(session, i + 1) for i in range(self.num_requests)]
            await asyncio.gather(*tasks)
        
        overall_end_time = time.time()
        total_duration = overall_end_time - overall_start_time
        
        # Analyze and display results
        self.analyze_results(total_duration)
        
        # Save results
        self.save_results(total_duration)
    
    def analyze_results(self, total_duration: float):
        """Analyze and display test results."""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS")
        print("=" * 60)
        
        success_count = sum(1 for r in self.results if r['success'])
        failure_count = self.num_requests - success_count
        
        successful_durations = [r['duration_s'] for r in self.results if r['success']]
        all_durations = [r['duration_s'] for r in self.results]
        
        # Basic stats
        print(f"⏱️  Total test duration: {total_duration:.2f} seconds")
        print(f"✅ Successful requests: {success_count}/{self.num_requests} ({success_count/self.num_requests*100:.1f}%)")
        print(f"❌ Failed requests: {failure_count}")
        
        if successful_durations:
            avg_duration = sum(successful_durations) / len(successful_durations)
            print(f"📈 Average response time: {avg_duration:.2f} seconds")
            print(f"🚀 Requests per second: {success_count/total_duration:.2f}")
            
            # Response time percentiles
            p50 = self.calculate_percentile(successful_durations, 50)
            p95 = self.calculate_percentile(successful_durations, 95)
            p99 = self.calculate_percentile(successful_durations, 99)
            
            print(f"\n📊 Response Time Percentiles:")
            print(f"   P50 (median): {p50:.2f}s")
            print(f"   P95: {p95:.2f}s") 
            print(f"   P99: {p99:.2f}s")
        
        # Status code breakdown
        status_codes = {}
        for result in self.results:
            status = result['status_code'] or 'Error'
            status_codes[status] = status_codes.get(status, 0) + 1
        
        print(f"\n📋 Status Code Breakdown:")
        for status, count in sorted(status_codes.items()):
            print(f"   {status}: {count}")
        
        # Show some failures if any
        failures = [r for r in self.results if not r['success']]
        if failures:
            print(f"\n⚠️  Sample Errors (showing first 3):")
            for i, failure in enumerate(failures[:3]):
                print(f"   {i+1}. Request {failure['request_num']}: {failure.get('error', 'HTTP error')}")
    
    def save_results(self, total_duration: float):
        """Save detailed results to a file."""
        os.makedirs("stress_test_results", exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"stress_test_results/test_{timestamp}.txt"
        
        with open(filename, "w") as f:
            f.write(f"API Stress Test Results\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Configuration:\n")
            f.write(f"  URL: {self.url}\n")
            f.write(f"  Method: {self.method}\n")
            f.write(f"  Concurrent Requests: {self.num_requests}\n")
            f.write(f"  Timeout: {self.timeout}s\n")
            f.write(f"  Headers: {json.dumps(self.headers, indent=2) if self.headers else 'None'}\n")
            f.write(f"  Data: {json.dumps(self.data, indent=2) if self.data else 'None'}\n\n")
            
            f.write(f"Test Duration: {total_duration:.2f} seconds\n\n")
            
            f.write("Detailed Results:\n")
            f.write("-" * 30 + "\n")
            
            for result in self.results:
                f.write(f"Request {result['request_num']:2d}: "
                       f"Status={result.get('status_code', 'ERR'):3s}, "
                       f"Duration={result['duration_s']:6.2f}s, "
                       f"Success={result['success']}\n")
                
                if result.get('error'):
                    f.write(f"              Error: {result['error']}\n")
        
        print(f"\n💾 Detailed results saved to: {filename}")

def main():
    """Main function."""
    tester = APIStressTester()
    args = tester.parse_arguments()
    
    # Setup configuration
    if any(vars(args).values()):  # If any command line arguments provided
        if not tester.setup_from_args(args):
            return
    else:
        if not tester.interactive_setup():
            return
    
    # Run the test
    try:
        asyncio.run(tester.run_test())
        print("\n🎉 Test completed successfully!")
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")

if __name__ == "__main__":
    main()