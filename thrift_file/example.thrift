namespace py example
/* resources are setted in advance */



struct Response {
    1: i64 pid,
    2: string resource,
    3: string operation, /*success or failed*/
}
struct Request{
    1: i64 pid,
    2: string resource,
    3: string operation
}

service LockService {
    Response acquire_lock(1: Request request),
    Response release_lock(1: Request request),
}