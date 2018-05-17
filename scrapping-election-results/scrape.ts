import * as cheerio from "cheerio";
import * as request from "request";

const TARGET_URL = "https://election.thestar.com.my/";
const STATE_NAMES = [
    "ft", // federal territories
    "johor",
    "kedah",
    "kelantan",
    "malacca",
    "negerisembilan",
    "pahang",
    "penang",
    "perak",
    "perlis",
    "sabah",
    "sarawak",
    "selangor",
    "terengganu",
];

function getStatesName() {
    // Note: The function below is for reference purpose only, as it only needs to be called once
    // return Array
    //     .from(document.getElementsByClassName("state-list")[0].children)
    //     .slice(1)
    //     .map((x) => (x.children[0]as HTMLAnchorElement).href)
    //     .map((x) => x.split("my/")[1])
    //     .map((x) => x.split(".")[0]);
}

/**
 * Note: The function below is for reference purpose only, as it only needs to be called once
 */

function pullDataFromWebsites() {
    const fs = require("fs");
    STATE_NAMES.forEach((x) => {
        request(`${TARGET_URL}${x}.html`, (error, response, html) => {
            fs.writeFile(`./htmls/${x}.html`, html, (err) => {
                console.log(err);
            });
        });
    });
}

// request(TARGET_URL, processResponse);

/**
 * Notes:
 * - f1 stands for Parliament, f2 stands for State
 */
function processResponse(error, response, html) {
    if (error) {
        throw error;
    }
    const $ = cheerio.load(html);
}

pullDataFromWebsites();
