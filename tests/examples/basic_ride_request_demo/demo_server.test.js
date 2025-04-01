import express from 'express'
import http from 'http'
import { Server } from 'socket.io'
import { initDemoServer, demoRideFlow } from './demo_server'

jest.mock('express', () => {
  const expressMock = jest.fn(() => ({
    use: jest.fn(),
    get: jest.fn()
  }))
  expressMock.json = jest.fn()
  return expressMock
})

jest.mock('http', () => ({
  createServer: jest.fn()
}))

jest.mock('socket.io', () => {
  return {
    Server: jest.fn().mockImplementation(() => ({
      on: jest.fn()
    }))
  }
})

describe('initDemoServer', () => {
  let listenSpy
  let consoleLogSpy
  let consoleErrorSpy
  let processExitSpy

  beforeAll(() => {
    listenSpy = jest.fn()
    consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {})
    consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {})
    processExitSpy = jest.spyOn(process, 'exit').mockImplementation(() => {})
    http.createServer.mockReturnValue({ listen: listenSpy })
  })

  afterAll(() => {
    consoleLogSpy.mockRestore()
    consoleErrorSpy.mockRestore()
    processExitSpy.mockRestore()
  })

  test('should create and start a server on the default port', () => {
    initDemoServer()
    expect(listenSpy).toHaveBeenCalledWith(3000, expect.any(Function))
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Demo server listening on port 3000'))
  })

  test('should create and start a server on a custom port', () => {
    initDemoServer(4000)
    expect(listenSpy).toHaveBeenCalledWith(4000, expect.any(Function))
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Demo server listening on port 4000'))
  })

  test('should handle and log initialization errors', () => {
    const errorMessage = 'Initialization Error'
    http.createServer.mockImplementationOnce(() => {
      throw new Error(errorMessage)
    })

    initDemoServer()
    expect(consoleErrorSpy).toHaveBeenCalledWith('Failed to initialize demo server:', expect.any(Error))
    expect(processExitSpy).toHaveBeenCalledWith(1)
  })
})

describe('demoRideFlow', () => {
  let consoleLogSpy
  let consoleErrorSpy

  beforeEach(() => {
    consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {})
    consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {})
  })

  afterEach(() => {
    consoleLogSpy.mockRestore()
    consoleErrorSpy.mockRestore()
  })

  test('should simulate the ride flow without errors', () => {
    demoRideFlow()
    expect(consoleLogSpy).toHaveBeenNthCalledWith(1, 'Rider Test Rider requests a ride')
    expect(consoleLogSpy).toHaveBeenNthCalledWith(2, 'Driver Test Driver accepts the ride')
    expect(consoleLogSpy).toHaveBeenNthCalledWith(3, 'Ride completed for rider Test Rider')
  })

  test('should handle errors gracefully', () => {
    const errorMessage = 'Demo Ride Flow Error'
    jest.spyOn(console, 'log').mockImplementationOnce(() => {
      throw new Error(errorMessage)
    })

    demoRideFlow()
    expect(consoleErrorSpy).toHaveBeenCalledWith('Error in demoRideFlow:', expect.any(Error))
  })
})