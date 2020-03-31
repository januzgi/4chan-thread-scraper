const fs = require('fs');

const resetJson = () => {
  // There needs to be a dummy object in place
  let emptyObj = { links: ['dummy'] };
  console.log('Overwriting imgUrls.json file.');
  let json = JSON.stringify(emptyObj);

  // Write the file
  fs.writeFile('imgUrls.json', json, 'utf8', function(err) {
    if (err) {
      return console.log(err);
    }
    console.log('File saved successfully!');
  });
};

// Empty the imgUrls.json file by overwriting the data
resetJson();
