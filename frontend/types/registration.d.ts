declare interface IRegistration{
    date: Date,
    comment: string,
    course: ICourses,
    student: IUser,
    slot: ITimeslots
}