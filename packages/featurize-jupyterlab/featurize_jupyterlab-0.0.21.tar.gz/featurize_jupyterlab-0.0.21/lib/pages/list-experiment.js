import React from 'react';
import { withRouter } from 'react-router-dom';
import { getStore, getExperimentStore } from '../store';
import { Table, Button } from 'antd';
import { Link } from "react-router-dom";
// import StatusTag from '../components/status-tag';
// import Operations from '../components/operations';
import FeaturizeBreadcrumb from '../components/breadcrumb';
class ListExperimentPage extends React.Component {
    constructor(props) {
        super(props);
        this.refresh = async () => {
            this.setState({
                list: await this.listStore.loadState(),
                loading: false
            });
        };
        this.state = {
            loading: true,
            list: [],
        };
        this.listStore = getStore('experiments');
    }
    componentDidMount() {
        this.setState({ list: this.listStore.getState() });
        this.refresh();
    }
    deleteExperiment(identity) {
        return async () => {
            await getExperimentStore(identity).delete();
            this.setState({ list: await this.listStore.loadState() });
        };
    }
    setExperimentStatus(identity, status) {
        return async () => {
            await getExperimentStore(identity).setStatus(status);
            this.setState({ list: await this.listStore.loadState() });
        };
    }
    render() {
        const columns = [
            {
                title: 'Name',
                dataIndex: 'name',
                key: 'name',
                render: (text, experiment) => (React.createElement(Link, { to: `/featurize/experiments/${experiment.id}` }, text))
            },
            // {
            //   title: 'Status',
            //   dataIndex: 'status',
            //   key: 'status',
            //   render: (text: string, experiment: Experiment) => {
            //     return (
            //       <StatusTag status={text} />
            //     )
            //   }
            // },
            // {
            //   title: 'Hash',
            //   dataIndex: 'identity',
            //   key: 'identity',
            //   render: (text: string, experiment: Experiment) => {
            //     return text.substring(0, 6);
            //   }
            // },
            {
                title: 'Created At',
                dataIndex: 'createdAt',
                key: 'createdAt',
            }
            // {
            //   title: 'Action',
            //   key: 'action',
            //   render: (text: string, experiment: Experiment) => {
            //     return (
            //       <Operations
            //         experimentStore={getExperimentStore(experiment.identity)}
            //         statusCallback={this.refresh}
            //         deleteCallback={this.refresh}
            //       />
            //     );
            //   }
            // }
        ];
        return (React.createElement("div", { className: "featurize__list-experiment-page" },
            React.createElement(FeaturizeBreadcrumb, { links: [{ name: 'Experiment List', link: '/featurize/experiments' }] }),
            React.createElement("div", { className: "page-operations" },
                React.createElement(Link, { to: "/featurize/experiments/new" },
                    React.createElement(Button, { type: "primary", size: "default" }, "New Experiment"))),
            React.createElement(Table, { columns: columns, dataSource: this.state.list, rowKey: "id", loading: this.state.loading })));
    }
}
export default withRouter(ListExperimentPage);
