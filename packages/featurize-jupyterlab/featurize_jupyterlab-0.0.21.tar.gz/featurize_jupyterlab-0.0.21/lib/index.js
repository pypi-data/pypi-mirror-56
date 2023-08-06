import { ILayoutRestorer } from '@jupyterlab/application';
import { ICommandPalette, MainAreaWidget, WidgetTracker } from '@jupyterlab/apputils';
import { ILauncher } from '@jupyterlab/launcher';
import { Widget } from '@phosphor/widgets';
import App from './app';
import ReactDOM from 'react-dom';
import React from 'react';
class FeaturizeWidget extends Widget {
    constructor(jlapp) {
        super();
        this.addClass('featurize-widget');
        ReactDOM.render(React.createElement(App, { jlapp }), this.node);
    }
}
function main(app, palette, restorer, launcher) {
    // Create a single widget
    let widget;
    // Add an application command
    const command = 'featurize:experiment:open';
    if (launcher) {
        launcher.add({
            command: command,
            category: 'Featurize',
            rank: 0
        });
    }
    app.commands.addCommand(command, {
        label: 'Experiment',
        iconClass: args => (args['isPalette'] ? '' : 'featurize-main-icon'),
        execute: () => {
            if (!widget) {
                // Create a new widget if one does not exist
                const content = new FeaturizeWidget(app);
                widget = new MainAreaWidget({ content });
                widget.id = 'jupyterlab-featurize';
                widget.title.label = 'featurize experiment';
                widget.title.closable = true;
            }
            if (!tracker.has(widget)) {
                // Track the state of the widget for later restoration
                tracker.add(widget);
            }
            if (!widget.isAttached) {
                // Attach the widget to the main work area if it's not there
                app.shell.add(widget, 'main');
            }
            widget.content.update();
            // Activate the widget
            app.shell.activateById(widget.id);
        }
    });
    // Add the command to the palette.
    palette.addItem({ command, category: 'Featurize' });
    let tracker = new WidgetTracker({
        namespace: 'featurize'
    });
    restorer.restore(tracker, {
        command,
        name: () => 'featurize'
    });
}
const extension = {
    id: 'jupyterlab-featurize',
    autoStart: true,
    requires: [ICommandPalette, ILayoutRestorer, ILauncher],
    activate: main
};
export default extension;
