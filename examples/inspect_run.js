'use strict';
const fs = require('node:fs');
const {parseRunRecord} = require('../src/doc_tools.js');
if (process.argv.length !== 3) {
  console.error('Usage: node examples/inspect_run.js path/to/result.json');
  process.exit(2);
}
try {
  const record = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  console.log(JSON.stringify(parseRunRecord(record), null, 2));
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
