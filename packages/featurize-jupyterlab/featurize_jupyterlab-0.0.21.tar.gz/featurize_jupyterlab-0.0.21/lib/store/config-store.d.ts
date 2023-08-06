import Store from './base-store';
import { ConfigState } from './constant';
declare class ConfigStore extends Store<ConfigState> {
    id: string;
    state: ConfigState;
    constructor(id: string);
    getState(): ConfigState;
    updateModule(data: any): Promise<void>;
    addModule(data: any): Promise<void>;
    loadState(): Promise<ConfigState>;
}
export default ConfigStore;
