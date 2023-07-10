import {dataProductStat} from './full-data.mjs';
const jsonData = JSON.stringify(dataProductStat);

// Write the JSON data to a text file
import { writeFileSync } from 'fs';
writeFileSync('productstat_data.json', jsonData);