import React from 'react';
import { FormComponentProps } from "antd/lib/form/Form";
import { Component, ComponentConfig, Field, Execution } from "../store/constant";
export interface DynamicFormProp extends FormComponentProps {
    component: Component;
    componentConfig: ComponentConfig | Execution;
    executionId?: string;
    experimentId?: string;
    fieldsOnly?: boolean;
    prefix?: string;
    onSubmit?: (values: any) => void;
    formProps?: any;
}
interface DynamicFormState {
    fieldUploadedFiles: any;
    checkpointCollections: any;
}
declare class DynamicForm extends React.Component<DynamicFormProp, DynamicFormState> {
    [key: string]: any;
    static defaultProps: {
        formProps: {};
        prefix: string;
    };
    constructor(props: DynamicFormProp);
    setUploaderFieldState(field: Field): Promise<void>;
    setCheckpointFieldState(field: Field): Promise<void>;
    componentDidMount(): void;
    handleSubmit: (e: React.FormEvent<Element>) => void;
    handleRemove: (field: Field) => (file: any) => Promise<void>;
    handleChange: (field: Field) => (e: any) => void;
    renderUploaderInput(field: Field): JSX.Element;
    renderStringInput(field: Field): JSX.Element;
    renderHardcodeInput(field: Field): JSX.Element;
    renderNumberInput(field: Field): JSX.Element;
    renderBooleanInput(field: Field): JSX.Element;
    renderCheckpointInput(field: Field): JSX.Element;
    renderCollectionInput(field: Field): JSX.Element;
    fieldValue(field: Field): any;
    renderFields(): JSX.Element;
    render(): JSX.Element;
}
declare const WrappedDynamicForm: import("antd/lib/form/interface").ConnectedComponentClass<typeof DynamicForm, Pick<DynamicFormProp, "prefix" | "onSubmit" | "component" | "wrappedComponentRef" | "executionId" | "experimentId" | "componentConfig" | "fieldsOnly" | "formProps">>;
export { DynamicForm, WrappedDynamicForm };
