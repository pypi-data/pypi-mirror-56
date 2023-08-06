import React from 'react';
import { Form, Input, Button } from 'antd';
import { request } from '../utils';
class ExperimentMetaForm extends React.Component {
    constructor(props) {
        super(props);
        this.handleSubmit = (e) => {
            e.preventDefault();
            const { validateFields } = this.props.form;
            validateFields(async (errors, values) => {
                const response = await request('/experiments', 'post', values);
                const body = await response.json();
                this.props.afterSubmit(body.data);
            });
        };
    }
    render() {
        const { getFieldDecorator } = this.props.form;
        return (React.createElement(Form, { onSubmit: this.handleSubmit, className: "dynamic-form" },
            React.createElement(Form.Item, { label: 'Experiment Name' }, getFieldDecorator('name', {
                rules: [{
                        required: true,
                    }]
            })(React.createElement(Input, null))),
            React.createElement(Form.Item, null,
                React.createElement(Button, { type: "primary", htmlType: "submit" }, "Create Experiment"))));
    }
}
const WrappedExperimentMetaForm = Form.create({ name: 'experiment_meta_form' })(ExperimentMetaForm);
export default WrappedExperimentMetaForm;
