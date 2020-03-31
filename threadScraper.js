const Nightmare = require('nightmare');
const cheerio = require('cheerio');
const fs = require('fs');

// Read each thread's URLs from the log.json
function readThreadUrls() {
  return new Promise((resolve) => {
    fs.readFile('log.json', 'utf8', function readFileCallback(err, data) {
      if (err) {
        console.log(err);
        resolve('error');
      } else {
        let urls = JSON.parse(data); // Now urls is an object
        resolve(urls);
      }
    });
  });
}

// Gets the thread's img urls correctly
function crawlThread(url) {
  return new Promise((resolve) => {
    console.log('Starting crawl process for the thread ' + url);
    const nightmare = new Nightmare({ show: false });
    try {
      let images = nightmare
        .goto(url)
        .wait('.thread')
        .evaluate(() => {
          let elements = Array.from(
            document.getElementsByClassName('fileThumb')
          );
          return elements.map((elem) => {
            return {
              content: elem.innerHTML
            };
          });
        })
        .end()
        .then((images) => {
          console.log(
            'Found ' + images.length + ' images. Mapping the urls...'
          );
          let formatted = images.map((item) => {
            let $ = cheerio.load(item.content);
            link = 'https:' + $('img').attr('src');
            data = {
              link: link
            };
            return data;
          });
          return formatted;
        });
      resolve(images);
    } catch (err) {
      console.log(err);
      resolve('error');
    }
  });
}

// Adds the read urls to imgUrls.json
function writeImgUrls(response) {
  return new Promise((resolve) => {
    let obj;
    try {
      // Read the json file to add data to it
      fs.readFile('imgUrls.json', 'utf8', function readFileCallback(err, data) {
        if (err) {
          console.log(err);
          resolve('error');
        } else {
          obj = JSON.parse(data); // Now it's an object
          obj.links.push(response); // Add the data
          json = JSON.stringify(obj); // Convert back to json
          // Write the file
          fs.writeFile('imgUrls.json', json, 'utf8', function(err) {
            if (err) {
              console.log(err);
              resolve('error');
            }
            console.log('File saved successfully!');
            resolve('Success!');
          });
        }
      });
    } catch (err) {
      console.log(err);
      resolve('error');
    }
  });
}

async function run() {
  // 1. Read the thread urls from log.json
  let urls = await readThreadUrls();
  if (urls === 'error') {
    console.log('Error in readThreadUrls()');
  } else {
    console.log(
      'Read URLs correctly from log.json. \nStarting to crawl threads.'
    );
  }

  // 2. Run the crawlThread and writeImgUrls async functions once for every URL
  for (let url in urls) {
    // Only go to real urls
    if (urls[url]) {
      // Crawls through every thread and returns the img urls as a response
      let response = await crawlThread(urls[url].link);
      if (response === 'error') {
        console.log('Error in crawlThread(url)');
      } else {
        console.log('Completed with no errors! Adding urls to imgUrls.json.');
      }

      // Writes the img urls into imgUrls.json
      let writeUrlsToImgJson = await writeImgUrls(response);
      if (writeUrlsToImgJson === 'error') {
        console.log('Error in writeImgUrls(response)');
      } else {
        console.log('Added img urls to imgUrls.json succesfully.');
        console.log('File output complete.');
      }
    }
  }
}

run();
