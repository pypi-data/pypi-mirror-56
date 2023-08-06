import Store from './base-store';
import { request } from '../utils';
class ConfigStore extends Store {
    constructor(id) {
        super();
        this.state = {
            id: id,
            created_at: '',
            updated_at: '',
            name: '',
            config: {},
            experiment_id: ''
        };
    }
    getState() {
        return this.state;
    }
    async updateModule(data) {
        await request(`/experiments/modules/${data.id}`, 'put', Object.assign({}, data));
    }
    async addModule(data) {
        await request(`/executions/${this.state.id}/modules`, 'post', Object.assign({}, data));
    }
    async loadState() {
        const response = await request(`/executions/${this.state.id}/modules`, 'get');
        const body = await response.json();
        this.state.config = body.data;
        return this.state;
    }
}
export default ConfigStore;
