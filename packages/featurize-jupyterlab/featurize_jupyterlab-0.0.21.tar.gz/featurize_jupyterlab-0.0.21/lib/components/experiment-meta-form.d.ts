import React from 'react';
import { FormComponentProps } from 'antd/lib/form';
import { Experiment } from '../store/constant';
export interface ExperimentMetaFormProp extends FormComponentProps {
    afterSubmit: (state: Experiment) => void;
}
declare class ExperimentMetaForm extends React.Component<ExperimentMetaFormProp, {}> {
    constructor(props: ExperimentMetaFormProp);
    handleSubmit: (e: React.FormEvent<Element>) => void;
    render(): JSX.Element;
}
declare const WrappedExperimentMetaForm: import("antd/lib/form/interface").ConnectedComponentClass<typeof ExperimentMetaForm, Pick<ExperimentMetaFormProp, "afterSubmit" | "wrappedComponentRef">>;
export default WrappedExperimentMetaForm;
