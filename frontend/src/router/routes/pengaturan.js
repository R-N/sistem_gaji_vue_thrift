
import BackupView from '@/views/pengaturan/backup/BackupView';
import AkunView from '@/views/pengaturan/akun/AkunView';

const routes = [
	{ path: 'pengaturan/variabel', component: null, name: "pengaturan-variabel" },
	{ path: 'pengaturan/backup', component: BackupView, name: "backup" },
	{ path: 'pengaturan/akun', component: AkunView, name: "akun" }
]

export { routes };
export default routes;