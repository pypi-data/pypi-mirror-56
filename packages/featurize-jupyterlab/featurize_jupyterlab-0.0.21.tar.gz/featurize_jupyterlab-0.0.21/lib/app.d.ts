import { Component } from 'react';
import { JupyterFrontEnd } from '@jupyterlab/application';
interface AppProps {
    jlapp: JupyterFrontEnd;
}
declare class App extends Component<AppProps, {}> {
    jlapp: JupyterFrontEnd;
    constructor(props: AppProps);
    render(): JSX.Element;
}
export default App;
