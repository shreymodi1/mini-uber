import { loadConfig } from './config';

describe('loadConfig', () => {
  const originalEnv = { ...process.env };
  
  beforeEach(() => {
    jest.resetModules();
    process.env = { ...originalEnv };
  });

  afterAll(() => {
    process.env = originalEnv;
  });

  test('should return default values when no environment variables are set', () => {
    delete process.env.DB_USER;
    delete process.env.DB_PASSWORD;
    delete process.env.API_KEY;

    const config = loadConfig();
    expect(config.dbUser).toBe('defaultUser');
    expect(config.dbPassword).toBe('defaultPassword');
    expect(config.apiKey).toBe('defaultApiKey');
  });

  test('should return values from environment variables if set', () => {
    process.env.DB_USER = 'envUser';
    process.env.DB_PASSWORD = 'envPassword';
    process.env.API_KEY = 'envApiKey';

    const config = loadConfig();
    expect(config.dbUser).toBe('envUser');
    expect(config.dbPassword).toBe('envPassword');
    expect(config.apiKey).toBe('envApiKey');
  });

  test('should throw an error if merging configurations fails', () => {
    jest.spyOn(console, 'error').mockImplementation(() => {});
    jest.spyOn(Object, 'assign').mockImplementation(() => {
      throw new Error('Forced merge error');
    });

    expect(() => loadConfig()).toThrow('Configuration load failed');
    expect(console.error).toHaveBeenCalled();
  });
});