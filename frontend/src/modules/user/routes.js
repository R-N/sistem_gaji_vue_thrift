import AkunView from '@/modules/user/management/views/main';
import ProfilView from '@/modules/user/profile/views/main';

const routes = [
    { path: 'user/profile', component: ProfilView, name: "profile" },
    { path: 'user/management', component: AkunView, name: "user-management" },
]

export { routes };
export default routes;