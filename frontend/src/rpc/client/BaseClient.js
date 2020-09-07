import {
	createHttpClient,
	createHttpConnection,
	HttpConnection,
	TBinaryProtocol,
	TBufferedTransport
} from "thrift";

import { appStore } from '@/store/modules/app';

const createClient = (
		serviceClass, 
		endpoint, 
		useHttps=null,
		backendHost=null,
		backendPort=null
	) => {

	useHttps = useHttps || defaultUseHttps;
	backendHost = backendHost || defaultBackendHost;
	backendPort = backendPort || defaultBackendPort;

	const options = {
		transport: TBufferedTransport,
		protocol: TBinaryProtocol,
		https: useHttps,
		path: endpoint
	};

	var connection = createHttpConnection(
		backendHost,
		backendPort,
		options
	);

	var client = createHttpClient(serviceClass.Client, connection);
	return client
}

const setUseHttps = (newUseHttps) => { defaultUseHttps = newUseHttps };
const setBackendHost = (newHost) => { defaultBackendHost = newHost };
const setBackendPort = (newPort) => { defaultBackendPort = newHost };

class BaseClient{
	client = null

	constructor(
		clientClass, 
		endpoint, 
		useHttps=null,
		backendHost=null,
		backendPort=null
	){
		this.client = createClient(clientClass, endpoint, useHttps, backendHost, backendPort);
	}

	async rehydrate(payload=null){
		
	}
}

export { BaseClient, createClient, setUseHttps, setBackendHost, setBackendPort };
export default BaseClient;