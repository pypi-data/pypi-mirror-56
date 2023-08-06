import Store from './base-store';
import { request } from '../utils';
export default class ListStore extends Store {
    constructor(remoteUrl) {
        super();
        this.remoteUrl = remoteUrl;
        this.state = [];
    }
    async loadState() {
        const response = await request(this.remoteUrl, 'get');
        const body = await response.json();
        this.state = body.data;
        return this.state;
    }
    getState() {
        return this.state;
    }
}
