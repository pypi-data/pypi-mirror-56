import React, { Component } from 'react';
import { Route, Redirect, Switch, HashRouter } from "react-router-dom";
import CreateExperimentPage from "./pages/create-experiment";
import CreateExecutionPage from "./pages/create-execution";
import ShowExperimentPage from "./pages/show-experiment";
import EditExecutionPage from "./pages/edit-execution";
import ListExperimentPage from "./pages/list-experiment";
import ShowExecutionPage from './pages/show-execution';
class App extends Component {
    constructor(props) {
        super(props);
        this.jlapp = props.jlapp;
    }
    render() {
        return (React.createElement("div", { className: "featurize-app" },
            React.createElement(HashRouter, null,
                React.createElement(Switch, null,
                    React.createElement(Route, { path: "/featurize", exact: true, component: ListExperimentPage }),
                    React.createElement(Route, { path: "/featurize/experiments/new", exact: true, component: CreateExperimentPage }),
                    React.createElement(Route, { path: "/featurize/experiments", exact: true, component: ListExperimentPage }),
                    React.createElement(Route, { path: "/featurize/experiments/:id", exact: true, component: ShowExperimentPage }),
                    React.createElement(Route, { path: "/featurize/experiments/:id/newExecution", exact: true, component: CreateExecutionPage }),
                    React.createElement(Route, { path: "/featurize/experiments/:experimentId/edit/:executionId", exact: true, component: EditExecutionPage }),
                    React.createElement(Route, { path: "/featurize/executions/:executionId", exact: true, render: (props) => React.createElement(ShowExecutionPage, Object.assign({}, props, { jlapp: this.jlapp })) }),
                    React.createElement(Redirect, { path: "/", exact: true, to: "/featurize" })))));
    }
}
export default App;
