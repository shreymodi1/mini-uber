import express from 'express';
import http from 'http';
import { Server as SocketServer } from 'socket.io';

/**
 * Configures the Express server, attaches routes, and sets up Socket.IO events
 * @returns {Object} The HTTP server instance
 */
export function createServer() {
  try {
    const app = express();
    const server = http.createServer(app);
    const io = new SocketServer(server);

    // TODO: Add any necessary Express middleware here, such as bodyParser or morgan

    // TODO: Attach application routes
    // Example: app.use('/api', apiRoutes);

    // TODO: Attach Socket.IO event handlers
    io.on('connection', (socket) => {
      // Example: console.log('New client connected');
      socket.on('disconnect', () => {
        // Example: console.log('Client disconnected');
      });
    });

    // Basic error handling for Express
    app.use((err, req, res, next) => {
      console.error('Express error:', err);
      res.status(500).json({ error: 'Internal Server Error' });
    });

    return server;
  } catch (error) {
    console.error('Error creating server:', error);
    throw error;
  }
}

/**
 * Binds the server to a specified port and begins listening
 * @param {Object} server - The HTTP server instance
 * @param {number} port - The port number to listen on
 * @returns {Promise<void>} A promise that resolves when the server is listening
 */
export async function startServer(server, port) {
  return new Promise((resolve, reject) => {
    try {
      server.listen(port, () => {
        console.log(`Server is running on port ${port}`);
        resolve();
      });

      // Handle potential server errors
      server.on('error', (error) => {
        console.error('Server error:', error);
        reject(error);
      });
    } catch (error) {
      console.error('Error starting server:', error);
      reject(error);
    }
  });
}