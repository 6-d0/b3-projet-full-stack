declare interface IRegistration {
  uuid: string;
  date: Date;
  comment: string;
  course: ICourses;
  student: IUser;
  slot: ITimeslots;
}
