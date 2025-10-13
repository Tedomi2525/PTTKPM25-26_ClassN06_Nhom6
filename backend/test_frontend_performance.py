"""
Script to test frontend performance by analyzing network and localStorage operations
"""

# Create a performance test for the frontend login flow
content = """
// Performance test script for frontend login
console.log('🔄 Starting frontend login performance test...');

// Measure localStorage operations
function testLocalStoragePerformance() {
    console.log('📊 Testing localStorage performance...');
    
    const iterations = 1000;
    const testData = JSON.stringify({
        user_id: 'test123',
        fullName: 'Test User',
        role: 'student',
        schoolId: 'SV25000002',
        avatar: 'test.jpg',
        domain: 'test.com',
        programId: 1
    });
    
    // Test write performance
    const writeStart = performance.now();
    for (let i = 0; i < iterations; i++) {
        localStorage.setItem(`test_${i}`, testData);
    }
    const writeEnd = performance.now();
    const writeTime = writeEnd - writeStart;
    
    // Test read performance
    const readStart = performance.now();
    for (let i = 0; i < iterations; i++) {
        localStorage.getItem(`test_${i}`);
    }
    const readEnd = performance.now();
    const readTime = readEnd - readStart;
    
    // Cleanup
    for (let i = 0; i < iterations; i++) {
        localStorage.removeItem(`test_${i}`);
    }
    
    console.log(`📝 localStorage Write: ${writeTime.toFixed(2)}ms (${(writeTime/iterations).toFixed(3)}ms per item)`);
    console.log(`📖 localStorage Read: ${readTime.toFixed(2)}ms (${(readTime/iterations).toFixed(3)}ms per item)`);
    
    if (writeTime > 100) {
        console.log('⚠️ localStorage write operations are slow!');
    }
    if (readTime > 100) {
        console.log('⚠️ localStorage read operations are slow!');
    }
}

// Test cookie operations
function testCookiePerformance() {
    console.log('📊 Testing cookie performance...');
    
    const testValue = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJTVjI1MDAwMDAyIiwiZXhwIjoxNzYwMzE2OTQ1fQ.test';
    
    const iterations = 100;
    
    // Test cookie write
    const writeStart = performance.now();
    for (let i = 0; i < iterations; i++) {
        document.cookie = `test_token_${i}=${testValue}; path=/; max-age=3600`;
    }
    const writeEnd = performance.now();
    
    // Test cookie read
    const readStart = performance.now();
    for (let i = 0; i < iterations; i++) {
        const value = document.cookie.split('; ').find(row => row.startsWith(`test_token_${i}=`));
    }
    const readEnd = performance.now();
    
    // Cleanup cookies
    for (let i = 0; i < iterations; i++) {
        document.cookie = `test_token_${i}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`;
    }
    
    const writeTime = writeEnd - writeStart;
    const readTime = readEnd - readStart;
    
    console.log(`🍪 Cookie Write: ${writeTime.toFixed(2)}ms (${(writeTime/iterations).toFixed(3)}ms per item)`);
    console.log(`🍪 Cookie Read: ${readTime.toFixed(2)}ms (${(readTime/iterations).toFixed(3)}ms per item)`);
}

// Test network delay simulation
function testNetworkDelay() {
    console.log('📊 Testing network simulation...');
    
    const delays = [0, 50, 100, 200, 500];
    
    delays.forEach(delay => {
        const start = performance.now();
        
        setTimeout(() => {
            const actual = performance.now() - start;
            console.log(`⏱️ Expected delay: ${delay}ms, Actual: ${actual.toFixed(1)}ms`);
        }, delay);
    });
}

// Run all tests
testLocalStoragePerformance();
testCookiePerformance();
testNetworkDelay();

console.log('✅ Performance tests completed. Check console for results.');
"""

print("Frontend Performance Test Script Created")
print("Copy and paste this into browser console to test:")
print("=" * 60)
print(content)