namespace py data.perusahaan.structs
namespace js data.perusahaan.structs

struct TPerusahaan{
	1: i32 id;
	2: bool enabled;
	3: string name;
}

struct TPerusahaanForm{
	1: string name;
}

struct TPerusahaanQuery{
	1: optional i32 limit;
	2: optional i32 offset;
	3: optional bool enabled;
}