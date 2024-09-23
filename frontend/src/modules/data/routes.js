
import DataPerusahaanView from '@/modules/data/perusahaan/views/main';
import DataDepartemenView from '@/modules/data/departemen/views/main';
import DataJobLevelView from '@/modules/data/job_level/views/main';

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