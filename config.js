import dotenv from 'dotenv';
dotenv.config();

/**
 * Default configuration object
 */
const defaultConfig = {
  dbUser: 'defaultUser',
  dbPassword: 'defaultPassword',
  apiKey: 'defaultApiKey',
  // TODO: Add other default configurations here
};

/**
 * Reads environment variables and merges them with defaults
 * @returns {Object} The loaded configuration object
 */
export function loadConfig() {
  try {
    const config = {
      ...defaultConfig,
      dbUser: process.env.DB_USER || defaultConfig.dbUser,
      dbPassword: process.env.DB_PASSWORD || defaultConfig.dbPassword,
      apiKey: process.env.API_KEY || defaultConfig.apiKey,
      // TODO: Merge other environment variables as needed
    };

    return config;
  } catch (error) {
    console.error('Failed to load config:', error);
    throw new Error('Configuration load failed');
  }
}