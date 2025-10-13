// Frontend Performance Monitor
// Add this to your main layout or app.vue to monitor performance

export const usePerformanceMonitor = () => {
  const startTime = ref<number>(0)
  const measurements = ref<Record<string, number>>({})
  
  const startMeasure = (name: string) => {
    measurements.value[name] = performance.now()
  }
  
  const endMeasure = (name: string) => {
    const start = measurements.value[name]
    if (start) {
      const duration = performance.now() - start
      console.log(`⏱️ ${name}: ${duration.toFixed(1)}ms`)
      delete measurements.value[name]
      return duration
    }
    return 0
  }
  
  const measureStorage = () => {
    // Test localStorage performance
    const iterations = 100
    const testData = JSON.stringify({ test: 'data', timestamp: Date.now() })
    
    const writeStart = performance.now()
    for (let i = 0; i < iterations; i++) {
      localStorage.setItem(`perf_test_${i}`, testData)
    }
    const writeTime = performance.now() - writeStart
    
    const readStart = performance.now()
    for (let i = 0; i < iterations; i++) {
      localStorage.getItem(`perf_test_${i}`)
    }
    const readTime = performance.now() - readStart
    
    // Cleanup
    for (let i = 0; i < iterations; i++) {
      localStorage.removeItem(`perf_test_${i}`)
    }
    
    console.log('📊 Storage Performance:')
    console.log(`  Write: ${writeTime.toFixed(1)}ms (${(writeTime/iterations).toFixed(2)}ms each)`)
    console.log(`  Read: ${readTime.toFixed(1)}ms (${(readTime/iterations).toFixed(2)}ms each)`)
    
    if (writeTime > 50) console.warn('⚠️ localStorage writes are slow!')
    if (readTime > 50) console.warn('⚠️ localStorage reads are slow!')
  }
  
  const measureNetworkLatency = async () => {
    const start = performance.now()
    try {
      const response = await fetch('/api/ping', { method: 'HEAD' })
      const latency = performance.now() - start
      console.log(`🌐 Network latency: ${latency.toFixed(1)}ms`)
      return latency
    } catch (error) {
      console.warn('❌ Network test failed:', error)
      return -1
    }
  }
  
  return {
    startMeasure,
    endMeasure,
    measureStorage,
    measureNetworkLatency
  }
}