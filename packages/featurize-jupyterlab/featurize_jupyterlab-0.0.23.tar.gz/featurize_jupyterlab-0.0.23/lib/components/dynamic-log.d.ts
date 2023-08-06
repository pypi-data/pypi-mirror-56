import React from 'react';
import { Execution } from '../store/constant';
interface Log {
    text: string;
}
interface DynamicLogProps {
    maxVisibleLines: number;
    maxFetchLines: number;
    pullInterval: number;
    offset: number;
    execution: Execution;
}
interface DynamicLogState {
    logs: Log[];
}
declare class DynamicLog extends React.Component<DynamicLogProps, DynamicLogState> {
    private currentLine;
    private stopFetch;
    static defaultProps: {
        maxVisibleLines: number;
        maxFetchLines: number;
        pullInterval: number;
        offset: number;
    };
    constructor(props: DynamicLogProps);
    fetch: () => Promise<Log[]>;
    update: () => Promise<void>;
    componentDidMount(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
}
export default DynamicLog;
