import React from 'react';
import ExperimentMetaForm from '../components/experiment-meta-form';
import { Typography } from 'antd';
import { withRouter } from 'react-router-dom';
import FeaturizeBreadcrumb from '../components/breadcrumb';
const { Title, Paragraph } = Typography;
class CreateExperimentPage extends React.Component {
    constructor() {
        super(...arguments);
        this.afterCreateExperiment = () => {
            this.props.history.push(`/featurize/experiments`);
        };
    }
    render() {
        const breadcrumbLinks = [
            { name: 'Experiment List', link: '/featurize/experiments' },
            { name: 'Create Experiment', link: '/featurize/experiments/new' }
        ];
        return (React.createElement("div", { className: "featurize__create-experiment-page" },
            React.createElement(FeaturizeBreadcrumb, { links: breadcrumbLinks }),
            React.createElement(Typography, null,
                React.createElement(Title, null, "New Experiment"),
                React.createElement(Paragraph, null, "An experiment is a training unit. You can set your training configuration, tweak hyperparameters, monitor the training status of a experiment.")),
            React.createElement(ExperimentMetaForm, { afterSubmit: this.afterCreateExperiment })));
    }
}
export default withRouter(CreateExperimentPage);
