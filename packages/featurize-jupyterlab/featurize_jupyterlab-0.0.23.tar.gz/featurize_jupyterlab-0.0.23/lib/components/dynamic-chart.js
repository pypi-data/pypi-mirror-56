import React from 'react';
import Echart from 'echarts';
import { DataProvider } from './data-provider';
class DynamicChart extends React.Component {
    constructor(props) {
        super(props);
        this.update = async () => {
            const points = await this.dataProvider.fetchMore();
            this.option.series[0].data.push(...Object.values(points).map(i => i.y));
            this.option.xAxis.data.push(...Object.values(points).map(i => i.x));
            this.option.dataZoom[0].endValue = !this.dataZoomed ? this.option.xAxis.data.length - 1 : null;
            this.option.dataZoom[0].startValue = !this.dataZoomed ? this.option.xAxis.data.length - 301 : null;
            this.chart.setOption(this.option, false, true, false);
            this.interval = setTimeout(this.update, this.props.pullInterval);
        };
        this.dataProvider = new DataProvider(this.props.execution.id, this.props.graphName);
        this.chartRef = React.createRef();
    }
    componentWillUnmount() {
        clearTimeout(this.interval);
    }
    componentDidMount() {
        this.option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross',
                    label: {
                        backgroundColor: '#ffa39e'
                    }
                }
            },
            title: {
                left: 'center',
                text: this.props.graphName,
            },
            toolbox: {
                show: false
            },
            xAxis: {
                data: []
            },
            yAxis: {
                type: 'value',
                boundaryGap: [0, '100%']
            },
            dataZoom: [
                {
                    show: true,
                    realtime: true
                }
            ],
            series: [
                {
                    name: this.props.graphName,
                    type: 'line',
                    smooth: true,
                    symbol: 'none',
                    sampling: 'average',
                    itemStyle: {
                        color: '#ffa39e'
                    },
                    data: []
                }
            ]
        };
        this.chart = Echart.init(this.chartRef.current);
        this.dataZoomed = false;
        this.chart.on('dataZoom', (e) => {
            this.dataZoomed = true;
        });
        this.update();
    }
    render() {
        return (React.createElement("div", { className: "featurize__chart" },
            React.createElement("div", { ref: this.chartRef, style: { height: `${this.props.height}px` } })));
    }
}
DynamicChart.defaultProps = {
    height: "400",
    maxPointsNum: 300,
    pullInterval: 3000
};
export default DynamicChart;
