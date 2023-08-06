import Store from './base-store';
import { Component } from './constant';
export default class ListStore<ListType = Component> extends Store<ListType[]> {
    remoteUrl: string;
    state: ListType[];
    constructor(remoteUrl: string);
    loadState(): Promise<any>;
    getState(): ListType[];
}
