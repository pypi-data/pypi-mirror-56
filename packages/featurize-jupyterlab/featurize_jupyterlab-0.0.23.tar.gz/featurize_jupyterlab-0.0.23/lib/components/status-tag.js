import { statusColor } from '../utils';
import { Tag } from 'antd';
import React from 'react';
export default function StatusTag(props) {
    const color = statusColor(props.status);
    return (React.createElement(Tag, { color: color }, props.status));
}
