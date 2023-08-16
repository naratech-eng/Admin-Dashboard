import {dataOverallStat} from './full-data.mjs';
const jsonData = JSON.stringify(dataOverallStat);

// Write the JSON data to a text file
import { writeFileSync } from 'fs';
writeFileSync('overallstat_data.json', jsonData);