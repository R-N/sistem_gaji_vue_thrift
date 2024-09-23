
import BackupView from '@/modules/system/backup/views/main';
// import AkunView from '@/modules/user/management/views/main';

const routes = [
    { path: 'system/variabel', component: null, name: "system-variables" },
    { path: 'system/backup', component: BackupView, name: "backup" },
    // { path: 'system/akun', component: AkunView, name: "akun" }
]

export { routes };
export default routes;