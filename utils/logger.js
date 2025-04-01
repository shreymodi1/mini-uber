/**
 * Utility module for logging debug, info, and error messages.
 * Includes helper functions to format messages consistently.
 */

/**
 * Returns a timestamp string in YYYY-MM-DD HH:mm:ss format.
 * @returns {string} Formatted timestamp
 */
function getTimestamp() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

/**
 * Logs a debug-level message.
 * @param {string} message - The message to log
 */
export function logDebug(message) {
  try {
    console.debug(`[DEBUG] [${getTimestamp()}] ${message}`);
  } catch (error) {
    console.error('[ERROR] Failed to log debug message:', error);
  }
  // TODO: Integrate with external logging service if needed
}

/**
 * Logs an info-level message.
 * @param {string} message - The message to log
 */
export function logInfo(message) {
  try {
    console.info(`[INFO] [${getTimestamp()}] ${message}`);
  } catch (error) {
    console.error('[ERROR] Failed to log info message:', error);
  }
  // TODO: Integrate with external logging service if needed
}

/**
 * Logs an error-level message.
 * @param {string} message - The message to log
 */
export function logError(message) {
  try {
    console.error(`[ERROR] [${getTimestamp()}] ${message}`);
  } catch (error) {
    console.error('[ERROR] Failed to log error message:', error);
  }
  // TODO: Integrate with external logging service if needed
}