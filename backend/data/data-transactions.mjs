import {dataTransaction} from './full-data.mjs';
const jsonData = JSON.stringify(dataTransaction);

// Write the JSON data to a text file
import { writeFileSync } from 'fs';
writeFileSync('transactions_data.json', jsonData);