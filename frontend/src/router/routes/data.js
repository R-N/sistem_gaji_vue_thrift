
import DataPerusahaanView from '@/views/data/perusahaan/DataPerusahaanView';
import DataDepartemenView from '@/views/data/departemen/DataDepartemenView';

const routes = [
	{ path: 'data/perusahaan', component: DataPerusahaanView, name: "data-perusahaan" },
	{ path: 'data/departemen', component: DataDepartemenView, name: "data-departemen" },
	{ path: 'data/job-level', component: null, name: "data-job-level" },
	{ path: 'data/jabatan', component: null, name: "data-jabatan" },
	{ path: 'data/karyawan', component: null, name: "data-karyawan" },
	{ path: 'data/shift', component: null, name: "data-shift" },
]

export { routes };
export default routes;