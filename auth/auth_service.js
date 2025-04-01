import bcrypt from 'bcryptjs'
// TODO: Replace with actual DB import/connection
// import db from '../db/connection'

/**
 * Inserts a new user record into DB with a hashed password
 * @param {Object} userData - The user details
 * @param {string} userData.email - The user's email
 * @param {string} userData.password - The user's plaintext password
 * @returns {Promise<Object>} The newly created user record
 * @throws {Error} Throws an error if user creation fails
 */
export async function createUserAccount(userData) {
  try {
    // TODO: Validate userData (e.g., check email format, password strength)

    // Hash the password before storing
    const saltRounds = 10
    const hashedPassword = await bcrypt.hash(userData.password, saltRounds)

    // TODO: Insert user into database
    // Example placeholder:
    // const query = 'INSERT INTO users (email, password) VALUES ($1, $2) RETURNING *'
    // const values = [userData.email, hashedPassword]
    // const result = await db.query(query, values)
    // return result.rows[0]

    return {
      email: userData.email,
      password: hashedPassword,
      message: 'User created (placeholder)'
    }
  } catch (error) {
    // Log error or handle accordingly
    throw new Error(`Failed to create user account: ${error.message}`)
  }
}

/**
 * Checks DB for matching user/pass combo
 * @param {string} email - The user's email
 * @param {string} password - The user's plaintext password
 * @returns {Promise<Object|boolean>} Returns user object or false if credentials are invalid
 * @throws {Error} Throws an error if credential verification fails
 */
export async function verifyCredentials(email, password) {
  try {
    // TODO: Fetch user record by email
    // Example placeholder:
    // const query = 'SELECT * FROM users WHERE email = $1'
    // const values = [email]
    // const result = await db.query(query, values)
    // const user = result.rows[0]

    // Placeholder user object for demonstration
    const user = {
      id: 1,
      email,
      password: '$2a$10$....' // Encrypted password
    }

    if (!user) {
      return false
    }

    // Compare input password with stored hashed password
    const isMatch = await bcrypt.compare(password, user.password)
    return isMatch ? user : false
  } catch (error) {
    // Log error or handle accordingly
    throw new Error(`Failed to verify credentials: ${error.message}`)
  }
}