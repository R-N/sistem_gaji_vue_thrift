import {
	createHttpClient,
	createHttpConnection,
	HttpConnection,
	TBinaryProtocol,
	TBufferedTransport
} from "thrift";

import { StoreUser } from '@/store/user';

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
const setBackendPort = (newPort) => { defaultBackendPort = newPort };

class TBaseClient extends StoreUser{
	client = null

	constructor(
		stores,
		clientClass, 
		endpoint, 
		useHttps=null,
		backendHost=null,
		backendPort=null
	){
		super(stores);
		this.client = createClient(clientClass, endpoint, useHttps, backendHost, backendPort);
	}

	async rehydrate(payload=null){
		
	}
}

export { TBaseClient, createClient, setUseHttps, setBackendHost, setBackendPort };
export default TBaseClient;