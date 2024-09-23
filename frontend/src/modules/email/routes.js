
import VerifyEmailView from '@/modules/email/verify/views/main';
import ResetPasswordView from '@/modules/email/password/views/main';

const routes = [
    { path: '/verifyemail/:token', component: VerifyEmailView, name: "verifyemail" },
    { path: '/resetpassword/:token', component: ResetPasswordView, name: "resetpassword" },
];

export { routes }
export default routes;