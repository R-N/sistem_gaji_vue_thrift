import akunClient from '@/rpc/client/akun';
import authClient from '@/rpc/client/auth';
import helloClient from '@/rpc/client/hello';
import userClient from '@/rpc/client/user';
import backupClient from '@/rpc/client/backup';

const clients = {
	akun: akunClient,
	auth: authClient,
	hello: helloClient,
	user: userClient,
	backup: backupClient
}

const init = (stores) => {
	Object.keys(clients).forEach(function(key) {
		clients[key].init(stores);
	});
}
const initClients = init;

export {
	clients, init, initClients,
	akunClient,
	authClient, 
	helloClient, 
	userClient,
	backupClient
};
export default clients