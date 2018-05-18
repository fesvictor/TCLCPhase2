import * as cheerio from "cheerio";
import * as request from "request";
import { PartyDetail } from "../resultOfEachState/outputInterfaces";
import { ResultByParties, ResultByStates, ResultsOverview, StateDetail } from "./outputInterfaces";

function main() {
    const fs = require("fs");
    fs.readFile(`./htmls/overview.html`, (error, data) => {
        if (error) {
            console.log(error);
            return;
        }
        const result = scrapeData(data.toString());
        console.log(JSON.stringify(result, null, 2));
        fs.writeFile(`./outputs/overview.json`, JSON.stringify(result, null, 2));
    });
}

function scrapeData(input: string): ResultsOverview {
    const $ = cheerio.load(input);
    const parliamentSeatsResultByParties = getParliamentSeatsResultByParties($);
    const parliamentSeatsResultByStates  = getSeatsResultByStates($, "div.parliament-update");
    const stateSeatsResultByStates  = getSeatsResultByStates($, "div.state-update");
    return {
        parliamentSeatsResultByParties: parliamentSeatsResultByParties,
        parliamentSeatsResultByStates: parliamentSeatsResultByStates,
        stateSeatsResultByStates: stateSeatsResultByStates,
    };
}

function getParliamentSeatsResultByParties($: CheerioStatic): ResultByParties {
    const partiesDetails: PartyDetail[] = [];
    $("div.parliament-seats-won").find("table.table-striped").find("tr").each((index, tr) => {
        let partyName: string;
        let won: number;
        let contesting: number;
        $(tr).find("td").each((tdindex, td) => {
            const text = $(td).text();
            switch (tdindex) {
                case 0: partyName = text; break;
                case 1: won = parseInt(text, 10); break;
                case 2: contesting = parseInt(text, 10); break;
            }
        });
        partiesDetails.push({
            name: partyName,
            wonSeats: won,
            contestingSeats: contesting,
        });
    });
    return {
        parties: partiesDetails.slice(1, -1), // Ignore the first and last row
    };
}

function getSeatsResultByStates($: CheerioStatic, selector: string): ResultByStates {
    const stateDetails: StateDetail[] = [];
    $(selector).find("tr").each((trindex, tr) => {
        let name: string;
        let totalSeatsCount: number;
        let bn: number;
        let ph: number;
        let pas: number;
        let other: number;
        $(tr).find("td").each((tdindex, td) => {
            const text = $(td).text();
            switch (tdindex) {
                case 0:
                    name = text.split("[")[0].trim();
                    if (/TOTAL/.test(text)) {
                        break;
                    }
                    totalSeatsCount = parseInt(text.match(/[0-9]+/g)[0], 10);
                    break;
                case 1: bn = parseInt(text, 10); break;
                case 2: ph = parseInt(text, 10); break;
                case 3: pas = parseInt(text, 10); break;
                case 4: other = parseInt(text, 10); break;
            }
        });
        stateDetails.push({
            name: name,
            totalSeatsCount: totalSeatsCount,
            result: [bn, ph, pas, other],
        });
    });

    return {
        states: stateDetails,
    };
}

main();
