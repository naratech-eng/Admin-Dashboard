import {dataProduct} from './full-data.mjs';
const jsonData = JSON.stringify(dataProduct);

// Write the JSON data to a text file
import { writeFileSync } from 'fs';
writeFileSync('product_data.json', jsonData);