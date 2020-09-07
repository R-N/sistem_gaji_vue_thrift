import {
	createHttpClient,
	createHttpConnection,
	HttpConnection,
	TBinaryProtocol,
	TBufferedTransport
} from "thrift";


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

	constructor(clientClass, endpoint){
		this.client = createClient(clientClass, endpoint);
	}

	async rehydrate(payload=null){
		
	}
}

export { BaseClient, createClient };
export default BaseClient;