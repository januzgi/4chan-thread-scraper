const cheerio = require('cheerio');
const axios = require('axios');
const fs = require('fs');
const baseUrl = 'https://boards.4channel.org/biz/thread/';

// All thread URLs
let allThreadNos = [];
// All imgUrls
let allImgUrls = [];

// Reset the imgUrls.json file
const resetJson = async () => {
  // Dummy object
  let emptyObj = { links: ['dummy'] };
  console.log('Resetting imgUrls.json file.');
  let json = JSON.stringify(emptyObj);
  // Write the file
  fs.writeFile('imgUrls.json', json, 'utf8', function (err) {
    if (err) {
      console.log(err);
      return 'error';
    }
    return 'Success!';
  });
};

const fetchHTML = async (url) => {
  const result = await axios.get(url);
  // Return the data object of the response
  return result.data;
};

// Get the thread img urls
const crawlThread = async (contents) => {
  // Load the cheerio object
  let $ = cheerio.load(contents);
  // Add each img thumbnail resource url to allImgUrls
  $('.fileThumb > img').each((i, element) => {
    imgUrl = 'https:' + $(element).attr('src');
    allImgUrls.push(imgUrl);
  });
  return 'Success!';
};

// Adds the read urls to imgUrls.json
const writeImgUrls = async (response) => {
  // return new Promise((resolve) => {
  let obj;
  try {
    // Read the json file to add data to it
    fs.readFile('imgUrls.json', 'utf8', function readFileCallback(err, data) {
      if (err) {
        console.log(err);
        // resolve('error');
        return 'error';
      } else {
        obj = JSON.parse(data); // Now it's an object
        obj.links.push(response); // Add the data
        json = JSON.stringify(obj); // Convert back to json
        // Write the file
        fs.writeFile('imgUrls.json', json, 'utf8', function (err) {
          if (err) {
            console.log(err);
            // resolve('error');
            return 'error';
          }
          // resolve('Success!');
          return 'Success!';
        });
      }
    });
  } catch (err) {
    console.log(err);
    // resolve('error');
    return 'error';
  }
  // });
};

const run = async () => {
  // 1. Reset imgUrls.json to write the urls from this fetch
  let reset = await resetJson();
  if (reset === 'error') {
    console.log('Error in resetJson()');
  } else {
    console.log('Reseted imgUrls.json. \nStarting to fetch thread URLs.');
  }

  // 2. Get the json for /biz/ thread URLs
  let json = await fetchHTML('https://a.4cdn.org/biz/threads.json');
  // Read each URL from the json
  for (let i = 0; i < json.length; i++) {
    for (let j = 0; j < json[i].threads.length; j++) {
      allThreadNos.push(json[i].threads[j]['no']);
    }
  }
  // Delete the first two URLs of the sticky threads
  allThreadNos.splice(0, 2);
  console.log('Fetched thread URLs.');

  // 3. Run the crawlThread and writeImgUrls async functions once for every URL
  console.log('Crawling thread: ');
  let counter = 1; // counter for urls
  for (let k = 0; k < allThreadNos.length; k++) {
    // Attach the no of the thread to the url
    let url = baseUrl + allThreadNos[k];
    // Only go to existing items
    if (url) {
      // Get the contents of this thread
      let contents = await fetchHTML(url);
      // Crawls through every thread
      let response = await crawlThread(contents);
      if (response === 'error') {
        console.log('Error in crawlThread(url)');
      } else {
        console.log(counter + '/' + allThreadNos.length + ' # ' + url);
        counter += 1;
      }
    }
  }

  // Writes all of the the img urls into imgUrls.json
  let writeUrlsToImgJson = await writeImgUrls(allImgUrls);
  if (writeUrlsToImgJson === 'error') {
    console.log('Error in writeImgUrls(response)');
  } else {
    console.log('Added allImgUrls to imgUrls.json succesfully.');
    console.log('\nscraper.js is done.\n');
  }
};

run();
