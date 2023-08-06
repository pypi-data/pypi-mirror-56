export default abstract class Store<StateType> {
    state: StateType;
    abstract loadState(): Promise<StateType>;
    abstract getState(): StateType;
    setState(state: StateType): void;
}
