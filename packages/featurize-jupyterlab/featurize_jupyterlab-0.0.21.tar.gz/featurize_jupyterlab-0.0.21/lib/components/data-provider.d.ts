export interface Points {
    [key: number]: {
        x: number;
        y: number;
    };
}
export declare class DataProvider {
    labels: string[];
    data: any;
    datasetName: string;
    values: number[];
    graphName: string;
    identity: string;
    startAt: number;
    constructor(identity: string, graphName: string);
    fetchMore(): Promise<Points>;
}
