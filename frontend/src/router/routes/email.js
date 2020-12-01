
import VerifyEmailView from '@/views/email/verify/VerifyEmailView';
import ResetPasswordView from '@/views/email/password/ResetPasswordView';

const routes = [
	{ path: '/verifyemail/:token', component: VerifyEmailView, name: "verifyemail" },
	{ path: '/resetpassword/:token', component: ResetPasswordView, name: "resetpassword" },
];

export { routes }
export default routes;