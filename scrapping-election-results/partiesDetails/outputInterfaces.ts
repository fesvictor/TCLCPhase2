export interface PartiesData {
    partyDetails: PartyDetail[];
}

export interface PartyDetail {
    fullname: string;
    shortname: string;
    chairman: string;
    category: string; // E.g. "Barisan Nasional component parties"
}
