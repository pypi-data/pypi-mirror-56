import { request } from '../utils';
;
export class DataProvider {
    constructor(identity, graphName) {
        this.startAt = 0;
        this.graphName = graphName;
        this.identity = identity;
    }
    async fetchMore() {
        const response = await request(`/executions/${this.identity}/graph`, 'get', {
            start_at: this.startAt,
            graph_name: this.graphName,
        });
        const result = await response.json();
        this.startAt = result.data.position;
        return result.data.points;
    }
}
