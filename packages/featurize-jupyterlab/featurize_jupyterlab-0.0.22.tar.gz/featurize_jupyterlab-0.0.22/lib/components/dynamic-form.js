import React, { Fragment } from 'react';
import { Form, Input, Button, Select, Switch, InputNumber, Upload, Icon } from 'antd';
import { capitalize, getCookie, requestData } from '../utils';
import _ from 'lodash';
class DynamicForm extends React.Component {
    constructor(props) {
        super(props);
        this.handleSubmit = (e) => {
            e.preventDefault();
            const { validateFields } = this.props.form;
            validateFields((errors, values) => {
                if (!errors) {
                    this.props.onSubmit(values);
                }
            });
            this.props.form.resetFields();
        };
        this.handleRemove = (field) => {
            return async (file) => {
                const { fieldUploadedFiles } = this.state;
                fieldUploadedFiles[field.key] = fieldUploadedFiles[field.key].filter((v) => v.url !== file.url);
                this.setState({ fieldUploadedFiles });
                const data = await requestData(`/executions/${this.props.executionId}/upload`, 'delete', {
                    filename: file.name,
                    fieldname: field.key,
                });
                this.props.form.setFieldsValue({
                    [`${this.props.prefix}${field.key}`]: data.map((d) => d.url),
                });
            };
        };
        this.handleChange = (field) => {
            return (e) => {
                if (e.file.response) {
                    const { fieldUploadedFiles } = this.state;
                    fieldUploadedFiles[field.key] = e.file.response.data;
                    setTimeout(() => {
                        this.props.form.setFieldsValue({
                            [`${this.props.prefix}${field.key}`]: e.file.response.data.map((d) => d.url),
                        });
                    });
                }
                const { fieldUploadedFiles } = this.state;
                fieldUploadedFiles[field.key] = e.fileList;
                this.setState({ fieldUploadedFiles });
            };
        };
        this.state = {
            fieldUploadedFiles: {},
            checkpointCollections: {},
        };
    }
    async setUploaderFieldState(field) {
        const uploadFileUrls = await requestData(`/executions/${this.props.executionId}/upload`, 'get', {
            field: field.key,
        });
        const { fieldUploadedFiles } = this.state;
        fieldUploadedFiles[field.key] = uploadFileUrls;
        this.setState({ fieldUploadedFiles });
        setTimeout(() => {
            this.props.form.setFieldsValue({
                [`${this.props.prefix}${field.key}`]: fieldUploadedFiles[field.key].map((d) => d.url),
            });
        });
    }
    async setCheckpointFieldState(field) {
        const { checkpointCollections } = this.state;
        checkpointCollections[field.key] = await requestData(`/experiments/${this.props.experimentId}/checkpoints`, 'get');
        this.setState({ checkpointCollections });
    }
    componentDidMount() {
        this.props.component.options.forEach(async (field, index) => {
            if (field.settings.type === 'uploader') {
                await this.setUploaderFieldState(field);
            }
            else if (field.settings.type === 'checkpoint') {
                await this.setCheckpointFieldState(field);
            }
        });
    }
    renderUploaderInput(field) {
        return (React.createElement(Upload, { action: `/featurize/executions/${this.props.executionId}/upload`, headers: { 'X-XSRFToken': getCookie('_xsrf') }, listType: 'picture', multiple: true, name: field.key, onChange: this.handleChange(field), fileList: this.state.fieldUploadedFiles[field.key], onRemove: this.handleRemove(field) },
            React.createElement(Button, null,
                React.createElement(Icon, { type: "upload" }),
                " Upload")));
    }
    renderStringInput(field) {
        return (React.createElement(Input, { placeholder: field.settings.help }));
    }
    renderHardcodeInput(field) {
        return (React.createElement(Input, { placeholder: field.settings.help, disabled: true }));
    }
    renderNumberInput(field) {
        return (React.createElement(InputNumber, { placeholder: field.settings.help }));
    }
    renderBooleanInput(field) {
        return (React.createElement(Switch, { defaultChecked: this.fieldValue(field), onChange: () => { } }));
    }
    renderCheckpointInput(field) {
        return (React.createElement(Select, { showSearch: true, getPopupContainer: triggerNode => triggerNode.parentElement }, Object.keys(this.state.checkpointCollections[field.key] || {}).map((groupName) => {
            return (React.createElement(Select.OptGroup, { label: groupName }, this.state.checkpointCollections[field.key][groupName].map((checkpoint) => {
                return (React.createElement(Select.Option, { value: `${checkpoint.executionId}.${checkpoint.name}`, className: 'dynamic-form-option' },
                    checkpoint.name,
                    React.createElement("span", { className: 'option-end-desc' }, checkpoint.createdAt)));
            })));
        })));
    }
    renderCollectionInput(field) {
        const collections = field.settings.collection.map((item) => {
            if (Array.isArray(item)) {
                return item;
            }
            else {
                return [item, item];
            }
        });
        return (React.createElement(Select, { getPopupContainer: triggerNode => triggerNode.parentElement }, collections.map((item) => {
            return (React.createElement(Select.Option, { value: item[1] }, item[0]));
        })));
    }
    fieldValue(field) {
        const config = this.props.componentConfig;
        if (config && config.parameters && config.parameters[_.camelCase(field.key)]) {
            return config.parameters[_.camelCase(field.key)];
        }
        else {
            return field.settings.default;
        }
    }
    renderFields() {
        const { getFieldDecorator } = this.props.form;
        return (React.createElement(Fragment, null, this.props.component.options.map((field, i) => {
            return (React.createElement(Form.Item, { label: field.name, key: field.key }, getFieldDecorator(`${this.props.prefix}${field.key}`, {
                initialValue: this.fieldValue(field),
                rules: [{
                        required: field.settings.required,
                        message: field.settings.help,
                    }]
            })(this[`render${capitalize(field.settings.type || 'string')}Input`](field))));
        })));
    }
    render() {
        if (this.props.fieldsOnly) {
            return this.renderFields();
        }
        else {
            return (React.createElement(Form, Object.assign({ onSubmit: this.handleSubmit, className: "dynamic-form" }, this.props.formProps),
                this.renderFields(),
                React.createElement(Form.Item, null,
                    React.createElement(Button, { type: "primary", htmlType: "submit", className: "login-form-button" }, "Save and Select"))));
        }
    }
}
DynamicForm.defaultProps = {
    formProps: {},
    prefix: ''
};
const WrappedDynamicForm = Form.create({ name: 'normal_login' })(DynamicForm);
export { DynamicForm, WrappedDynamicForm };
