import React from 'react';
import { Table, Tabs, Icon, Button } from 'antd';
import { Link } from 'react-router-dom';
import { getExperimentStore } from '../store';
import Operations from '../components/operations';
import FeaturizeBreadcrumb from '../components/breadcrumb';
import StatusTag from '../components/status-tag';
class ShowExperimentPage extends React.Component {
    constructor(props) {
        super(props);
        this.refresh = async () => {
            this.setState({
                loading: true
            });
            this.setState({
                loading: false,
                experiment: await this.experimentStore.loadState()
            });
        };
        this.onRemark = () => {
            this.refresh();
        };
        this.onTabChanged = (activeKey) => {
            this.setState({
                activeTab: activeKey,
            });
        };
        this.onDelete = () => {
            this.setState({
                isDeleted: true,
            });
        };
        const { id } = this.props.match.params;
        this.experimentStore = getExperimentStore(id);
        this.state = {
            experiment: this.experimentStore.getState(),
            activeTab: 'executions',
            isDeleted: false,
            loading: true
        };
    }
    async componentDidMount() {
        this.refresh();
    }
    render() {
        const breadcrumbLinks = [
            { name: 'Experiment List', link: '/featurize/experiments' },
            { name: this.state.experiment.name, link: `/featurize/experiments/${this.state.experiment.id}` }
        ];
        const columns = [
            {
                title: 'Name',
                dataIndex: 'name',
                key: 'name',
                render: (text, execution) => (React.createElement(Link, { to: `/featurize/executions/${execution.id}` }, text))
            },
            {
                title: 'Status',
                dataIndex: 'status',
                key: 'status',
                render: (text) => {
                    return (React.createElement(StatusTag, { status: text }));
                }
            },
            {
                title: 'Type',
                dataIndex: 'taskType',
                key: 'taskType'
            },
            {
                title: 'Created At',
                dataIndex: 'createdAt',
                key: 'createdAt',
            },
            {
                title: 'Action',
                key: 'action',
                render: (text, execution) => {
                    return (React.createElement(Operations, { executionId: execution.id, experimentId: this.state.experiment.id, statusCallback: this.refresh, deleteCallback: this.refresh }));
                }
            }
        ];
        return (React.createElement("div", { className: "featurize__show-experiment-page" },
            React.createElement(FeaturizeBreadcrumb, { links: breadcrumbLinks }),
            React.createElement(Tabs, { activeKey: this.state.activeTab, animated: false, onChange: this.onTabChanged },
                React.createElement(Tabs.TabPane, { tab: React.createElement("span", null,
                        React.createElement(Icon, { type: "code" }),
                        "Executions"), key: "executions" },
                    React.createElement("div", { className: "executions" },
                        React.createElement("div", { className: "page-operations" },
                            React.createElement(Link, { to: `/featurize/experiments/${this.state.experiment.id}/newExecution` },
                                React.createElement(Button, { type: "primary", size: "default" }, "New Execution"))),
                        React.createElement(Table, { columns: columns, dataSource: this.state.experiment.excutions, rowKey: "id", loading: this.state.loading }))))));
    }
}
export default ShowExperimentPage;
