import React from 'react';
import { Breadcrumb } from 'antd';
import { Link } from 'react-router-dom';
class FeaturizeBreadcrumb extends React.Component {
    render() {
        return (React.createElement("div", { className: "featurize-breadcrumb" },
            React.createElement(Breadcrumb, { className: "breadcrumb" }, this.props.links.map((link) => React.createElement(Breadcrumb.Item, { key: link.name },
                React.createElement(Link, { to: link.link }, link.name))))));
    }
}
export default FeaturizeBreadcrumb;
