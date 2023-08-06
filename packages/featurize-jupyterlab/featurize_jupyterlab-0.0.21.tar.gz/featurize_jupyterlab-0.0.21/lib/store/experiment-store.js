import Store from './base-store';
import { request } from '../utils';
class ExperimentStore extends Store {
    constructor(id) {
        super();
        this.state = {
            id,
            name: '',
            created_at: '',
            updated_at: '',
            enabled_packages: '',
            excutions: []
        };
        this.loadState();
    }
    getState() {
        return this.state;
    }
    getExecution(id) {
        for (let p in this.state.excutions) {
            if (this.state.excutions[p].id === id) {
                return this.state.excutions[p];
            }
        }
    }
    async loadState() {
        const response = await request(`/experiments/${this.state.id}`, 'get');
        const body = await response.json();
        this.state = body.data;
        this.state.excutions = await this.loadExecutions();
        return this.state;
    }
    async update(name, packages) {
        await request(`/experiments/${this.state.id}`, 'put', {
            name: name,
            enabled_packages: packages
        });
        return true;
    }
    async delete() {
        await request(`/experiments/${this.state.id}`, 'delete');
        return true;
    }
    async loadExecutions() {
        const response = await request(`/experiments/${this.state.id}/executions`, 'get');
        const body = await response.json();
        return body.data;
    }
    async deleteExecution(id) {
        await request(`/experiments/executions/${id}`, 'delete');
        return true;
    }
    async createExecution() {
        await request(`/experiments/${this.state.id}/executions`, 'post');
        return true;
    }
    async loadComponents() {
        const response = await request(`/experiments/${this.state.id}/components`, 'get');
        const body = await response.json();
        return body.data;
    }
}
export default ExperimentStore;
