import http from 'http';
import { createServer, startServer } from './server';

describe('server.js', () => {
  describe('createServer()', () => {
    let server;

    afterEach(() => {
      if (server && server.listening) {
        server.close();
      }
      server = undefined;
    });

    test('should create an HTTP server instance without error', () => {
      server = createServer();
      expect(server).toBeInstanceOf(http.Server);
    });

    test('should throw an error if server creation fails', () => {
      jest.spyOn(http, 'createServer').mockImplementationOnce(() => {
        throw new Error('Mock server creation failure');
      });
      expect(() => createServer()).toThrow('Mock server creation failure');
      http.createServer.mockRestore();
    });
  });

  describe('startServer()', () => {
    let server;
    const testPort = 4000;

    beforeEach(() => {
      server = createServer();
    });

    afterEach(async () => {
      if (server && server.listening) {
        await new Promise((resolve) => server.close(resolve));
      }
      server = undefined;
    });

    test('should start the server on the specified port', async () => {
      await expect(startServer(server, testPort)).resolves.toBeUndefined();
      expect(server.listening).toBe(true);
    });

    test('should reject if server fails to start', async () => {
      jest.spyOn(server, 'listen').mockImplementationOnce(() => {
        server.emit('error', new Error('Mock listen error'));
      });
      await expect(startServer(server, testPort)).rejects.toThrow('Mock listen error');
    });
  });
});