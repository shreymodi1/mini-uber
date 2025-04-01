import { signupHandler, loginHandler, logoutHandler } from './auth_controller';

describe('signupHandler', () => {
  test('should respond with 201 on successful signup', async () => {
    const req = {
      body: {
        userDetails: { username: 'testUser', password: 'testPass' }
      }
    };
    const res = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };

    await signupHandler(req, res);
    expect(res.status).toHaveBeenCalledWith(201);
    expect(res.json).toHaveBeenCalledWith({ message: 'Signup successful' });
  });

  test('should respond with 500 on internal server error', async () => {
    const req = {};
    const res = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };

    const originalImplementation = signupHandler;
    signupHandler = jest.fn().mockImplementation(async () => {
      throw new Error('Database error');
    });

    await signupHandler(req, res);
    expect(res.status).toHaveBeenCalledWith(500);
    expect(res.json).toHaveBeenCalledWith({ error: 'Internal server error' });

    signupHandler = originalImplementation;
  });
});

describe('loginHandler', () => {
  test('should respond with 200 on successful login', async () => {
    const req = {
      body: {
        username: 'existingUser',
        password: 'correctPassword'
      }
    };
    const res = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };

    await loginHandler(req, res);
    expect(res.status).toHaveBeenCalledWith(200);
    expect(res.json).toHaveBeenCalledWith({ message: 'Login successful' });
  });

  test('should respond with 500 on internal server error', async () => {
    const req = {};
    const res = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };

    const originalImplementation = loginHandler;
    loginHandler = jest.fn().mockImplementation(async () => {
      throw new Error('Authentication error');
    });

    await loginHandler(req, res);
    expect(res.status).toHaveBeenCalledWith(500);
    expect(res.json).toHaveBeenCalledWith({ error: 'Internal server error' });

    loginHandler = originalImplementation;
  });
});

describe('logoutHandler', () => {
  test('should respond with 200 on successful logout', async () => {
    const req = {};
    const res = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };

    await logoutHandler(req, res);
    expect(res.status).toHaveBeenCalledWith(200);
    expect(res.json).toHaveBeenCalledWith({ message: 'Logout successful' });
  });

  test('should respond with 500 on internal server error', async () => {
    const req = {};
    const res = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };

    const originalImplementation = logoutHandler;
    logoutHandler = jest.fn().mockImplementation(async () => {
      throw new Error('Session error');
    });

    await logoutHandler(req, res);
    expect(res.status).toHaveBeenCalledWith(500);
    expect(res.json).toHaveBeenCalledWith({ error: 'Internal server error' });

    logoutHandler = originalImplementation;
  });
});