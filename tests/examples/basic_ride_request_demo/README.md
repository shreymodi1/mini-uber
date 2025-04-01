import fs from 'fs';
import path from 'path';

describe('Basic Ride Request Demo README', () => {
  let readmeContent;

  beforeAll(() => {
    const readmePath = path.join(__dirname, '../examples/basic_ride_request_demo/README.md');
    readmeContent = fs.readFileSync(readmePath, 'utf-8');
  });

  test('should include instructions for installing dependencies', () => {
    expect(readmeContent).toMatch(/(install|dependencies)/i);
  });

  test('should include instructions for running the server', () => {
    expect(readmeContent).toMatch(/(run the server|start the server)/i);
  });

  test('should mention simulating ride requests', () => {
    expect(readmeContent).toMatch(/(ride request|simulation)/i);
  });
});