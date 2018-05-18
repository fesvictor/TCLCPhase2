import * as cheerio from "cheerio";
import * as request from "request";
import { PartiesData, PartyDetail } from "./outputInterfaces";

function main() {
    const fs = require("fs");
    // The file is obtained from https://election.thestar.com.my/
    fs.readFile(`./htmls/parties.html`, (error, data) => {
        if (error) {
            console.log(error);
            return;
        }
        const result = scrapeData(data.toString());
        result.partyDetails.forEach((x) => {
            console.log("============================================");
            console.log(x.category);
            console.log("  " + x.fullname + " (" + x.shortname + ")");
            console.log("     --> " + x.chairman);
            console.log("============================================");
        });
        fs.writeFile(`./outputs/parties.json`, JSON.stringify(result, null, 2));
    });
}

function scrapeData(input: string): PartiesData {
    const partyDetails: PartyDetail[] = [];
    const $ = cheerio.load(input);
    let allText: string;
    $("div.overview-two").each((index, element) => {
        allText = $(element).text();
    });
    const result = allText.split("\n").filter((x) => x.length > 0 && !/^\s+$/.test(x)).slice(1, -2);
    let categoryName: string;
    let partyName: string;
    let presidentName: string;
    console.log(result);
    for (let i = 0; i < result.length; i++) {
        const x = result[i];
        const precedingSpaceCount = x.match(/^\s+/)[0].length;
        if (precedingSpaceCount < 20) {
            categoryName = x.trim();
        } else {
            partyName = x;
            console.log(x);
            console.log(result[i + 1]);
            if (/:/.test(result[i + 1])) {
                presidentName = result[i + 1].split(":")[1].trim();
                i++;
            } else {
                presidentName = null;
            }
            partyDetails.push({
                category: categoryName,
                chairman: presidentName,
                fullname: /\(/.test(partyName) ? partyName.split("(")[0].trim() : partyName.trim(),
                shortname: /\(/.test(partyName) ? partyName.split("(")[1].split(")")[0].trim() : null,
            });
        }
    }
    return {
        partyDetails: partyDetails,
    };
}

main();
