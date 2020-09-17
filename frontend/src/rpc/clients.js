import akunClient from '@/rpc/client/akun';
import authClient from '@/rpc/client/auth';
import helloClient from '@/rpc/client/hello';
import userClient from '@/rpc/client/user';
import backupClient from '@/rpc/client/backup';
import emailClient from '@/rpc/client/email';

const clients = {
	akun: akunClient,
	auth: authClient,
	hello: helloClient,
	user: userClient,
	backup: backupClient,
	email: emailClient
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
	backupClient,
	emailClient
};
export default clients