namespace py data.departemen.structs
namespace js data.departemen.structs

struct TDepartemen{
	1: i32 id;
	2: bool enabled;
	3: string name;
	4: i32 perusahaan_id;
}

struct TDepartemenForm{
	1: string name;
	2: i32 perusahaan_id;
}

struct TDepartemenQuery{
	1: optional i32 limit;
	2: optional i32 offset;
	3: optional bool enabled;
	4: i32 perusahaan_id;
}