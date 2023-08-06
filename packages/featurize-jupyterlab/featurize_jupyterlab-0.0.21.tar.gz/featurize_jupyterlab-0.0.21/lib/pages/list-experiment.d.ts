import React from 'react';
import { RouteComponentProps } from 'react-router-dom';
import ListStore from '../store/list-store';
import { Experiment } from '../store/constant';
declare type PropsType = RouteComponentProps<void> & {};
export interface ListExperimentState {
    loading: boolean;
    list: any[];
}
declare class ListExperimentPage extends React.Component<PropsType, ListExperimentState> {
    listStore: ListStore<Experiment>;
    constructor(props: PropsType);
    refresh: () => Promise<void>;
    componentDidMount(): void;
    deleteExperiment(identity: string): () => Promise<void>;
    setExperimentStatus(identity: string, status: string): () => Promise<void>;
    render(): JSX.Element;
}
declare const _default: React.ComponentClass<Pick<RouteComponentProps<void, import("react-router").StaticContext, any>, never>, any> & import("react-router").WithRouterStatics<typeof ListExperimentPage>;
export default _default;
