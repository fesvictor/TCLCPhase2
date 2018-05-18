import { PartyDetail } from "./../resultOfEachState/outputInterfaces";
export interface ResultsOverview {
    parliamentSeatsResultByParties: ResultByParties;
    parliamentSeatsResultByStates: ResultByStates;
    stateSeatsResultByStates: ResultByStates;
}

export interface ResultByParties {
    parties: PartyDetail[];
}

export interface ResultByStates {
    states: StateDetail[];
}

export interface StateDetail {
    name: string;
    totalSeatsCount: number;
    result: [number, number, number, number]; // BN, PH, PAS, OTHER
}
