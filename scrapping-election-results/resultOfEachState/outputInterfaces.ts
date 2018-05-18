export interface State {
    parliamentSeatsSummary: ElectionSummary;
    stateSeatsSummary: ElectionSummary;
    parliamentSeats: Seat[];
    stateSeats: Seat[];
}

export interface ElectionSummary {
    pakatanSummaries: [number, number, number, number]; // [BN, PAS, PH, OTHERS]
    partyDetails: PartyDetail[];
}

export interface PartyDetail {
    name: string;
    wonSeats: number;
    contestingSeats: number;
}

// NOTE: e.g. means Example
// P stands for Parliament seats
// S stands for State seats
export interface Seat {
    codeName: string;        // e.g. P114
    name: string;            // e.g. Kepong
    relatedSeatCode: string; // e.g. P114
    contestants: Contestant[];
    voteInfo: VoteInfo;
}

export interface Contestant {
    name: string;           // e.g. Lim Guan Eng
    partyName: string;      // e.g. PH - DAP
    voteCount: number;      // e.g. 51653
    votePercentage: number; // e.g. 72.2
    isWinner: boolean;
}

export interface VoteInfo {
    howManyVoters: number;
    majority: number; // Means the winner won by how many votes
    spoiltVotes: number;
    unreturnedVotes: number;
    voterTurnout: VoterTurnout;
    demographics: Demographic;
    incumbent: string; // Person in charge
}

export interface VoterTurnout {
    count: number;
    percentage: number;
}

export interface Demographic {
    races: Race[];
}

export interface Race {
    type: string; // e.g. Malay, Chinese, Indian
    percentage: number;
}
