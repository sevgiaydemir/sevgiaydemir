class firmwareTemplates {
    constructor() {
        this.baseHeaders = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'AutomationTest/1.0'
        }
    }

    getHeaders(accessToken = '', additionalHeaders = {}) {
        const headersWithToken = { ...this.baseHeaders }
        if (accessToken) {
            headersWithToken['Authorization'] = `Bearer ${accessToken}`
        }
        return { ...headersWithToken, ...additionalHeaders }
    }
}
module.exports = firmwareTemplates;
