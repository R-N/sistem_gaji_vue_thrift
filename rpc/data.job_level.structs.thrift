namespace py data.job_level.structs
namespace js data.job_level.structs

struct TJobLevel{
	1: i32 id;
	2: bool enabled;
	3: string name;
    4: optional i32 gaji_pokok;
    5: optional i32 tunjangan_jabatan;
    6: optional i32 upah_lembur_1;
    7: optional i32 upah_lembur_2;
    8: optional i32 upah_lembur_3;
}

struct TJobLevelForm{
	1: string name;
    2: optional i32 gaji_pokok;
    3: optional i32 tunjangan_jabatan;
    4: optional i32 upah_lembur_1;
    5: optional i32 upah_lembur_2;
    6: optional i32 upah_lembur_3;
}

struct TJobLevelQuery{
	1: optional i32 limit;
	2: optional i32 offset;
	3: optional bool enabled;
}