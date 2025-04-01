import { loadDemoConfig } from './demo_config';

describe('loadDemoConfig', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    jest.resetModules();
    process.env = { ...originalEnv };
  });

  afterAll(() => {
    process.env = originalEnv;
  });

  test('should return default placeholders if environment variables are not set', () => {
    delete process.env.DEMO_API_KEY;
    delete process.env.NODE_ENV;
    const config = loadDemoConfig();
    expect(config.apiKey).toBe('YOUR_DEMO_API_KEY_PLACEHOLDER');
    expect(config.environment).toBe('development');
  });

  test('should return environment variables if they are set', () => {
    process.env.DEMO_API_KEY = 'TEST_API_KEY';
    process.env.NODE_ENV = 'production';
    const config = loadDemoConfig();
    expect(config.apiKey).toBe('TEST_API_KEY');
    expect(config.environment).toBe('production');
  });

  test('should log error and rethrow if something goes wrong', () => {
    jest.spyOn(console, 'error').mockImplementation(() => {});
    process.env = undefined;
    expect(() => loadDemoConfig()).toThrowError();
    expect(console.error).toHaveBeenCalledWith(
      expect.stringContaining('Failed to load demo configuration:')
    );
  });
});