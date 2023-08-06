import React from 'react';
interface BreadcrumbProps {
    links: Array<{
        name: string;
        link: string;
    }>;
}
declare class FeaturizeBreadcrumb extends React.Component<BreadcrumbProps, {}> {
    render(): JSX.Element;
}
export default FeaturizeBreadcrumb;
