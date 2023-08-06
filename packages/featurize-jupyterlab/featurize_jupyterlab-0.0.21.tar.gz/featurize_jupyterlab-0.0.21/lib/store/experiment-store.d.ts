import Store from './base-store';
import { Experiment, Execution, Component } from './constant';
declare class ExperimentStore extends Store<Experiment> {
    state: Experiment;
    constructor(id: string);
    getState(): Experiment;
    getExecution(id: string): Execution;
    loadState(): Promise<Experiment>;
    update(name: string, packages: string): Promise<boolean>;
    delete(): Promise<boolean>;
    loadExecutions(): Promise<Execution[]>;
    deleteExecution(id: string): Promise<boolean>;
    createExecution(): Promise<boolean>;
    loadComponents(): Promise<Component[]>;
}
export default ExperimentStore;
