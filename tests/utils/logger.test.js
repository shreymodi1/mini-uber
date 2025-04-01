import { logDebug, logInfo, logError } from '../utils/logger';

describe('Logger Utility', () => {
  describe('logDebug', () => {
    beforeEach(() => {
      jest.spyOn(console, 'debug').mockImplementation(() => {});
    });

    afterEach(() => {
      (console.debug as jest.Mock).mockRestore();
    });

    test('should log debug message with correct format', () => {
      const message = 'test debug message';
      logDebug(message);
      expect(console.debug).toHaveBeenCalledTimes(1);
      expect(console.debug).toHaveBeenCalledWith(expect.stringContaining('[DEBUG] ['));
      expect(console.debug).toHaveBeenCalledWith(expect.stringContaining(message));
    });

    test('should not throw any error if console.debug fails', () => {
      (console.debug as jest.Mock).mockImplementation(() => {
        throw new Error('Console debug failure');
      });
      expect(() => logDebug('test fail debug')).not.toThrow();
    });
  });

  describe('logInfo', () => {
    beforeEach(() => {
      jest.spyOn(console, 'info').mockImplementation(() => {});
    });

    afterEach(() => {
      (console.info as jest.Mock).mockRestore();
    });

    test('should log info message with correct format', () => {
      const message = 'test info message';
      logInfo(message);
      expect(console.info).toHaveBeenCalledTimes(1);
      expect(console.info).toHaveBeenCalledWith(expect.stringContaining('[INFO] ['));
      expect(console.info).toHaveBeenCalledWith(expect.stringContaining(message));
    });

    test('should not throw any error if console.info fails', () => {
      (console.info as jest.Mock).mockImplementation(() => {
        throw new Error('Console info failure');
      });
      expect(() => logInfo('test fail info')).not.toThrow();
    });
  });

  describe('logError', () => {
    beforeEach(() => {
      jest.spyOn(console, 'error').mockImplementation(() => {});
    });

    afterEach(() => {
      (console.error as jest.Mock).mockRestore();
    });

    test('should log error message with correct format', () => {
      const message = 'test error message';
      logError(message);
      expect(console.error).toHaveBeenCalledTimes(1);
      expect(console.error).toHaveBeenCalledWith(expect.stringContaining('[ERROR] ['));
      expect(console.error).toHaveBeenCalledWith(expect.stringContaining(message));
    });

    test('should not throw any error if console.error fails', () => {
      (console.error as jest.Mock).mockImplementation(() => {
        throw new Error('Console error failure');
      });
      expect(() => logError('test fail error')).not.toThrow();
    });
  });
});