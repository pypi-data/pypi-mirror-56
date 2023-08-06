import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
export function capitalize(s) {
    return s.charAt(0).toUpperCase() + s.slice(1);
}
export function statusColor(status) {
    const colorMapping = {
        training: 'green',
        idle: 'blue',
        not_running: 'gray',
        error: 'red'
    };
    return colorMapping[status] || 'orange';
}
export function pendingStatus(status) {
    return ['stopping', 'booting', 'starting', 'killing'].indexOf(status) > 0;
}
export function request(url, method, request = null) {
    let fullRequest;
    if (request === null) {
        fullRequest = {
            method: method
        };
    }
    else if (method === 'delete' || method === 'get' || method === 'head') {
        fullRequest = {
            method: method,
        };
        url = url + '?' + Object.keys(request).map(function (key) {
            return key + '=' + request[key];
        }).join('&');
    }
    else {
        fullRequest = {
            method: method,
            body: (request instanceof FormData) ? request : JSON.stringify(request)
        };
    }
    let setting = ServerConnection.makeSettings();
    let fullUrl = URLExt.join(setting.baseUrl, '/featurize', url);
    return ServerConnection.makeRequest(fullUrl, fullRequest, setting);
}
export function upload(url, request = null) {
    let setting = ServerConnection.makeSettings();
    let fullUrl = URLExt.join(setting.baseUrl, '/featurize', url);
    const xsrfToken = getCookie('_xsrf');
    return fetch(fullUrl, {
        headers: new Headers([['X-XSRFToken', xsrfToken]]),
        method: 'post',
        body: request
    });
}
export function getCookie(name) {
    const matches = document.cookie.match('\\b' + name + '=([^;]*)\\b');
    return matches ? matches[1] : undefined;
}
export async function requestData(url, method, data = null) {
    const response = await request(url, method, data);
    const result = await response.json();
    return result['data'];
}
