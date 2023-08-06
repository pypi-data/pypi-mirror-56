import React from 'react';
import { Form, Input, Button, Modal } from 'antd';
import { request } from '../utils';
class RemarkForm extends React.Component {
    constructor() {
        super(...arguments);
        this.handleSubmit = (e) => {
            e.preventDefault();
            const { validateFields } = this.props.form;
            validateFields((errors, values) => {
                request('/experiments/remark', 'post', Object.assign(values, {
                    identity: this.props.remarkableId,
                    remarkableType: this.props.remarkable
                }));
                this.props.afterSubmit();
            });
        };
    }
    render() {
        const { getFieldDecorator } = this.props.form;
        return (React.createElement(Form, { onSubmit: this.handleSubmit, className: "dynamic-form" },
            React.createElement(Form.Item, { label: "Remark", key: "remark" }, getFieldDecorator('remark', {
                rules: [{ required: true }]
            })(React.createElement(Input, { placeholder: "Input remark..." }))),
            React.createElement(Form.Item, null,
                React.createElement(Button, { type: "primary", htmlType: "submit" }, "Add remark"))));
    }
}
const WrappedRemarForm = Form.create({ name: 'remark_form' })(RemarkForm);
export default function RemarkModal(props) {
    return (React.createElement(Modal, { footer: false, title: "Add Remark", visible: props.visible, onCancel: props.onCancel },
        React.createElement(WrappedRemarForm, Object.assign({}, props))));
}
export { WrappedRemarForm };
