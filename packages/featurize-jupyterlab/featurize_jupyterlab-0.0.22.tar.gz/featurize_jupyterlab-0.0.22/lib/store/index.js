import ListStore from './list-store';
import ExperimentStore from './experiment-store';
const stores = {
    'components': new ListStore('/components'),
    'experiments': new ListStore('/experiments')
};
const experimentStores = {};
export function getStore(storeName) {
    return stores[storeName];
}
export function getExperimentStore(identity) {
    if (experimentStores[identity]) {
        return experimentStores[identity];
    }
    return experimentStores[identity] = new ExperimentStore(identity);
}
