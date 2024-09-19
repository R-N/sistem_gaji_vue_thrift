
import DataPerusahaanView from '@/views/data/perusahaan/DataPerusahaanView';
import DataDepartemenView from '@/views/data/departemen/DataDepartemenView';
import DataJobLevelView from '@/views/data/job_level/DataJobLevelView';

const routes = [
	{ path: 'data/perusahaan', component: DataPerusahaanView, name: "data-perusahaan" },
	{ path: 'data/departemen', component: DataDepartemenView, name: "data-departemen" },
	{ path: 'data/job-level', component: DataJobLevelView, name: "data-job-level" },
	{ path: 'data/jabatan', component: null, name: "data-jabatan" },
	{ path: 'data/karyawan', component: null, name: "data-karyawan" },
	{ path: 'data/shift', component: null, name: "data-shift" },
]

export { routes };
export default routes;