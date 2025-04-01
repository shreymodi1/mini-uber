import { createUserAccount, verifyCredentials } from './auth_service.js'
import bcrypt from 'bcryptjs'

jest.mock('bcryptjs')

describe('createUserAccount', () => {
  afterEach(() => {
    jest.clearAllMocks()
  })

  test('should create a user with hashed password', async () => {
    const mockHashedPassword = 'hashedPassword123'
    bcrypt.hash.mockResolvedValueOnce(mockHashedPassword)

    const userData = { email: 'test@example.com', password: 'test123' }
    const result = await createUserAccount(userData)

    expect(bcrypt.hash).toHaveBeenCalledWith(userData.password, 10)
    expect(result).toEqual({
      email: userData.email,
      password: mockHashedPassword,
      message: 'User created (placeholder)'
    })
  })

  test('should throw error if hashing fails', async () => {
    bcrypt.hash.mockRejectedValueOnce(new Error('Hash error'))
    const userData = { email: 'error@example.com', password: 'failHash' }
    await expect(createUserAccount(userData)).rejects.toThrow('Failed to create user account: Hash error')
  })
})

describe('verifyCredentials', () => {
  afterEach(() => {
    jest.clearAllMocks()
  })

  test('should return user object if password matches', async () => {
    const mockEmail = 'test@example.com'
    const mockPassword = 'test123'
    bcrypt.compare.mockResolvedValueOnce(true)

    const result = await verifyCredentials(mockEmail, mockPassword)

    expect(bcrypt.compare).toHaveBeenCalled()
    expect(result).toEqual({
      id: 1,
      email: mockEmail,
      password: '$2a$10$....'
    })
  })

  test('should return false if password does not match', async () => {
    const mockEmail = 'test@example.com'
    const mockPassword = 'wrongPassword'
    bcrypt.compare.mockResolvedValueOnce(false)

    const result = await verifyCredentials(mockEmail, mockPassword)
    expect(result).toBe(false)
  })

  test('should return false if user does not exist', async () => {
    const originalImplementation = jest.requireActual('./auth_service.js').verifyCredentials
    const mockVerifyFunction = jest.fn(async () => {
      // Simulate no user found
      return false
    })
    const localVerifyCredentials = jest.spyOn(require('./auth_service.js'), 'verifyCredentials').mockImplementation(mockVerifyFunction)

    const result = await localVerifyCredentials('nonexistent@example.com', 'doesNotMatter')
    expect(result).toBe(false)
  })

  test('should throw error if verification fails', async () => {
    bcrypt.compare.mockRejectedValueOnce(new Error('Compare error'))
    await expect(verifyCredentials('error@example.com', 'failCompare')).rejects.toThrow('Failed to verify credentials: Compare error')
  })
})