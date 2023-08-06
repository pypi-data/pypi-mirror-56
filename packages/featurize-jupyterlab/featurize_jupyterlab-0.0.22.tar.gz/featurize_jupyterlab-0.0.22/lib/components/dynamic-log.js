import React from 'react';
import { request } from '../utils';
class DynamicLog extends React.Component {
    constructor(props) {
        super(props);
        this.fetch = async () => {
            const response = await request(`/executions/${this.props.execution.id}/log`, 'get', {
                offset: this.currentLine,
                limit: this.props.maxFetchLines,
                identity: this.props.execution.id
            });
            const result = await response.json();
            this.currentLine = result['data']['read_up_to'];
            if (result['data']['logs'] === "") {
                return [];
            }
            else {
                return result['data']['logs'].split('\n');
            }
        };
        this.update = async () => {
            const logs = await this.fetch();
            if (logs.length > 0) {
                this.setState({
                    logs: this.state.logs.concat(logs)
                });
            }
            if (!this.stopFetch) {
                setTimeout(this.update, this.props.pullInterval);
            }
        };
        this.state = {
            logs: []
        };
        this.currentLine = this.props.offset;
        this.stopFetch = false;
    }
    componentDidMount() {
        this.update();
    }
    componentWillUnmount() {
        this.stopFetch = true;
    }
    render() {
        return (React.createElement("div", { className: "featurize__dynamic-log" },
            React.createElement("div", { className: "log-container" }, this.state.logs.map((log, index) => React.createElement("div", { className: "log-line", key: this.currentLine + index },
                React.createElement("span", { className: "log-text" }, log))))));
    }
}
DynamicLog.defaultProps = {
    maxVisibleLines: 1000,
    maxFetchLines: 1024,
    pullInterval: 1000,
    offset: 0,
};
export default DynamicLog;
