const Nightmare = require('nightmare');
const cheerio = require('cheerio');
const fs = require('fs');

const board = 'biz';

const url = (board) => {
  return 'https://boards.4channel.org/' + board + '/catalog';
};

// Gets the thread urls correctly and writes them into a file.
const crawlCatalogue = async () => {
  console.log('Starting crawl process for /' + board + '/');
  const nightmare = new Nightmare({ show: false });
  try {
    let threads = await nightmare
      .goto(url(board))
      .wait('#threads .thread')
      .evaluate(() => {
        let elements = Array.from(document.getElementsByClassName('thread'));
        return elements.map((elem) => {
          return {
            content: elem.innerHTML
          };
        });
      })
      .end()
      .then((threads) => {
        console.log(
          'Found ' + threads.length + ' threads. Mapping to objects...'
        );
        // Delete first two static threads
        delete threads[0];
        delete threads[1];
        let formatted = threads.map((item) => {
          let $ = cheerio.load(item.content);
          link = 'https:' + $('a').attr('href');
          data = {
            link: link
          };
          return data;
        });
        return formatted;
      });
    return threads;
  } catch (err) {
    console.log(err);
  }
};

crawlCatalogue()
  .then((response) => {
    console.log('Completed with no errors! Writing file.');
    let formattedResponse = JSON.stringify(response, null, 4);
    try {
      fs.writeFileSync('log.json', formattedResponse, 'utf8');
      console.log('File output complete.');
    } catch (err) {
      if (err) throw err;
    }
  })
  .catch((e) => console.log(e));
