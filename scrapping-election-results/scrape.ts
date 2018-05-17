import * as cheerio from "cheerio";
import * as request from "request";
import {
    Contestant,
    Demographic,
    ElectionSummary,
    PartyDetail,
    Race,
    Seat,
    State,
    VoteInfo,
    VoterTurnout,
} from "./outputInterfaces";

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

function pullDataFromWebsites() {
    // Note: This function for reference purpose only, as it only needs to be called once
    const fs = require("fs");
    STATE_NAMES.forEach((x) => {
        request(`${TARGET_URL}${x}.html`, (error, response, html) => {
            fs.writeFile(`./htmls/${x}.html`, html, (err) => {
                console.log(err);
            });
        });
    });
}

function scrapeData(html): State {
    const $ = cheerio.load(html);
    const electionSummaries: ElectionSummary[] = [];
    const seatss: Seat[][] = [];
    $("div.state-overview-section").each((index, element) => {
        electionSummaries.push(getElectionSummary($, element));
    });
    $("div.tab-pane").each((index, element) => {
        seatss.push(getSeats($, element));
    });
    return {
        parliamentSeatsSummary: electionSummaries[0],
        parliamentSeats: seatss[0],
        stateSeatsSummary: electionSummaries[1],
        stateSeats: seatss[1],
    };
}

function getElectionSummary($: CheerioStatic, parent: CheerioElement): ElectionSummary {
    const electionSummary: ElectionSummary = {
        pakatanSummaries: null,
        partyDetails: [],
    };
    const pakatanSummaries: number[] = [];
    $(parent).find("li.bd-list").each((index, element) => {
        pakatanSummaries.push(parseInt($(element).text().split(" ")[1], 10));
    });
    electionSummary.pakatanSummaries = pakatanSummaries as [number, number, number, number];

    $(parent).find("table").find("tr").each((index, tr) => {
        const data: any[] = [];
        $(tr).find("td").each((tdindex, td) => {
            data.push($(td).text());
        });
        const partyDetail: PartyDetail = {
            name: data[0],
            wonSeats: parseInt(data[1], 10),
            contestingSeats: parseInt(data[2], 10),
        };
        electionSummary.partyDetails.push(partyDetail);
    });

    // Remove first row and last row
    electionSummary.partyDetails = electionSummary.partyDetails.slice(1, -1);

    return electionSummary;
}

function getSeats($: CheerioStatic, parent: CheerioElement): Seat[] {
    const seats: Seat[] = [];
    $(parent).find("div.panel-default").each((index, element) => {
        const fullName = $(element).find("a").text();
        const seat: Seat = {
            codeName: fullName.split(" ")[0],
            name: fullName.split(" ").slice(1).join(" ").split("(")[0].trim(),
            relatedSeatCode: fullName.split("(")[1] ? fullName.split("(")[1].split(")")[0] : null,
            contestants: getContestants($, element),
            voteInfo: getVoteInfo($, element),
        };
        seats.push(seat);
    });
    return seats;
}

function getContestants($: CheerioStatic, parent: CheerioElement): Contestant[] {
    const contestants: Contestant[] = [];
    $(parent).find("div.progress-wrapper").each((index, element) => {
        const nameAndParty = $(element).find("p.name-candidate").text().split("(");
        const votes = $(element).find("div.number-of-voters").text().split("%");
        const contestant: Contestant = {
            isWinner: $(element).find("i.fa-check").length > 0,
            name: nameAndParty[0].trim(),
            partyName: nameAndParty[1].trim().slice(0, -1),
            voteCount: parseInt(votes[1].replace(",", "").trim().slice(1, -1), 10),
            votePercentage: parseFloat(votes[0]),
        };
        contestants.push(contestant);
    });
    return contestants;
}

function getVoteInfo($: CheerioStatic, parent: CheerioElement): VoteInfo {
    const voteInfo: VoteInfo = {
        howManyVoters: 0,
        majority: 0,
        spoiltVotes: 0,
        unreturnedVotes: 0,
        voterTurnout: null,
        demographics: null,
        incumbent: (() => {
            try { return $(parent).find(".incumbent").text().split(":")[1].trim();
            } catch (error) { return null; }})(),
    };
    $(parent).find("div.voters-vote").find("p").each((index, element) => {
        if (index < 5) {
            const value = $(element).text().split(":")[1].replace(",", "").trim();
            switch (index) {
                case 0: voteInfo.howManyVoters   = parseInt(value, 10); break;
                case 1: voteInfo.majority        = parseInt(value, 10); break;
                case 2: voteInfo.spoiltVotes     = parseInt(value, 10); break;
                case 3: voteInfo.unreturnedVotes = parseInt(value, 10); break;
                case 4: voteInfo.voterTurnout    = getVoterTurnout(value);

            }
        } else {
            voteInfo.demographics = getDemographics($(element).text());
        }
    });
    console.log(voteInfo);
    return voteInfo;
}

function getVoterTurnout(input: string): VoterTurnout {
    const tokens = input.split("(");
    return {
        count: parseInt(tokens[0].replace(",", "").trim(), 10),
        percentage: parseFloat(tokens[1].slice(0, -2)),
    };
}

function getDemographics(input: string): Demographic {
    const races: Race[] = input.split(";").map((x) => ({
        type: x.split(" ")[0],
        percentage: parseFloat(x.split(" ")[1].slice(0, -1)),
    }));
    return { races };

}

function main() {
    const fs = require("fs");
    STATE_NAMES.slice(1, 2).forEach((x) => {
        fs.readFile(`./htmls/${x}.html`, (error, data) => {
            if (error) {
                console.log(error);
                console.log(`^ Error at ${x}.html`);
                return;
            }
            console.log(`Scraping data from ./htmls/${x}.html`);
            const result = scrapeData(data.toString());
            // console.log(JSON.stringify(result, null, 2));
            console.log(`Saving result to ./outputs/${x}.json`);
            fs.writeFile(`./outputs/${x}.json`, JSON.stringify(result, null, 2));
            console.log("=====================================");
        });
    });
}

main();
