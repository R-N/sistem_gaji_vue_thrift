import userAuthClient from '@/rpc/client/user/auth';
import userEmailClient from '@/rpc/client/user/email';
import userManagementClient from '@/rpc/client/user/management';
import userProfileClient from '@/rpc/client/user/profile';
import userRecoveryClient from '@/rpc/client/user/recovery';

import helloHelloClient from '@/rpc/client/hello/hello';

import systemBackupClient from '@/rpc/client/system/backup';

import dataPerusahaanClient from '@/rpc/client/data/perusahaan';

const clients = {
	user: {
		auth: userAuthClient,
		email: userEmailClient,
		management: userManagementClient,
		profile: userProfileClient,
		recovery: userRecoveryClient
	},
	hello: {
		hello: helloHelloClient
	},
	system: {
		backup: systemBackupClient
	},
	data: {
		perusahaan: dataPerusahaanClient
	}
}

const init = (stores) => {
	Object.keys(clients).forEach(function(key) {
		let namespace = clients[key]
		Object.keys(namespace).forEach(function(key2) {
			namespace[key2].init(stores);
		});
	});
}
const initClients = init;

export {
	clients, 
	init, 
	initClients
};
export default clients