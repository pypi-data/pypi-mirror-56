import React from 'react';
import { RouteComponentProps } from 'react-router-dom';
declare type PropsType = RouteComponentProps<void> & {
    someString: string;
};
declare class CreateExperimentPage extends React.Component<PropsType> {
    afterCreateExperiment: () => void;
    render(): JSX.Element;
}
declare const _default: React.ComponentClass<Pick<PropsType, "someString">, any> & import("react-router").WithRouterStatics<typeof CreateExperimentPage>;
export default _default;
