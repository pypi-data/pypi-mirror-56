import React from 'react';
import { DataProvider } from './data-provider';
import { Execution } from '../store/constant';
interface DynamicChartProps {
    height: string;
    graphName: string;
    pullInterval: number;
    execution: Execution;
    maxPointsNum: number;
}
declare class DynamicChart extends React.Component<DynamicChartProps, {}> {
    dataProvider: DataProvider;
    static defaultProps: {
        height: string;
        maxPointsNum: number;
        pullInterval: number;
    };
    chart: any;
    chartRef: React.RefObject<HTMLDivElement>;
    interval: number;
    option: any;
    dataZoomed: boolean;
    constructor(props: DynamicChartProps);
    update: () => Promise<void>;
    componentWillUnmount(): void;
    componentDidMount(): void;
    render(): JSX.Element;
}
export default DynamicChart;
