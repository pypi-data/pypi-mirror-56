import React from 'react';
import { FormComponentProps } from 'antd/lib/form';
interface RemarkFormProps extends FormComponentProps {
    remarkable: string;
    remarkableId: string;
    afterSubmit: () => void;
}
interface RemarkModalProps {
    remarkable: string;
    remarkableId: string;
    afterSubmit: () => void;
    visible: boolean;
    onCancel: () => void;
}
declare class RemarkForm extends React.Component<RemarkFormProps, {}> {
    handleSubmit: (e: React.FormEvent<Element>) => void;
    render(): JSX.Element;
}
declare const WrappedRemarForm: import("antd/lib/form/interface").ConnectedComponentClass<typeof RemarkForm, Pick<RemarkFormProps, "afterSubmit" | "wrappedComponentRef" | "remarkable" | "remarkableId">>;
export default function RemarkModal(props: RemarkModalProps): JSX.Element;
export { WrappedRemarForm };
