import { dataUser } from './full-data.mjs';
// import { dataUser } from './data/full-data.mjs';
// const dataSample = [
//   {
//     name: "John Doe",
//     age: 30,
//     email: "johndoe@example.com"
//   },
//   {
//     name: "Jane Smith",
//     age: 25,
//     email: "janesmith@example.com"
//   }
// ];

const jsonData = JSON.stringify(dataUser);

// Write the JSON data to a text file
import { writeFileSync } from 'fs';
writeFileSync('user_data.json', jsonData);

// run `node --experimental-modules your-script.mjs` get the data converted
