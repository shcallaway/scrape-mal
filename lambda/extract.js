const cheerio = require("cheerio");
const AWS = require("aws-sdk");

const fields = {
  title: {
    selector: "#contentWrapper > div:nth-child(1) > h1 > span"
  },
  alt_title_en: {
    selector:
      "#content > table > tbody > tr > td.borderClass > div > div:nth-child(8)"
  },
  alt_title_jp: {
    selector:
      "#content > table > tbody > tr > td.borderClass > div > div:nth-child(9)"
  },
  type: {
    selector:
      "#content > table > tbody > tr > td.borderClass > div > div:nth-child(12) > a"
  },
  num_episodes: {
    selector:
      "#content > table > tbody > tr > td.borderClass > div > div:nth-child(13)"
  },
  status: {
    selector:
      "#content > table > tbody > tr > td.borderClass > div > div:nth-child(14)"
  },
  aired: {
    selector:
      "#content > table > tbody > tr > td.borderClass > div > div:nth-child(15)"
  },
  premiered: {
    selector:
      "#content > table > tbody > tr > td.borderClass > div > div:nth-child(16) > a"
  },
  broadcast: {
    selector:
      "#content > table > tbody > tr > td.borderClass > div > div:nth-child(17)"
  },
  source: {
    selector:
      "#content > table > tbody > tr > td.borderClass > div > div:nth-child(21)"
  },
  duration: {
    selector:
      "#content > table > tbody > tr > td.borderClass > div > div:nth-child(23)"
  },
  rating: {
    selector:
      "#content > table > tbody > tr > td.borderClass > div > div:nth-child(24)"
  },
  synopsis: {
    selector:
      "#content > table > tbody > tr > td:nth-child(2) > div.js-scrollfix-bottom-rel > table > tbody > tr:nth-child(1) > td > span"
  },
  background: {
    selector:
      "#content > table > tbody > tr > td:nth-child(2) > div.js-scrollfix-bottom-rel > table > tbody > tr:nth-child(1) > td"
  }
  //   producers: "",
  //   licensors: "",
  //   studios: "",
  //   genres: ""
};

exports.lambda_handler = async event => {
  let pageId;

  try {
    pageId = JSON.parse(event.body).mal_id;
  } catch (error) {
    return {
      statusCode: 400
    };
  }

  return getPage(pageId).then(
    page => {
      const $ = cheerio.load(page);
      const result = {
        mal_id: pageId
      };

      Object.keys(fields).forEach(field => {
        result[field] = getText($, fields[field].selector);
      });

      console.log(result);

      return {
        statusCode: 200,
        body: JSON.stringify(result)
      };
    },
    error => {
      console.log(error);

      return {
        statusCode: 500
      };
    }
  );
};

String.prototype.sanitize = function() {
  return this.trim()
    .replace(/\n/g, "")
    .replace("[Written by MAL Rewrite]", "");
};

function getPage(pageId) {

  // Use this if you are developing locally
  //   const s3 = new AWS.S3({
  //     accessKeyId: process.env.ACCESS_KEY_ID,
  //     secretAccessKey: process.env.SECRET_ACCESS_KEY
  //   });

  const s3 = new AWS.S3();

  return new Promise((resolve, reject) => {
    s3.getObject(
      {
        Bucket: process.env.BUCKET_NAME,
        Key: `anime/${pageId}.html`
      },
      function(error, data) {
        if (error) {
          reject(error);
        } else {
          const page = Buffer.from(data.Body).toString("utf8");
          resolve(page);
        }
      }
    );
  });
}

function getText($, selector) {
  const ignoredChildren = ["div", "span", "h1", "h2"];

  return $(selector)
    .find(ignoredChildren.join(", "))
    .remove()
    .end()
    .text()
    .sanitize();
}
