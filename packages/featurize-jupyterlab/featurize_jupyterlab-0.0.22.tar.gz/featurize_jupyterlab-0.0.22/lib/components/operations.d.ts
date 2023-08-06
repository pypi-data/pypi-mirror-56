import React from 'react';
import ExperimentStore from '../store/experiment-store';
import { Execution } from '../store/constant';
interface OperationsProps {
    executionId: string;
    experimentId: string;
    statusCallback: (type: string) => any;
    deleteCallback: () => any;
    remarkCallback?: () => any;
}
interface OperationsState {
    showBootModal: boolean;
    showRemarkModal: boolean;
    bootCommand: string;
    devBootCommand: string;
    execution: Execution;
    experimentStore: ExperimentStore;
}
export default class Operations extends React.Component<OperationsProps, OperationsState> {
    constructor(props: OperationsProps);
    componentDidMount: () => Promise<void>;
    showBootModal: () => () => void;
    stopExecution: () => () => void;
    deleteExecution(): () => Promise<void>;
    onRemark: () => void;
    render(): JSX.Element;
}
export {};
